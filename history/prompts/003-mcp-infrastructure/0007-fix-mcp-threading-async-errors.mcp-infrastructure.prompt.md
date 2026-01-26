---
id: 7
title: Fix MCP Threading Async Runtime Errors
stage: refactor
date: 2026-01-26
surface: agent
model: claude-haiku-4-5-20251001
feature: mcp-infrastructure
branch: 003-mcp-infrastructure
user: Claude Haiku 4.5
command: null
labels: [mcp, threading, async, runtime-error, fixes, refactoring]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - C:\Projects\todo-full-stack-III\backend\src\services\mcp_server.py
  - C:\Projects\todo-full-stack-III\backend\main.py
tests:
  - C:\Projects\todo-full-stack-III\backend\tests\test_mcp.py
---

## Prompt

Resolve MCP server threading and async runtime errors by implementing the following fixes:
1. Removed incorrect host/port parameters from mcp.run() calls
2. Fixed the threading approach to properly handle the async MCP server
3. Corrected the async runtime issues that caused "Already running asyncio in this thread" error
4. Ensured the MCP server runs properly in a background thread without blocking the main application

## Response snapshot

This PHR documents the critical fixes made to resolve MCP server threading and async runtime errors in the todo-full-stack application. The changes enable the MCP (Model Context Protocol) server to run reliably in a background thread alongside the main FastAPI application.

Key changes made:

1. **Removed incorrect host/port parameters from mcp.run() calls**: The original implementation was passing host and port parameters to `mcp.run()` which is incorrect for FastMCP. FastMCP handles its own internal configuration and doesn't accept host/port parameters like traditional HTTP servers. The fix changed:
   ```python
   # Before (incorrect):
   mcp.run(host="localhost", port=8001)

   # After (correct):
   mcp.run()
   ```

2. **Fixed the threading approach to properly handle the async MCP server**: Implemented a proper threading pattern that isolates the MCP server in a dedicated daemon thread, preventing interference with the main FastAPI event loop. The implementation now uses:
   ```python
   def start_mcp_server():
       def run_server():
           # Run MCP server directly - FastMCP handles async internally
           mcp.run()

       # Create a daemon thread to run the MCP server
       server_thread = threading.Thread(target=run_server, daemon=True)
       server_thread.start()
       return server_thread
   ```

3. **Corrected async runtime issues causing "Already running asyncio in this thread" error**: The error occurred because both FastAPI (via Uvicorn) and the MCP server were trying to run asyncio event loops in the same thread. The solution was to ensure the MCP server runs in a separate thread where it can manage its own async context without conflicting with the main application's event loop.

4. **Ensured MCP server runs properly in background without blocking**: The MCP server is now started in a daemon thread during the FastAPI startup event, allowing it to run independently without interfering with the main application lifecycle. This approach ensures:
   - The MCP server doesn't block the main application startup
   - Both servers can coexist without async conflicts
   - Proper cleanup when the main application terminates
   - Non-blocking operation for both services

Integration with main.py:
```python
@app.on_event("startup")
async def on_startup():
    create_db_and_tables()
    # Start MCP server in a background thread
    start_mcp_server()
```

These changes resolve the threading and async runtime errors that were preventing the MCP server from operating correctly alongside the main FastAPI application. The solution maintains separation of concerns between the HTTP API server and the MCP server while ensuring both can operate reliably in the same process.

## Outcome

- ✅ Impact: Resolved MCP server threading and async runtime errors, enabling stable coexistence of FastAPI and MCP servers
- 🧪 Tests: MCP integration tests pass, both servers operate without conflicts
- 📁 Files: 2 core files modified to fix threading and async runtime issues
- 🔁 Next prompts: Deploy MCP-enabled backend and test AI agent integrations
- 🧠 Reflection: Proper thread isolation is essential when running multiple async servers in the same process

## Evaluation notes (flywheel)

- Failure modes observed: "Already running asyncio in this thread" error, blocking main application startup
- Graders run and results (PASS/FAIL): PASS - both servers now operate without async conflicts
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Test MCP server under load with concurrent requests