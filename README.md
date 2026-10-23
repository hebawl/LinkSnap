# LinkSnap 🔗

A simple URL shortener built with **FastAPI** and **PostgreSQL**. Create short links and redirect users to their original URLs.

🌐 **Live demo:** https://linksnap-spu6.onrender.com

## Features

- Create short URLs from longer links.
- Redirect short links to their original destinations.
- Store links in a PostgreSQL database.
- Generate unique six-character short codes.
- REST API with interactive documentation.
- Health-check endpoint.
- Automated tests with `pytest`.

## Tech Stack

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL, Neon
- **Database driver:** Psycopg
- **Templates:** Jinja2
- **Testing:** Pytest
- **Deployment:** Render
- **Version control:** Git and GitHub

## Getting Started

### Prerequisites

- Python 3.12 or compatible version
- Git
- A PostgreSQL database, such as [Neon](https://neon.tech/)

### 1. Clone the repository

```bash
git clone https://github.com/hebawl/LinkSnap.git
cd LinkSnap
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root. Use `.env.example` as a reference, if available.

Configure your database connection using `DATABASE_URL`, or use the local database settings supported by the application.

Example:

```env
DATABASE_URL=your_postgresql_connection_string
BASE_URL=http://127.0.0.1:8000
```

Replace the example value with your own database connection string. **Never commit your `.env` file or publish database credentials.**

### 5. Run the application

```powershell
uvicorn app.main:app --reload
```

Open these URLs in your browser:

- **Application:** http://127.0.0.1:8000
- **API documentation:** http://127.0.0.1:8000/docs
- **Health check:** http://127.0.0.1:8000/health

## Running Tests

Run the automated test suite with:

```powershell
pytest
```

## Roadmap

- [x] Publish the source code on GitHub
- [x] Deploy the application to Render
- [x] Connect a hosted PostgreSQL database
- [ ] Improve the frontend and user experience
- [ ] Add click analytics
- [ ] Add rate limiting
- [ ] Explore caching for improved performance
