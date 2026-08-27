import asyncio
import websockets
import socket
import logging

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

async def handler(websocket):
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
        async for message in websocket:
            pass 
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)
        logging.info(f"Client terputus: {client_ip}")

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
        elif cmd in ["set on", "set off"]:
            if connected_clients:
                websockets.broadcast(connected_clients, cmd)
                print(f"Command '{cmd}' berhasil dikirim.")
            else:
                print("Belum ada client terhubung.")
        else:
            print("Command tidak valid.")

async def main():
    host_ip = get_local_ip()
    port = 8765
    print(f"ws://{host_ip}:{port}/monitor")
    try:
        async with websockets.serve(handler, "0.0.0.0", port):
            await broadcast_commands()
    except Exception as e:
        pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
