# Employee Search API

A FastAPI-based backend API for employee search functionality using SQLite database.

## Prerequisites

- **For Docker method**: Docker and Docker Compose installed
- **For Manual method**: Python 3.11+ and pip

## Getting Started

### Method 1: Docker Compose (Recommended)

This is the easiest way to start the project. Docker will handle all dependencies and setup automatically.

#### Steps:

1. **Build and start the application:**
   ```bash
   docker-compose up --build
   ```

2. **Or run in detached mode:**
   ```bash
   docker-compose up -d --build
   ```

3. **View logs:**
   ```bash
   docker-compose logs -f
   ```

4. **Stop the application:**
   ```bash
   docker-compose down
   ```

The API will be available at:
- **API Base URL**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

The SQLite database (`employee_search.db`) will be created automatically in the project directory and will persist between container restarts.

---

### Method 2: Manual Setup with Uvicorn

For local development without Docker.

#### Steps:

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd employee_search
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Set environment variables (optional):**
   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=sqlite:///./employee_search.db
   API_V1_PREFIX=/api/v1
   ```
   
   If you don't create a `.env` file, the application will use the default values.

6. **Start the application:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

   The `--reload` flag enables auto-reload on code changes (useful for development).

7. **Access the API:**
   - **API Base URL**: `http://localhost:8000`
   - **API Documentation**: `http://localhost:8000/docs`
   - **Alternative Docs**: `http://localhost:8000/redoc`

The SQLite database will be created automatically on first startup in the project root directory.

---

## Database

The application uses SQLite database (`employee_search.db`) which is created automatically when the application starts. The database file will be located in the project root directory.

### Optional: Setup Test Data

If you want to populate the database with test data, you can run:

```bash
python -m app.tasks.set_up_data
```

Or if using Docker:

```bash
docker-compose exec app python -m app.tasks.set_up_data
```
