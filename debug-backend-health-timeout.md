# Debug Session: backend-health-timeout

Status: OPEN

## Symptom

- Browser cannot access `http://localhost:8000/health`.
- Previous `/auth/send-code` request stayed pending or timed out.

## Hypotheses

1. The FastAPI backend is not actually running on port `8000`.
2. Port `8000` is occupied by a stale or non-HTTP process.
3. Backend startup fails because `backend/app/routers/projects.py` contains accidentally pasted SQL.
4. Backend starts from the wrong working directory or module path.
5. The browser preview/proxy layer is showing a stale page while the local service is unavailable.

## Evidence Log

- `uvicorn` startup log showed `SyntaxError` in `backend/app/routers/projects.py` at the accidentally pasted SQL line.
- Removed the pasted SQL and restored the import closing parenthesis.
- `python3 -m py_compile backend/app/routers/projects.py` passed.
- `curl -i --max-time 5 http://127.0.0.1:8000/health` returned `HTTP/1.1 200 OK` with FastAPI health JSON.

## Next Steps

- Ask user to verify via `http://127.0.0.1:8000/health`.
- If browser still fails on `localhost`, use `127.0.0.1` for local verification and restart frontend.
