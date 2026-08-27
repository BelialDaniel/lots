# Auth

Identity service: credentials, JWT cookie, and `/verify`. The token is **who** the user is (`sub`, `email`). It does **not** carry `developer_id` or a role — a builder can belong to several developers.

Login sets an HttpOnly cookie. In local it is **host-only** (`acme.localhost`); `beta.localhost` does not receive it. Leave `COOKIE_DOMAIN` empty. In prod later: `COOKIE_DOMAIN=.lots.com` and `COOKIE_SECURE=true`.

`GET /api/v1/auth/verify` only sets `X-User-Id` from `sub`. The gateway no longer calls this as `auth_request`. `users` `/internal/access` calls it on the Docker network, then Nginx copies identity and tenant headers onto protected routes. The UI never sends identity or tenant headers.

## Gateway headers

| Header | Who sets it | This service |
| --- | --- | --- |
| `X-User-Id` | Gateway ← `users` `/internal/access` ← this `/verify` | **Yes** — the only header `/verify` emits |
| `X-Tenant-Slug` | Gateway, from `Host` | No |
| `X-Developer-Id` | Gateway ← `users` `/internal/access` | No |
| `X-User-Role` | Gateway ← `users` `/internal/access` (`developer` \| `builder`) | No |

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
