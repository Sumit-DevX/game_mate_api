# GameMate API

GameMate is a REST API for helping players find people to play with. It supports user accounts, game libraries, Looking For Group (LFG) posts, join requests, and JWT-based login.

It is built with FastAPI, SQLAlchemy, PostgreSQL, Pydantic, and Alembic.

## Features

- Create and browse gamer profiles
- Hash passwords when accounts are created
- Log in with an email and password to receive a JWT access token
- Verify a bearer token with a protected test endpoint
- Create and browse games
- Add games to a user's library
- Create and browse LFG posts, with optional game filtering
- Send, list, accept, and reject LFG join requests
- Return `404` errors for missing users, games, posts, and join requests
- Prevent self-join attempts and duplicate join requests

## Technology

- Python 3.10+
- FastAPI, SQLAlchemy 2, PostgreSQL (Psycopg 3), and Pydantic 2
- Alembic, `pwdlib`/Argon2, PyJWT, python-dotenv, and Uvicorn

## Project structure

```text
.
├── main.py                 # FastAPI app and router registration
├── database.py             # PostgreSQL engine and session dependency
├── models.py               # SQLAlchemy models and relationships
├── schemas.py              # Request and response models
├── routers/                # Authentication, users, games, and LFG routes
├── crud/                   # Database lookup helpers
├── utils/security.py       # Password hashing and JWT helpers
├── alembic/                # Migration environment and revisions
├── alembic.ini             # Alembic configuration
└── requirements.txt        # Python dependencies
```

## Setup

### Prerequisites

- Python 3.10 or newer
- A running PostgreSQL server and an application database

### Install and configure

1. Clone the repository and enter it.

   ```bash
   git clone <repository-url>
   cd game_mate_api
   ```

2. Create and activate a virtual environment.

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

4. Create `config.json` in the project root. It is Git-ignored and is read by both the application and Alembic.

   ```json
   {
     "username": "postgres",
     "password": "your-postgres-password",
     "host": "localhost",
     "database": "gamemate"
   }
   ```

5. Create a Git-ignored `.env` file for JWT signing.

   ```dotenv
   JWT_SECRET_KEY=replace-this-with-a-long-random-secret
   JWT_ALGORITHM=HS256
   ```

6. For a new database, create the tables from the current models.

   ```bash
   python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"
   ```

7. Start the development server.

   ```bash
   uvicorn main:app --reload
   ```

The interactive documentation is at `http://127.0.0.1:8000/docs`; the OpenAPI schema is at `/openapi.json`.

### Database migrations

Alembic is configured and the included revisions add `gamemate_user.password_hash` and then make it required. They apply only to an existing database that already has the original tables; they are not an initial-schema migration. For that older schema, back up the database and run:

```bash
alembic upgrade head
```

For a brand-new database, use step 6. Do not run the included password-column migration after creating tables from the current models, because the column already exists.

## API routes

| Area | Method | Endpoint | Description |
| --- | --- | --- | --- |
| Health | `GET` | `/` | Returns a running-status message. |
| Authentication | `POST` | `/auth/login` | Exchanges form credentials for a bearer token. |
| Authentication | `GET` | `/auth/test_auth` | Tests a valid bearer token. |
| Users | `POST` | `/users` | Creates a user account. |
| Users | `GET` | `/users` | Lists users. |
| Users | `GET` | `/users/{usr_id}` | Returns one user. |
| User games | `POST` | `/users/{usr_id}/games/{game_id}` | Adds a game to a user's library. |
| Games | `POST` | `/games/games` | Creates a game. |
| Games | `GET` | `/games/games` | Lists games. |
| Games | `GET` | `/games/games/{game_id}` | Returns one game. |
| LFG posts | `POST` | `/lfg` | Creates an LFG post. |
| LFG posts | `GET` | `/lfg` | Lists posts; accepts optional `?game_id={game_id}`. |
| LFG posts | `GET` | `/lfg/{post_id}` | Returns one post. |
| Join requests | `POST` | `/lfg/{post_id}/join?usr_id={user_id}` | Creates a pending request. |
| Join requests | `GET` | `/lfg/{post_id}/requests` | Lists a post's requests. |
| Join requests | `PATCH` | `/lfg/{post_id}/requests/{user_id}` | Accepts or rejects a pending request. |

> `/games/games` is the current path because the router prefix and endpoint path both include `/games`.

## Authentication

Create a user first, then send a form-encoded login request. OAuth2 calls the credential field `username`, but this API uses it for the user's email.

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=ari@example.com&password=strong-password"
```

The response contains an `access_token` and `token_type` (`bearer`). Tokens expire after 30 minutes. Test a token with:

```bash
curl http://127.0.0.1:8000/auth/test_auth \
  -H "Authorization: Bearer <access_token>"
```

Only `/auth/test_auth` currently requires authentication. The user, game, LFG, and join-request routes do not yet enforce ownership or authorization.

## Example workflow

Create a user:

```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ari",
    "age": 24,
    "email": "ari@example.com",
    "country": "India",
    "password": "strong-password"
  }'
```

Create a game, then add it to the user's library:

```bash
curl -X POST http://127.0.0.1:8000/games/games \
  -H "Content-Type: application/json" \
  -d '{"name": "Valorant"}'

curl -X POST http://127.0.0.1:8000/users/1/games/1
```

Create a join request:

```bash
curl -X POST "http://127.0.0.1:8000/lfg/1/join?usr_id=2"
```

Accept or reject it with `accepted` or `rejected`:

```bash
curl -X PATCH http://127.0.0.1:8000/lfg/1/requests/2 \
  -H "Content-Type: application/json" \
  -d '{"status": "accepted"}'
```

## Data model

- **User** — ID, name, age, email, country, and a password hash
- **Game** — ID and name
- **User_Games** — many-to-many link between users and games
- **LFG_Post** — author, game, title, players needed, and optional message
- **Join_Request** — LFG-post/user composite key and `pending`, `accepted`, or `rejected` status

## Current limitations

- `POST /lfg` currently fails before creating a post: it calls its user and game lookup helpers without passing the database session.
- Email addresses are not unique at either the database or route level.
- Most routes are public, including accepting or rejecting join requests.
- The schemas do not enforce constraints such as positive ages/player counts or string lengths.
- There is no automated test suite.
- Alembic's history does not include an initial-schema migration.

## License

No license has been specified. Add one before distributing the project or accepting external contributions.
