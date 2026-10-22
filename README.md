# LinkSnap — URL Shortener

A lightweight URL shortener built with **Python, FastAPI, and PostgreSQL**. LinkSnap turns long URLs into compact links and redirects visitors to their original destinations.

> **Project status:** Under development. Local application functionality is implemented; production deployment and additional hardening are planned.

## Overview

LinkSnap is a full-stack web application designed to explore REST API development, relational database integration, URL redirection, and deployment.

The project combines a simple web interface with a Python backend and PostgreSQL database to create and retrieve short links.

## Features

- **Short URL generation** — generates random six-character alphanumeric codes.
- **Persistent storage** — saves short codes and original URLs in PostgreSQL.
- **Automatic redirection** — redirects visitors to the original destination.
- **Web interface** — provides a clean interface for submitting URLs.
- **Copy to clipboard** — makes generated short links easy to copy.
- **Input validation** — validates submitted URLs using Pydantic.
- **Collision handling** — retries code generation when a short code already exists.
- **Health endpoint** — provides a basic endpoint for application health checks.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | Web framework and REST API |
| PostgreSQL | Relational database |
| Psycopg | PostgreSQL connectivity |
| Pydantic | Request validation |
| Jinja2 | HTML templating |
| HTML & CSS | User interface |
| Uvicorn | ASGI application server |
| Git & GitHub | Version control and source hosting |

## How It Works

1. A user submits a URL through the web interface.
2. FastAPI validates the submitted URL.
3. The backend generates a unique short code.
4. The original URL and short code are stored in PostgreSQL.
5. LinkSnap returns a short URL.
6. When someone visits that short URL, the backend looks up the destination and redirects the visitor.

## Architecture

```text
User's Browser
      |
      v
HTML / CSS Interface
      |
      v
FastAPI Application
      |
      +---- URL validation
      |
      +---- Short-code generation
      |
      v
PostgreSQL Database
      |
      v
Short-code lookup
      |
      v
HTTP Redirect to Original URL
```

## Getting Started

### Prerequisites

Install the following before running the project:

- Python 3.10 or newer
- PostgreSQL
- Git
- A terminal such as PowerShell

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd url-shortener
```

Replace the placeholder with your actual GitHub repository URL after publishing the project.

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks environment activation, you can run the environment's Python executable directly instead.

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=url_shortener
DB_USER=postgres
DB_PASSWORD=your_local_database_password
```

Change the values to match your PostgreSQL configuration. The example port is PostgreSQL's common default; your local installation may use a different port.

**Security:** Never commit `.env` or share real database credentials. In production, configure secrets through your hosting provider's environment settings.

### 5. Create the database

Create a PostgreSQL database named `url_shortener`, then run the following SQL against that database:

```sql
CREATE TABLE links (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    short_code VARCHAR(6) NOT NULL UNIQUE,
    original_url TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### 6. Start the application

From the project root:

```powershell
python -m uvicorn app.main:app --reload
```

Open these addresses in your browser:

- Web interface: http://127.0.0.1:8000/
- API documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

The development server is intended for local development, not production hosting.

## API Reference

### `GET /`

Returns the LinkSnap web interface.

### `GET /health`

Returns a basic health response.

Example:

```json
{
  "status": "ok"
}
```

### `POST /test-url`

Validates a submitted URL and returns it without creating a short link.

Request:

```json
{
  "url": "https://www.example.com"
}
```

### `POST /links`

Creates a short link and stores it in PostgreSQL.

Request:

```json
{
  "url": "https://www.example.com"
}
```

Example response:

```json
{
  "id": 1,
  "short_code": "aB12xZ",
  "short_url": "http://127.0.0.1:8000/aB12xZ",
  "original_url": "https://www.example.com/"
}
```

The example short code and response values are illustrative. The actual code is generated dynamically. The displayed URL uses the local development address until production URL configuration is added.

### `GET /{short_code}`

Looks up the short code and redirects to its destination. If the code does not exist, the API returns a `404 Not Found` response.

## Database Schema

The `links` table stores the application's URL mappings.

| Column | Description |
|---|---|
| `id` | Unique database identifier |
| `short_code` | Unique six-character short code |
| `original_url` | Original destination URL |
| `created_at` | Timestamp when the link was created |

The unique constraint on `short_code` prevents duplicate codes from being stored.

## Project Structure

```text
url-shortener/
├── app/
│   ├── main.py
│   ├── db.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── style.css
├── tests/
├── .env                 # Local secrets; do not commit
├── .gitignore
├── requirements.txt
└── README.md
```

## Security and Production Considerations

Before production deployment, the project will need additional configuration and hardening:

- Store credentials in environment variables or a managed secrets service.
- Configure a production base URL instead of returning localhost links.
- Use HTTPS for the public application.
- Add rate limiting and abuse prevention.
- Consider protections against malicious destinations and phishing abuse.
- Add automated tests for link creation, redirects, invalid input, and missing codes.
- Configure production database migrations and backups.
- Use a production ASGI server configuration and appropriate logging.

## Roadmap

- [ ] Publish the source code on GitHub.
- [ ] Add automated tests with `pytest`.
- [ ] Add configurable public URL generation.
- [ ] Deploy the application to a public hosting provider.
- [ ] Configure a production PostgreSQL database.
- [ ] Add custom aliases and configurable expiration.
- [ ] Add click analytics and link management.
- [ ] Improve deployment documentation and screenshots.

## Learning Goals

This project is an opportunity to practice:

- Designing REST APIs with FastAPI.
- Working with PostgreSQL and SQL constraints.
- Managing configuration and secrets safely.
- Building a simple frontend for a Python backend.
- Testing, version control, and production deployment.

## License

A license has not been selected yet. Add a `LICENSE` file before describing this project as open source.
