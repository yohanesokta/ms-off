import asyncio
import websockets
import socket
import logging
import http

logging.basicConfig(level=logging.INFO)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

connected_clients = set()

async def broadcast_command(cmd: str):
    if connected_clients:
        await asyncio.gather(*(c.send(cmd) for c in connected_clients))

# WebSocket handler for /monitor connections
async def ws_handler(websocket):
    try:
        path = websocket.request.path
    except AttributeError:
        path = getattr(websocket, "path", "")
    if path != "/monitor":
        await websocket.close()
        return
    connected_clients.add(websocket)
    client_ip = websocket.remote_address[0]
    logging.info(f"Client terhubung dari {client_ip}")
    try:
        async for _ in websocket:
            pass
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)
        logging.info(f"Client terputus: {client_ip}")

# Simple HTTP server on port 80 to receive /off and /on via curl
async def http_handler(reader, writer):
    try:
        data = await reader.readline()
        if not data:
            writer.close()
            return
        request_line = data.decode().strip()
        method, path, _ = request_line.split()
        # Consume and ignore the rest of the headers
        while True:
            line = await reader.readline()
            if line in (b"\r\n", b"\n", b""):
                break
        if path == "/off":
            asyncio.create_task(broadcast_command("set off"))
            response = "HTTP/1.1 200 OK\r\nContent-Length: 12\r\n\r\noff triggered"
        elif path == "/on":
            asyncio.create_task(broadcast_command("set on"))
            response = "HTTP/1.1 200 OK\r\nContent-Length: 11\r\n\r\non triggered"
        else:
            response = "HTTP/1.1 404 Not Found\r\nContent-Length: 9\r\n\r\nNot Found"
        writer.write(response.encode())
        await writer.drain()
    except Exception as e:
        logging.error(f"HTTP handler error: {e}")
    finally:
        writer.close()

async def broadcast_commands():
    loop = asyncio.get_running_loop()
    print("\n--- Command Menu ---")
    print("set off")
    print("set on")
    print("exit\n")
    while True:
        cmd = await loop.run_in_executor(None, input, "Masukkan command: ")
        cmd = cmd.strip()
        if cmd == "exit":
            break
        if cmd in ["set on", "set off"]:
            if connected_clients:
                websockets.broadcast(connected_clients, cmd)
                print(f"Command '{cmd}' berhasil dikirim.")
            else:
                print("Belum ada client terhubung.")
        else:
            print("Command tidak valid.")

async def main():
    host_ip = get_local_ip()
    ws_port = 8765
    http_port = 80
    print(f"WebSocket listening on ws://{host_ip}:{ws_port}/monitor")
    print(f"HTTP trigger listening on http://{host_ip}:{http_port}/off or /on")
    async with websockets.serve(ws_handler, "0.0.0.0", ws_port):
        http_server = await asyncio.start_server(http_handler, "0.0.0.0", http_port)
        async with http_server:
            await broadcast_commands()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
