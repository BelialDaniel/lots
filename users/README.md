# Users

Person, developer tenant (`slug`), and builder memberships. Role is **per tenant**, not a global flag.

Protected routes expect `X-User-Id` from the gateway. The UI never sends identity or tenant headers.

## Gateway headers

| Header | Who sets it | This service |
| --- | --- | --- |
| `X-User-Id` | Gateway, from `auth` `/verify` | Reads it (`api/headers.py` → `USER_ID`) |
| `X-Tenant-Slug` | Gateway, from `Host` (etapa 3) | Lookup: `GET /api/v1/users/internal/tenants/{slug}` |
| `X-Developer-Id` | Gateway after that lookup (etapa 4) | Returns `developer_id` in the lookup body; does not set the header yet |
| `X-User-Role` | Gateway after that lookup (`developer` \| `builder`) | Returns `TenantRole`; does not set the header yet |

Names are locked in `api/headers.py`. Do not invent `X-Owner-Id`. The JWT never carries `developer_id`.

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
