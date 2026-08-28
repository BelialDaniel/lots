# Lots

A minimalist lot-management platform. Each concern lives in its own microservice, and each service uses a different stack on purpose — a small, polyglot setup rather than a single monolith.

The goal is to manage real-estate lots (and the people around them) with a thin API gateway, isolated databases, and room to grow a resources domain later.

## Architecture

```
UI (React) ──► Nginx gateway (:8080)
                    ├── /api/v1/auth      → auth-service     (Node.js)
                    ├── /api/v1/users     → users-service    (Python)
                    └── /api/v1/resources → resources-service (planned)
```

Nginx is the only public API entry point. Protected routes ask the auth service to verify the JWT before the request is forwarded.

| Service | Role | Stack |
| --- | --- | --- |
| **auth** | Register, login, JWT cookies, token verification | Node.js, Express, TypeScript, Drizzle, Argon2 |
| **users** | User and profile data | Python, FastAPI, SQLModel, Alembic |
| **ui** | Web client | React 19, React Router 8, Vite, Tailwind |
| **api-gateway** | Routing and JWT gate | Nginx |
| **db** | One Postgres instance, one database per service | PostgreSQL 17 + pgvector |
| **rabbitmq** | Async messaging between services | RabbitMQ |
| **resources** | Lots, styles, plans *(not running yet)* | — |

Each service owns its own logical database (`auth`, `users`, `resources`) created on first Postgres boot.

## Run locally

Copy `.env` if you do not already have one, then:

```bash
docker compose up --build
```

| What | URL |
| --- | --- |
| UI | http://localhost:5173 |
| API gateway | http://localhost:8080 (also `http://<slug>.localhost:8080`) |
| Auth service (direct) | http://localhost:8001 |
| Users service (direct) | http://localhost:8002 |
| RabbitMQ management | http://localhost:15672 |

Gateway paths:

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/verify` — sets `X-User-Id` only (identity). No tenant in the JWT.
- `/api/v1/users/` (JWT required; `X-Tenant-Slug` from Host, e.g. `acme.localhost:8080`)
- `/api/v1/users/docs` and `/api/v1/users/openapi.json` (public)

Identity vs tenant headers (the UI must not send these):

| Header | Set by | When |
| --- | --- | --- |
| `X-User-Id` | Gateway ← `auth` `/verify` | Now |
| `X-Tenant-Slug` | Gateway ← `Host` | Now |
| `X-Developer-Id` | Gateway ← `users` lookup | Etapa 4 |
| `X-User-Role` | Gateway ← `users` lookup (`developer` \| `builder`) | Etapa 4 |

## Migrations

Auth (Drizzle):

```bash
docker exec -it auth-service pnpm db:generate
docker exec -it auth-service pnpm db:migrate
```

Users (Alembic):

```bash
docker exec -it users-service uv run python -m alembic revision --autogenerate -m "describe the change"
docker exec -it users-service uv run python -m alembic upgrade head
```

## Repository layout

```
auth/          Node.js auth service
users/         Python users service
ui/            React frontend
infra/         Nginx gateway config
sql/           Postgres bootstrap (creates per-service databases)
scripts/       Helper scripts per service
```
