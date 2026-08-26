# Users

Person, developer tenant (`slug`), and builder memberships. Role is **per tenant**, not a global flag.

Protected routes expect `X-User-Id` from the gateway. The UI never sends identity or tenant headers.

The gateway does **not** call `auth` `/verify` itself. One `auth_request` hits `GET /api/v1/users/internal/access`, which calls `auth` on the Docker network and then checks owner/membership when `X-Tenant-Slug` is present.

## Gateway headers

| Header | Who sets it | This service |
| --- | --- | --- |
| `X-User-Id` | Gateway, from `/internal/access` | Reads it on business routes (`api/headers.py` → `USER_ID`). `/internal/access` sets it after `auth` `/verify`. |
| `X-Tenant-Slug` | Gateway, from `Host` | `/internal/access` reads it. Empty (`app.localhost`) = JWT only, no membership. |
| `X-Developer-Id` | Gateway, from `/internal/access` | Set when the user is owner or member of that slug |
| `X-User-Role` | Gateway, from `/internal/access` (`developer` \| `builder`) | Same |

Names are locked in `api/headers.py`. Do not invent `X-Owner-Id`. The JWT never carries `developer_id`.

`GET /internal/tenants/{slug}` remains for internal lookup (404 if the slug does not exist). It is **not** the Nginx `auth_request`. `/internal/access` returns **403** for a missing slug (Nginx would turn 404 into 500).

Internal HTTP to auth: `AUTH_VERIFY_URL` (default `http://auth-service:8000/api/v1/auth/verify`).

## Migrations

```bash
# 1. Generate a new migration (auto-detects model changes)
docker exec -it users-service uv run python -m alembic revision --autogenerate -m "description of changes"

# 2. Apply all pending migrations
docker exec -it users-service uv run python -m alembic upgrade head

# 3. Rollback last migration
docker exec -it users-service uv run python -m alembic downgrade -1

# 4. Show current migration version
docker exec -it users-service uv run python -m alembic current

# 5. Show migration history
docker exec -it users-service uv run python -m alembic history
```
