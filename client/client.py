import asyncio
import websockets
import subprocess
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
MSOFF_PATH = os.path.join(project_root, "build", "msoff.exe")

async def connect_to_server(uri):
    while True:
        try:
            print(f"Mencoba menghubungkan ke {uri}...")
            async with websockets.connect(uri) as websocket:
                print("Berhasil terhubung ke host server!")
                async for message in websocket:
                    print(f"Menerima: {message}")
                    if message == "set off":
                        subprocess.run([MSOFF_PATH, "display", "off"])
                    elif message == "set on":
                        subprocess.run([MSOFF_PATH, "display", "on"])
        except (websockets.exceptions.ConnectionClosed, ConnectionRefusedError, OSError):
            print("Koneksi terputus. Menghubungkan ulang...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    ip = input("Masukkan IP Address host: ").strip()
    if not ip:
        sys.exit(1)
        
    uri = f"ws://{ip}:8765/monitor"
    
    try:
        asyncio.run(connect_to_server(uri))
    except KeyboardInterrupt:
        pass
