# FastAPI WebSocket Server

A simple **FastAPI** server with WebSocket support for real-time communication and a **graceful shutdown** mechanism.  
The server waits until all clients disconnect or forces shutdown after a timeout (default: 30 minutes).

---

## Project Structure

```
fastapi-websocket/
├── app/
│   ├── core/                # infrastructure (settings, logging, lifecycle)
│   │   ├── lifespan/        # startup / shutdown logic
│   │   │   ├── base.py
│   │   │   ├── startup.py
│   │   │   ├── shutdown.py
│   │   └── settings.py      # constants (timeouts, intervals)
│   │   └── logging.py
│   ├── endpoints/           # HTTP and WebSocket routes
│   │   ├── http.py
│   │   ├── websocket.py
│   ├── templates/           # HTML client for WebSocket testing
│   │   └── index.html
│   └── websockets/          # WebSocket logic
│       ├── manager.py       # ConnectionManager (add/remove clients)
│       ├── notifier.py      # periodic notifications
│       └── shutdown.py      # GracefulShutdown
├── main.py                  # entry point (uvicorn main:app)
├── pyproject.toml / poetry.lock
├── Makefile                 # utility commands
└── .gitignore
```

---

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourname/fastapi-websocket.git
cd fastapi-websocket
```

2. Install dependencies via **Poetry**:

```bash
poetry install
```

3. Ensure Uvicorn with WebSocket support is installed:

```bash
pip install "uvicorn[standard]"
```

---

## Running the Server

```bash
uvicorn main:app --reload
```

or (via Makefile):

```bash
make run
```

By default, the server runs at:  
👉 `http://127.0.0.1:8000`

---

## WebSocket Testing

1. Open the test client in a browser:

```
http://127.0.0.1:8000
```

2. Use the **Send Hello** button to send a message.  
3. Broadcast messages will appear in the browser console (every 10 seconds or on shutdown).

---

## Graceful Shutdown

- When receiving `CTRL+C` or `SIGTERM`:  
  - the server **waits** until all clients disconnect,  
  - or **forcefully closes** them after `SHUTDOWN_TIMEOUT` (default: 30 minutes).  

- Logic:
  1. Waits for all clients to disconnect.  
  2. If timeout expires — executes `close_all()`.  

---

## Configuration

Configuration is stored in `app/core/settings.py`:

```python
# Interval between notifications (seconds)
NOTIFICATION_INTERVAL = 10

# Graceful shutdown timeout (seconds)
SHUTDOWN_TIMEOUT = 30 * 60
```

You can also move these values into `.env` and load them via Pydantic Settings.

---

## How to Test Graceful Shutdown

1. Run the server.  
2. Open multiple browser tabs with the WebSocket client.  
3. Press `CTRL+C` in the terminal.  
4. The server sends a shutdown notice and waits:  
   - if clients disconnect → server exits immediately;  
   - if clients stay → server waits `SHUTDOWN_TIMEOUT` then forcefully closes.  

--- 