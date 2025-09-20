import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import select


from database import db
from models.model_entries import Entry
from models.model_users import User

entries = Blueprint("entries", __name__, url_prefix="/api/entries")

@entries.route('/create',methods = ['POST'])
@jwt_required()
def create_entry():
    
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        required_fields= ["date","shift", "net_sales","transactions","articles", "accessories","apparel", "footfall"] 
        if not all (field in data and data[field] for field in  required_fields):
            return jsonify ({'error': 'no se han introducido todos los datos'}),400  
        
        new_entry = Entry(
            user_id = user_id,
            date = data['date'],
            shift = data["shift"],
            net_sales = data["net_sales"],
            transactions = data["transactions"],
            articles = data["articles"],
            accessories = data["accessories"],
            apparel = data["apparel"],
            footfall = data["footfall"]
        )
        new_entry.calculate_metrics()
        db.session.add(new_entry)
        db.session.commit()
        
        return jsonify({
        'msg': 'entrada introducida correctamente',
        'entry': new_entry.serialize() }), 201 
                                                                         
         
    except Exception as e:
        print('error de entrada',e)
        return jsonify( 'Error al cargar los datos'),500
    
    
@entries.route('/modify/<int:entry_id>',methods= ['PUT'])
@jwt_required()
def modify_entry(entry_id):
    try:
        data = request.get_json()
        
        if not data :
            return jsonify({'message': 'Debe cambair algún valor'}),400
        
        user_id =int(get_jwt_identity())
        
        stm = db.session.scalar(select(Entry).where(Entry.id == entry_id))
        
        print("DEBUG - user_id del token:", user_id)
        print("DEBUG - user_id de la entrada:", stm.user_id)
        
        if not stm:
            return jsonify({'message': 'No existe ese dato'}), 404
        
       
        
        if stm.user_id != user_id :
            return jsonify({'message':'no puedes acceder a ese dato'}),401
        
        for key, value in data.items():
             if key not in ["id", "user_id"]:
                setattr(stm, key, value)
                
        stm.calculate_metrics() 
        db.session.commit()  
        return jsonify({ 'msg': 'Entrada actualizada correctamente', 'entry': stm.serialize()}), 200    
        
        
    except Exception as e:
        print('error al obrener los datos',e)
        return jsonify ({'error':'Error al obtener los datos'}),500
    
@entries.route('/delete/<int:entry_id>',methods = ['DELETE'])
@ jwt_required ()
def delete_entry(entry_id) :
    try:

        user_id = int(get_jwt_identity())
        
        id_entry = db.session.scalar(select(Entry).where(Entry.id == entry_id))
        
        
        if not id_entry :
            return jsonify({'msg':'dato no encontrado en la base de datos'}),404
        
        if id_entry.user_id != user_id:
              return jsonify({'msg': 'no puedes borrar esta entrada'}), 401
            
        
        db.session.delete(id_entry)
        db.session.commit()
        return jsonify({'msg': 'entrada eliminada correctamente'}), 200
    except Exception as e:
        print('error al obrener los datos',e)
        return jsonify ({'error':'Error al obtener los datos'}),500
    
    
@entries.route('/range/',methods = ['GET'])
@jwt_required()
def get_by_date():
    
    try:
    
        user_id= int(get_jwt_identity())
        
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date :
            return jsonify({'msg':'debes introducir las fechas de consulta'}),400
        
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        entries = db.session.scalars(select(Entry) .where(Entry.user_id == user_id).where(Entry.date.between(start, end).order_by(Entry.date)).all())
        
        return jsonify({
            'start_date': start_date,
            'end_date': end_date,
            'total_entries': len(entries),
            'entries': [entry.serialize() for entry in entries]
        })
        
         
    except Exception as e:
        print('Error al obtener entradas por rango:', e)
        return jsonify({'error': 'Error al obtener los datos'}), 500
    