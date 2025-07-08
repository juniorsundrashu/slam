import sys
import os
import tempfile
import zipfile
import subprocess
import time
import threading

def extract_source():
    zip_path = os.path.join(sys._MEIPASS, "source.zip")  # bundled via PyInstaller
    extract_dir = os.path.join(tempfile.gettempdir(), "slam_src")

    if not os.path.exists(os.path.join(extract_dir, "bot")):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

    sys.path.insert(0, extract_dir)
    os.chdir(extract_dir)
    return extract_dir

def run_alive():
    try:
        subprocess.Popen([sys.executable, "alive.py"])
    except Exception as e:
        print(f"[ALIVE] Failed to launch alive.py: {e}")

def run_web_server(port):
    try:
        cmd = f"gunicorn wserver:start_server --bind 0.0.0.0:{port} --worker-class aiohttp.GunicornWebWorker"
        subprocess.Popen(cmd, shell=True)
    except Exception as e:
        print(f"[WEB] Failed to start web server: {e}")

def setup_qbittorrent():
    try:
        os.makedirs("qBittorrent/config", exist_ok=True)
        subprocess.run(["cp", "qBittorrent.conf", "qBittorrent/config/qBittorrent.conf"], shell=True)
        subprocess.Popen(["qbittorrent-nox", "-d", "--profile=."], shell=True)
    except Exception as e:
        print(f"[QBIT] Setup failed: {e}")

def extract_and_run():
    extract_dir = extract_source()

    # ENV VAR fallback
    port = os.environ.get("PORT", "8080")

    # Run background services (web + alive + qBittorrent)
    threading.Thread(target=run_web_server, args=(port,), daemon=True).start()
    threading.Thread(target=run_alive, daemon=True).start()
    threading.Thread(target=setup_qbittorrent, daemon=True).start()

    # Delay for services to stabilize
    time.sleep(2)

    # Start main bot
    try:
        from bot import LOGGER, bot_loop
        LOGGER.info("Starting Slam Mirror Bot from launcher...")
        bot_loop()
    except Exception as e:
        print(f"[BOT] Fatal error in bot startup: {e}")

if __name__ == "__main__":
    extract_and_run()
