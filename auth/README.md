# Auth

Identity service: credentials, JWT cookie, and `/verify`. The token is **who** the user is (`sub`, `email`). It does **not** carry `developer_id` or a role — a builder can belong to several developers.

`GET /api/v1/auth/verify` only sets `X-User-Id` from `sub`. The gateway copies that header onto protected routes. The UI never sends identity or tenant headers.

## Gateway headers

| Header | Who sets it | This service |
| --- | --- | --- |
| `X-User-Id` | Gateway, from `/verify` | **Yes** — the only header `/verify` emits |
| `X-Tenant-Slug` | Gateway, from `Host` | No |
| `X-Developer-Id` | Gateway after `users` lookup (etapa 4) | No |
| `X-User-Role` | Gateway after `users` lookup (`developer` \| `builder`) | No |

Do not add `X-Owner-Id` or put tenant claims in the JWT.

## Migrations

```bash
# 1. Generate a new migration (auto-detects schema changes)
docker exec -it auth-service pnpm db:generate

# 2. Apply all pending migrations
docker exec -it auth-service pnpm db:migrate

# 3. Open Drizzle Studio
docker exec -it auth-service pnpm db:studio
```
