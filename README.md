# FastAPI Todo Project (Educational)

---

## 🇬🇧 English

### 📌 Description

This is an **educational Todo application** built with **FastAPI**. The project is designed to demonstrate a clean backend architecture, modern Python tooling, and common patterns used in real-world web services.

The application includes user authentication, task management, database migrations, caching, message brokers, and automated tests.

---

### 🚀 Features

* User authentication (email + OAuth providers)
* Todo / task management
* Layered architecture (handlers, services, repositories)
* PostgreSQL database with Alembic migrations
* Cache layer
* Message broker support
* Dependency Injection
* Docker & Docker Compose setup
* Unit and integration tests

---

### 🛠 Tech Stack

* **Python 3.13**
* **FastAPI**
* **SQLAlchemy**
* **Alembic**
* **PostgreSQL**
* **Redis (cache)**
* **Message Broker**
* **Poetry**
* **Pytest**
* **Docker / Docker Compose**

---

### 📂 Project Structure

```
app/
├── main.py            # Application entry point
├── settings.py        # Application settings
├── dependency.py      # Dependency injection
├── exceptions.py      # Custom exceptions
│
├── infrastructure/    # External services (DB, cache, broker)
├── users/             # User & auth domain
├── tasks/             # Todo / tasks domain
├── broker/            # Message broker logic
│
├── tests/             # Unit & integration tests
├── alembic/           # Database migrations
```

---

### ⚙️ Installation

```bash
# clone repository

git clone <repo-url>
cd project

# install dependencies
poetry install
```

---

### ▶️ Run Locally

```bash
# activate virtual environment
poetry shell

# start application
uvicorn app.main:app --reload
```

Application will be available at:

```
http://localhost:8000
```

Swagger UI:

```
http://localhost:8000/docs
```

---

### 🐳 Run with Docker

```bash
docker-compose up --build
```

---

### 🧪 Tests

```bash
pytest
```

---

### 🎓 Purpose

This is a **first serious backend project** created during studies.

The main goals of this project:

* Learn FastAPI and modern Python backend development
* Practice clean architecture and separation of concerns
* Work with databases, migrations, caching, and message brokers
* Gain experience with Docker and testing

This project is **not a tutorial or a guide**, but a hands-on learning project built step by step during the learning process.

---



Проект **не является пособием или учебником**, а представляет собой практическую работу, выполненную в процессе обучения.
