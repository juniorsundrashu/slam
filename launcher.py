import os
import sys
import zipfile
import platform
import tempfile
import shutil
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("Launcher")

IS_WINDOWS = platform.system() == "Windows"

def safe_mkdir(path):
    try:
        os.makedirs(path, exist_ok=True)
        LOGGER.info(f"Created directory: {path}")
    except Exception as e:
        LOGGER.error(f"Failed to create directory {path}: {e}")

def safe_copy(src, dst):
    try:
        shutil.copy(src, dst)
        LOGGER.info(f"Copied file: {src} → {dst}")
    except Exception as e:
        LOGGER.error(f"Failed to copy file from {src} to {dst}: {e}")

def safe_unzip(zip_path, extract_to="."):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            LOGGER.info(f"Extracted {zip_path} to {extract_to}")
    except Exception as e:
        LOGGER.error(f"Failed to unzip {zip_path}: {e}")

def start_bundled_bot():
    # Detect bundle path from PyInstaller
    bundle_dir = getattr(sys, '_MEIPASS', None)
    if not bundle_dir:
        LOGGER.error("This script must be run as a bundled EXE (PyInstaller).")
        sys.exit(1)

    zip_path = os.path.join(bundle_dir, "source.zip")
    extract_dir = os.path.join(tempfile.gettempdir(), "slam_src")

    if not os.path.exists(os.path.join(extract_dir, "bot")):
        LOGGER.info("Extracting source.zip...")
        safe_unzip(zip_path, extract_dir)

    sys.path.insert(0, extract_dir)

    # Pre-boot logic: create required folders/files
    qb_config_dir = os.path.join(extract_dir, "qBittorrent", "config")
    safe_mkdir(qb_config_dir)

    qb_conf_source = os.path.join(extract_dir, "qBittorrent.conf")
    qb_conf_dest = os.path.join(qb_config_dir, "qBittorrent.conf")
    if os.path.exists(qb_conf_source):
        safe_copy(qb_conf_source, qb_conf_dest)

    # Boot bot
    try:
        from bot import LOGGER as BOT_LOGGER, bot_loop
        BOT_LOGGER.info("🚀 Starting Slam Mirror Bot from extracted zip...")
        bot_loop()
    except Exception as e:
        LOGGER.error(f"Failed to start bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_bundled_bot()
