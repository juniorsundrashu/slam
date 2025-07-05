import sys
import os
import tempfile
import zipfile

def extract_and_run():
    zip_path = os.path.join(sys._MEIPASS, "source.zip")  # bundled via PyInstaller
    extract_dir = os.path.join(tempfile.gettempdir(), "slam_src")

    if not os.path.exists(os.path.join(extract_dir, "bot")):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

    sys.path.insert(0, extract_dir)

    from bot import LOGGER, bot_loop
    LOGGER.info("Starting Slam Mirror Bot from extracted zip...")
    bot_loop()

if __name__ == "__main__":
    extract_and_run()
