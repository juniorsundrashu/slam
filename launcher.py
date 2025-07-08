import sys
import os
import tempfile
import zipfile
import shutil
import platform
import logging

def extract_and_run():
    try:
        base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
        zip_path = os.path.join(base_path, "source.zip")
        extract_dir = os.path.join(tempfile.gettempdir(), "slam_src")

        if not os.path.exists(os.path.join(extract_dir, "bot")):
            if os.path.exists(extract_dir):
                shutil.rmtree(extract_dir)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

        sys.path.insert(0, extract_dir)

        # Cross-platform folder creation
        os.makedirs("qBittorrent/config", exist_ok=True)

        # Optional: Windows-specific logic
        if platform.system() == "Windows":
            logging.info("Adjusting settings for Windows...")
            # Add any Windows-specific tweaks here

        from bot import LOGGER, bot_loop
        LOGGER.info("Starting Slam Mirror Bot from extracted zip...")
        bot_loop()

    except Exception as e:
        print(f"[FATAL] Failed to launch: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    extract_and_run()
