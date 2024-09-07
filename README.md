# Candidate Management API

## Overview

This project is a **Candidate Profile Management** system allowing users to create, view, update, delete, and search for candidate profiles via a FastAPI-based API with MongoDB as the database. Users can also generate reports of candidate profiles in CSV format. The project is containerized using Docker and follows best practices to ensure production-readiness.

---

## Table of Contents

- [Candidate Management API](#candidate-management-api)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Technologies Used](#technologies-used)
  - [Requirements](#requirements)
  - [Getting Started](#getting-started)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Set Up Environment Variables](#2-set-up-environment-variables)
    - [3.  Run the Application with Docker](#3--run-the-application-with-docker)
    - [4.  Access the API](#4--access-the-api)
    - [5. Access Swagger API Documentation](#5-access-swagger-api-documentation)
    - [5. Running Tests](#6-running-tests)
    

---

## Technologies Used

- **Python**
- **FastAPI** - Web framework for building APIs
- **Pydantic** - For request model validation
- **MongoDB** - As the database
- **Docker** - Containerization
- **docker-compose** - Service orchestration
- **TDD** - Test-Driven Development methodology
- **Service/Repository Design Pattern** - Separation of concerns for maintainability

---

## Requirements

- **Python 3.11+**
- **Docker** and **docker-compose**
- A **MongoDB** instance (can be run in a container)

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd recruitment-fastapi

MONGO_URL=mongodb://mongo:27017
SECRET_KEY=your_secret_key_here

```

### 2. Set Up Environment Variables
Create a .env file in the root directory with the following content:

```bash
MONGO_INITDB_ROOT_USERNAME=your_username_here
MONGO_INITDB_ROOT_PASSWORD=your_password_here
MONGO_INITDB_DATABASE=your_database_name_here

DATABASE_URL=your_database_url_here

ACCESS_TOKEN_EXPIRES_IN=15
REFRESH_TOKEN_EXPIRES_IN=60
JWT_SECRET=fastapi
```

### 3.  Run the Application with Docker
Build and run the application using Docker Compose:

```
docker-compose up --build
```

### 4.  Access the API
```
Once the app is running, you can access it at http://localhost:8000.
```

### 5. Access Swagger API Documentation
```
FastAPI generates documentation automatically. You can access it at:

Swagger UI: http://localhost:8000/docs
Redoc: http://localhost:8000/redoc
```

### 5. Running Tests
Ensure you have all test dependencies installed. You can do this by installing the requirements from requirements.txt

```
pip install -r requirements.txt
```

Run Tests Locally

```
pytest
```

