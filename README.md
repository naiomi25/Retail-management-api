# 📊 Web Data Management API (Backend)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Overview

This repository contains the **backend** of a Web Data Management project. It provides a robust REST API for user registration, authentication, and comprehensive CRUD operations on daily sales entries, including advanced analytics by date ranges and shifts.

## ⚡ Key Features

- 🔐 **JWT Authentication** - Secure user registration and login
- 📝 **CRUD Operations** - Complete entry management system
- 📊 **Advanced Analytics** - Date range queries with shift-based aggregations
- 🛡️ **Data Security** - User-specific data access control
- 📈 **Automatic Metrics** - Real-time calculation of KPIs (Average, UPT, CR)

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3.11+** | Core language |
| **Flask** | Web framework |
| **Flask-JWT-Extended** | JWT authentication |
| **SQLAlchemy** | ORM and database operations |
| **Flask-Migrate** | Database migrations |
| **PostgreSQL** | Relational database |
| **Flask-CORS** | Cross-origin request handling |

## 🚀 Installation

### Prerequisites
- Python 3.11 or higher
- PostgreSQL database
- Git

### Step-by-step Setup

1. **Clone the repository**
   ```bash
   git clone <repository_url>
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   
   **Windows:**
   ```bash
   .venv\Scripts\activate
   ```
   
   **Mac/Linux:**
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=your_postgres_connection_string
   JWT_SECRET_KEY=your_jwt_secret
   ```

6. **Initialize database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

7. **Run the server**
   ```bash
   flask --app app.py run
   ```

🎉 **Server running at:** `http://127.0.0.1:5000`

## 📡 API Endpoints

### 👤 User Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/users/register` | Register new user |
| `POST` | `/api/users/login` | Authenticate user |

### 📊 Entry Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/entries/create` | Create new sales entry |
| `PUT` | `/api/entries/modify/<entry_id>` | Update existing entry |
| `DELETE` | `/api/entries/delete/<entry_id>` | Delete entry |
| `GET` | `/api/entries/range/` | Query entries by date range |

---

## 🔐 Authentication

The API uses **JWT tokens** for secure authentication. Follow these steps:

### Register a New User

**Endpoint:** `POST /api/users/register`

**Request Body:**
```json
{
  "username": "exampleuser",
  "email": "user@example.com", 
  "password": "securepassword"
}
```

**Response:**
- ✅ `201 Created` - Registration successful
- ❌ `400 Bad Request` - Validation errors

### User Login

**Endpoint:** `POST /api/users/login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "msn": "User logged in successfully",
  "access_token": "<JWT_TOKEN>"
}
```

### 🔑 Using Authentication Token

Include the JWT token in all subsequent requests:

```http
Authorization: Bearer <JWT_TOKEN>
```

---

## 📈 Entry Operations

### Create New Entry

**Endpoint:** `POST /api/entries/create`

**Request Body:**
```json
{
  "date": "2025-09-12",
  "shift": "morning",
  "net_sales": 500.00,
  "transactions": 50,
  "articles": 140,
  "accessories": 40,
  "apparel": 50,
  "footfall": 20
}
```

**Response:** `201 Created` with calculated metrics

### Modify Entry

**Endpoint:** `PUT /api/entries/modify/<entry_id>`

**Request Body:**
```json
{
  "articles": 150,
  "apparel": 55
}
```

**Response:** `200 OK` with updated entry

### Delete Entry

**Endpoint:** `DELETE /api/entries/delete/<entry_id>`

**Response:** `200 OK` - Entry successfully deleted

### 🎯 Query by Date Range ⭐ **Feature Highlight**

**Endpoint:** `GET /api/entries/range/`

**Query Parameters:**
- `start_date`: Start date (YYYY-MM-DD) - **Required**
- `end_date`: End date (YYYY-MM-DD) - **Required**

**Example Request:**
```
GET /api/entries/range/?start_date=2025-09-10&end_date=2025-09-13
```

**Response:**
```json
{
  "start_date": "2025-09-10",
  "end_date": "2025-09-13", 
  "total_entries": 4,
  "entries": [
    {
      "id": 1,
      "date": "2025-09-10",
      "shift": "morning",
      "net_sales": 450.50,
      "transactions": 35,
      "average": 12.87,
      "upt": 4.2,
      "cr": 87.5
    }
  ],
  "averages_by_shift": {
    "morning": {
      "avg_net_sales": 425.75,
      "avg_transactions": 32,
      "avg_articles": 125,
      "avg_cr": 85.2
    },
    "evening": {
      "avg_net_sales": 620.25,
      "avg_transactions": 45,
      "avg_articles": 165,
      "avg_cr": 92.1
    }
  }
}
```

---

## 📊 Data Model

### Entry Fields

| Field | Type | Description |
|-------|------|-------------|
| `date` | Date | Entry date |
| `shift` | String | Work shift (morning, afternoon, evening) |
| `net_sales` | Decimal | Total sales amount |
| `transactions` | Integer | Number of transactions |
| `articles` | Integer | Total articles sold |
| `accessories` | Integer | Accessories sold |
| `apparel` | Integer | Apparel items sold |
| `footfall` | Integer | Customer traffic |

### Calculated Metrics (Automatic)

| Metric | Formula | Description |
|--------|---------|-------------|
| `average` | net_sales ÷ articles | Average price per article |
| `upt` | (articles ÷ transactions) × 100 | Units Per Transaction |
| `cr` | (transactions ÷ footfall) × 100 | Conversion Rate |

---

## 🔒 Security Features

- ✅ **JWT Authentication** - Secure token-based auth
- ✅ **User Isolation** - Users can only access their own data
- ✅ **Input Validation** - Server-side data validation
- ✅ **Error Handling** - Comprehensive error responses

## 📝 Important Notes

- 🧮 **Automatic Calculations:** Metrics (average, UPT, CR) are computed server-side
- 🔐 **Data Privacy:** Users can only access/modify their own entries
- 💰 **Number Format:** Decimal numbers for financial data, integers for counts
- 📅 **Date Format:** All dates must be in YYYY-MM-DD format

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ using Flask and PostgreSQL**

[⬆ Back to top](#-web-data-management-api-backend)

</div>
