```bash
# 1. Generate a new migration (auto-detects schema changes)
docker exec -it auth-service pnpm db:generate

# 2. Apply all pending migrations
docker exec -it auth-service pnpm db:migrate

# 3. Open Drizzle Studio
docker exec -it auth-service pnpm db:studio
```
