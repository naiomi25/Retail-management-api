# Web Data Management API

## Overview

This API allows users to register, log in, and manage daily entries of sales and store metrics. Users can create, update, delete, and query entries. The API also provides aggregated statistics by shift for selected date ranges.

---
## Backend
## Base URL

`http://localhost:5000/api/`

---

## Authentication

The API uses **JWT tokens** for authentication. You need to log in to get an access token to include in subsequent requests.

### Register a new user

| Method | Endpoint            |
| ------ | ------------------- |
| POST   | /api/users/register |

**Request Body (JSON):**

```json
{
  "username": "exampleuser",
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**

* `201 Created` if successful
* Error messages with appropriate status codes

### Log in

| Method | Endpoint         |
| ------ | ---------------- |
| POST   | /api/users/login |

**Request Body (JSON):**

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
  "access_token": "<JWT token>"
}
```

Include the token in subsequent requests in the `Authorization` header:

```
Authorization: Bearer <JWT token>
```

---

## Entries Endpoints

### Create a new entry

| Method | Endpoint            |
| ------ | ------------------- |
| POST   | /api/entries/create |

**Request Body (JSON):**

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

**Response:** `201 Created` with entry details

### Modify an entry

| Method | Endpoint                         |
| ------ | -------------------------------- |
| PUT    | /api/entries/modify/\<entry\_id> |

**Request Body (JSON):**

```json
{
  "articles": 150,
  "apparel": 55
}
```

**Response:** `200 OK` with updated entry details

### Delete an entry

| Method | Endpoint                         |
| ------ | -------------------------------- |
| DELETE | /api/entries/delete/\<entry\_id> |

**Response:** `200 OK` if successfully deleted

### Query entries by date range

| Method | Endpoint                                                         |
| ------ | ---------------------------------------------------------------- |
| GET    | /api/entries/range/?start\_date=YYYY-MM-DD\&end\_date=YYYY-MM-DD |

**Query Parameters:**

* `start_date`: start of the range (required)
* `end_date`: end of the range (required)

**Response:**

```json
{
  "start_date": "2025-09-10",
  "end_date": "2025-09-13",
  "total_entries": 4,
  "entries": [
    {...},
    {...}
  ],
  "averages_by_shift": {
    "morning": {...},
    "afternoon": {...}
  }
}
```

Aggregated averages are provided **per shift**.

---

## Notes

* Calculated metrics (`average`, `UPT`, `CR`) are automatically computed in the backend.
* Only the authenticated user can access or modify their own entries.
* The API expects decimal numbers for financial metrics and integers for counts.
