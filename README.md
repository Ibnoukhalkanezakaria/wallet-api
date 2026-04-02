# Digital Wallet API

A production-ready digital wallet API built with FastAPI, SQLAlchemy, asyncpg, and PostgreSQL. It demonstrates clean architecture, robust concurrency handling (using row-level locking to prevent race conditions during transfers), and atomic transactions to ensure financial data integrity.

## Prerequisites
- Docker & Docker Compose

## Quick Start (Docker)
1. Navigate to the `wallet-api` directory.
2. Start the services using Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. The API will be running at `http://localhost:8000`.
4. Swagger Documentation is available at: `http://localhost:8000/docs`.

## Example API Calls (cURL)

### 1. Create a Wallet
```bash
curl -X POST "http://localhost:8000/api/wallets"
```
*Output: `{"walletId":"<uuid>","balance":0}`*

### 2. Deposit Money
```bash
curl -X POST "http://localhost:8000/api/wallets/<wallet_id>/deposit" \
     -H "Content-Type: application/json" \
     -d '{"amount": 100.00}'
```

### 3. Get Balance
```bash
curl "http://localhost:8000/api/wallets/<wallet_id>/balance"
```

### 4. Transfer Money
```bash
curl -X POST "http://localhost:8000/api/wallets/transfer" \
     -H "Content-Type: application/json" \
     -d '{"fromWalletId": "<wallet_a>", "toWalletId": "<wallet_b>", "amount": 50.00}'
```

## Running Tests
Ensure dependencies are installed locally, or run them within the container:
```bash
pytest tests/
```

## Architecture Notes
- Uses `FastAPI` to provide immediate data validation (Pydantic) and auto-generated Swagger UI.
- Implements **Clean Architecture**: Routers -> Services -> Repositories.
- Handles race conditions by statically sorting IDs and using strict `SELECT ... FOR UPDATE` before mutations, preventing deadlocks when concurrent circular transfers occur.
- Handles custom exceptions automatically translated to specific HTTP status codes.
- Relational mapping done fully asynchronously using `asyncpg`.
