#!/usr/bin/env bash
set -euo pipefail

# Usage:
# .env with DATABASE_URL set, or pass DATABASE_URL env var on command line
# Example: DATABASE_URL='postgresql://user:pass@host:5432/db' ./scripts/migrate.sh

echo "Running alembic migrations..."
alembic upgrade head
echo "Migrations applied."
