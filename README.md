# AlgoGround ⚡
> In-Browser Computational Challenge Sandbox with Web Worker Isolation, Watchdog Supervision, and Practice State Synchronization.

AlgoGround is a lightweight, responsive developer practice environment featuring an interactive code editor, isolated background execution thread, parameter search synchronization, and automated test evaluation.

---

## Architecture Overview

```text
+-------------------------------------------------------------+
|                     AlgoGround Web Client                   |
|                                                             |
|  [ Catalog & Filtering ]       [ Code & SQL Sandbox ]       |
|  • Debounced search            • Multi-language editor      |
|  • Difficulty & topic tags     • Local progress cache       |
|  • URL query syncing           • Watchdog supervisor        |
+------------------------------+------------------------------+
                               |
                +--------------+--------------+
                |                             |
                v                             v
+-------------------------------+ +---------------------------+
|      FastAPI Microservice     | | Isolated Web Worker       |
| • GET  /api/v1/questions      | | • Dedicated background    |
| • POST /api/v1/submissions    | | • Sandboxed stdout capture|
| • GET  /api/v1/progress/{uid} | | • 2500ms watchdog limit   |
+-------------------------------+ +---------------------------+
```

---

## Technical Highlights

1. **Web Worker Sandboxing & Watchdog Supervisor**:
   - Algorithmic execution runs inside a dedicated browser Web Worker thread, keeping the primary UI responsive.
   - A 2500ms supervisory watchdog timer forcibly terminates worker threads if an infinite loop occurs, preventing client freeze.
   - Intercepts console logging cleanly to capture runtime diagnostics and standard output.

2. **Debounced Search & History State Sync**:
   - Synchronizes active search terms, difficulty levels, and active challenge identifiers directly to window URL parameters.

3. **Dual-Tier State Synchronization**:
   - Stores progress, streaks, and completion state locally via browser storage with fallback to FastAPI REST persistence.

4. **Multi-Platform Test Coverage**:
   - PyTest backend suite covering catalog retrieval, filter queries, solution evaluation, and progress calculation.

---

## Getting Started

### Local Setup

```bash
# 1. Run backend service
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# 2. Serve web client
cd ../frontend
python -m http.server 3000
```

Open `http://localhost:3000` in your web browser.

### Containerized Execution

```bash
docker-compose up --build
```

---

## Running Automated Tests

```bash
pytest tests/test_api.py -v
```

---

## License
MIT License - Open Source.
