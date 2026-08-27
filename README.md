# GameMate API

A REST API for connecting gamers around the games they play. Users can create profiles, add games to their library, publish **Looking For Group (LFG)** posts, and manage requests to join a group.

Built with FastAPI, SQLAlchemy, PostgreSQL, and Pydantic.

## Features

- Create and browse gamer profiles
- Create and browse games
- Associate games with a user's profile
- Create and filter LFG posts by game
- Submit join requests to LFG posts
- View and accept or reject join requests
- Returns appropriate errors for missing resources, duplicate game assignments, duplicate join requests, and self-join attempts

## Tech stack

- Python 3
- FastAPI
- SQLAlchemy 2
- PostgreSQL (via Psycopg 3)
- Pydantic 2
- Uvicorn

## Project structure

```text
.
├── main.py             # FastAPI application and router registration
├── database.py         # PostgreSQL engine and database-session dependency
├── models.py           # SQLAlchemy ORM models
├── schemas.py          # Pydantic request/response schemas
├── routers/            # API route definitions
├── crud/               # Reusable database lookup helpers
└── requirements.txt    # Python dependencies
```

## Getting started

### Prerequisites

- Python 3.10 or later
- A running PostgreSQL instance

### Installation

1. Clone the repository and enter it.

   ```bash
   git clone <your-repository-url>
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

4. Create a `config.json` file in the project root. This file is ignored by Git, so credentials stay local.

   ```json
   {
     "username": "postgres",
     "password": "your-password",
     "host": "localhost",
     "database": "gamemate"
   }
   ```

5. Create the PostgreSQL database named in `config.json`, then create the tables from the ORM models. The current application does not run migrations or create tables automatically.

   ```bash
   python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"
   ```

6. Start the development server.

   ```bash
   uvicorn main:app --reload
   ```

The API is then available at `http://127.0.0.1:8000`. Interactive documentation is available at `/docs`, and the OpenAPI schema at `/openapi.json`.

## API overview

| Area | Method | Endpoint | Description |
| --- | --- | --- | --- |
| Health | `GET` | `/` | Confirms that the API is running. |
| Users | `POST` | `/users` | Create a gamer profile. |
| Users | `GET` | `/users` | List gamer profiles. |
| Users | `GET` | `/users/{usr_id}` | Get one gamer profile. |
| User games | `POST` | `/users/{usr_id}/games/{game_id}` | Add a game to a user's library. |
| Games | `POST` | `/games/games` | Create a game. |
| Games | `GET` | `/games/games` | List games. |
| Games | `GET` | `/games/games/{game_id}` | Get one game. |
| LFG posts | `POST` | `/lfg` | Create an LFG post. |
| LFG posts | `GET` | `/lfg` | List LFG posts; filter with `?game_id={game_id}`. |
| LFG posts | `GET` | `/lfg/{post_id}` | Get one LFG post. |
| Join requests | `POST` | `/lfg/{post_id}/join?usr_id={user_id}` | Request to join an LFG post. |
| Join requests | `GET` | `/lfg/{post_id}/requests` | List requests for an LFG post. |
| Join requests | `PATCH` | `/lfg/{post_id}/requests/{user_id}` | Accept or reject a pending request. |

> The repeated `/games/games` path is the route exposed by the current build: the games router uses the `/games` prefix and its endpoints also specify `/games`.

## Example workflow

Create a user:

```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ari",
    "age": 24,
    "email": "ari@example.com",
    "country": "India"
  }'
```

Create a game:

```bash
curl -X POST http://127.0.0.1:8000/games/games \
  -H "Content-Type: application/json" \
  -d '{"name": "Valorant"}'
```

Add the game to the user's profile:

```bash
curl -X POST http://127.0.0.1:8000/users/1/games/1
```

Create an LFG post:

```bash
curl -X POST http://127.0.0.1:8000/lfg \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "game_id": 1,
    "title": "Ranked squad needed",
    "players_needed": 2,
    "message": "Looking for relaxed teammates for evening games."
  }'
```

Approve a join request:

```bash
curl -X PATCH http://127.0.0.1:8000/lfg/1/requests/2 \
  -H "Content-Type: application/json" \
  -d '{"status": "accepted"}'
```

## Data model

- **User**: name, age, email, and country
- **Game**: game name
- **UserGame**: many-to-many relationship between users and games
- **LFG Post**: author, game, title, players needed, and optional message
- **Join Request**: a user's request to join an LFG post, with `pending`, `accepted`, or `rejected` status

## Current scope

This is a backend API project. It currently has no authentication/authorization, migrations, automated tests, or frontend client. These are natural next steps for production use.

## License

No license has been specified yet. Add one before distributing or accepting outside contributions.

