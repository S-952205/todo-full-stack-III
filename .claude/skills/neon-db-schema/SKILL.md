---
name: neon-db-schema-skill
description: Use when designing database tables or SQLModel classes to ensure data integrity and performance in Neon.
---

# Neon DB Schema Skill

## Instructions
1. **Ownership**: Every table (like Tasks) MUST have a `user_id` foreign key.
2. **Index Optimization**: Add database indexes on `user_id` and `id` for high-speed lookups.
3. **Default Values**: Set `completed` status to `False` by default and auto-generate timestamps.
4. **Neon Connection**: Use the optimized connection string with `-pooler` suffix for serverless scalability.

## Examples
- **Model**: `user_id: str = Field(foreign_key="user.id", index=True)`
- **SQLModel**: `class Task(SQLModel, table=True): title: str = Field(index=True)`