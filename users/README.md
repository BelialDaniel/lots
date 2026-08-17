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
