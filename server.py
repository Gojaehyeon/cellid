"""
Cellid — lid-as-bow cello server.

- ws://localhost:8765    Lid angle broadcast (50ms tick)
- http://localhost:8088  Static files (index.html, ...)

Sensor polling runs on a dedicated thread so asyncio never blocks on
hidapi I/O.

Run:
    python3 -m venv venv && source venv/bin/activate
    pip install websockets pybooklid hidapi
    python server.py
"""

import asyncio
import json
import os
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

import websockets
from pybooklid import LidSensor

clients = set()
latest_angle = None


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return


def http_thread():
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(here)
    httpd = ThreadingHTTPServer(('localhost', 8088), Handler)
    print(f"HTTP serving {here} on http://localhost:8088", flush=True)
    httpd.serve_forever()


def sensor_thread():
    global latest_angle
    with LidSensor() as sensor:
        for angle in sensor.monitor(interval=0.05):
            latest_angle = angle


async def broadcaster():
    while True:
        try:
            if latest_angle is not None and clients:
                msg = json.dumps({"angle": latest_angle})
                stale = []
                for ws in list(clients):
                    try:
                        await ws.send(msg)
                    except (websockets.ConnectionClosed, Exception):
                        stale.append(ws)
                for ws in stale:
                    clients.discard(ws)
        except Exception as e:
            print(f"broadcaster err: {e}", flush=True)
        await asyncio.sleep(0.05)


async def handler(websocket):
    clients.add(websocket)
    print(f"WS client connected. total={len(clients)}", flush=True)
    try:
        await websocket.wait_closed()
    finally:
        clients.discard(websocket)
        print(f"WS client disconnected. total={len(clients)}", flush=True)


async def main():
    threading.Thread(target=sensor_thread, daemon=True).start()
    threading.Thread(target=http_thread, daemon=True).start()
    asyncio.create_task(broadcaster())
    async with websockets.serve(handler, "localhost", 8765):
        print("WS bridge listening on ws://localhost:8765", flush=True)
        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped.", flush=True)
