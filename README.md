# Table Reservation API

A simple RESTful API service for managing restaurant tables and reservations.  
Built with FastAPI, PostgreSQL, SQLAlchemy, Alembic, and Docker.

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/karim3487/table_reservation_api.git
cd table_reservation_api
```

### Environment Setup

- `.env` – default (dev)
- `.env.test` – for tests
- `.env.prod` – for production


```bash
cp env.example .env
cp env.prod.example .env.prod

cp env.test.example .env.test
```

### Build and start the app with Docker (using `.env.prod`)

```bash
make build && make up
```

### Run migrations

```bash
make migrate
```

### Run Tests

```bash
make test-db-up
make run-tests-docker
make test-db-down
```

## 🧱 Project Structure

```
app/
├── core/           # App settings, logging, middleware
├── db/             # DB session and Alembic config
├── models/         # SQLAlchemy models
├── schemas/        # Pydantic schemas
├── services/       # Business logic
├── repositories/   # DB queries
├── routers/        # API endpoints
├── errors/         # Custom exceptions & handlers
└── main.py         # App entry point
```


📚 API Docs

After starting the app, go to:
👉 http://localhost:8000/docs
