# E-commerce Chatbot Backend

This is the backend service for the E-commerce Customer Support Chatbot.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Database Setup
1. Install PostgreSQL on your system
2. Create a new database named `ecommerce_chatbot`
3. Copy `env.example` to `.env` and update the database connection string:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/ecommerce_chatbot
   GROQ_API_KEY=your_groq_api_key_here
   ```

### 3. Load Data
Run the data loading script to populate the database with e-commerce data:
```bash
python load_data.py
```

### 4. Run the Server
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation
Once the server is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Project Structure
- `database.py` - Database configuration and connection
- `models.py` - SQLAlchemy models for database tables
- `load_data.py` - Script to load CSV data into the database
- `main.py` - FastAPI application and API endpoints
- `schemas.py` - Pydantic models for request/response validation
- `services/` - Business logic and LLM integration 