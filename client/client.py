import asyncio
import websockets
import subprocess
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
MSOFF_PATH = os.path.join(project_root, "bin", "msoff.exe")


async def run_msoff(*args):
    """Jalankan msoff.exe di thread terpisah agar tidak memblokir event loop."""
    loop = asyncio.get_running_loop()
    try:
        result = await loop.run_in_executor(
            None,
            lambda: subprocess.run(
                [MSOFF_PATH, *args],
                capture_output=True,
                text=True
            )
        )
        if result.returncode != 0:
            print(f"[msoff] Gagal (kode {result.returncode}): {result.stderr.strip()}")
        else:
            print(f"[msoff] Sukses menjalankan: {' '.join(args)}")
    except FileNotFoundError:
        print(f"[msoff] File tidak ditemukan: {MSOFF_PATH}")
    except Exception as e:
        print(f"[msoff] Error saat menjalankan: {e}")


async def connect_to_server(uri):
    while True:
        try:
            print(f"Mencoba menghubungkan ke {uri}...")
            async with websockets.connect(
                uri,
                ping_interval=20,
                ping_timeout=20
            ) as websocket:
                print("Berhasil terhubung ke host server!")
                async for message in websocket:
                    print(f"Menerima: {message}")
                    if message == "set off":
                        asyncio.create_task(run_msoff("display", "off"))
                    elif message == "set on":
                        asyncio.create_task(run_msoff("display", "on"))
                    else:
                        print(f"Perintah tidak dikenali: {message}")

        except websockets.exceptions.ConnectionClosed:
            print("Koneksi ke server ditutup. Menghubungkan ulang dalam 5 detik...")
            await asyncio.sleep(5)
        except (ConnectionRefusedError, OSError) as e:
            print(f"Gagal terhubung ({e}). Mencoba lagi dalam 5 detik...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error tak terduga: {e}")
            await asyncio.sleep(5)


if __name__ == "__main__":
    ip = input("Masukkan IP Address host: ").strip()
    if not ip:
        print("IP tidak boleh kosong.")
        sys.exit(1)

    uri = f"ws://{ip}:8765/monitor"

    try:
        asyncio.run(connect_to_server(uri))
    except KeyboardInterrupt:
        print("\nProgram dihentikan.")