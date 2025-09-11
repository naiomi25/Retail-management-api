from database import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class User(db.Model):
    __tablename__= 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    user_name : Mapped[str] = mapped_column(nullable = False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    
    def serialize(self):
        return{ 
        'name' : self.name,
        'email': self.email,
        'user_name' : self.user_name
        }
    
    

