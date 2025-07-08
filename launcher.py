import sys
import os
import tempfile
import zipfile
import subprocess

# 🛡️ Patch subprocess to replace 'python'/'python3' with sys.executable
_original_popen = subprocess.Popen
_original_run = subprocess.run

def patch_python_calls(cmd, *args, **kwargs):
    if isinstance(cmd, list) and cmd:
        if cmd[0] in ("python", "python3"):
            cmd[0] = sys.executable
    elif isinstance(cmd, str):
        if cmd.startswith("python "):
            cmd = cmd.replace("python", sys.executable, 1)
        elif cmd.startswith("python3 "):
            cmd = cmd.replace("python3", sys.executable, 1)
    return cmd, args, kwargs

def patched_popen(cmd, *args, **kwargs):
    cmd, args, kwargs = patch_python_calls(cmd, *args, **kwargs)
    return _original_popen(cmd, *args, **kwargs)

def patched_run(cmd, *args, **kwargs):
    cmd, args, kwargs = patch_python_calls(cmd, *args, **kwargs)
    return _original_run(cmd, *args, **kwargs)

# Apply the monkey patches
subprocess.Popen = patched_popen
subprocess.run = patched_run

def extract_and_run():
    zip_path = os.path.join(sys._MEIPASS, "source.zip")  # bundled via PyInstaller
    extract_dir = os.path.join(tempfile.gettempdir(), "slam_src")

    if not os.path.exists(os.path.join(extract_dir, "bot")):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

    sys.path.insert(0, extract_dir)
    os.chdir(extract_dir)

    from bot import LOGGER, bot_loop
    LOGGER.info("Starting Slam Mirror Bot from extracted zip...")
    bot_loop()

if __name__ == "__main__":
    extract_and_run()
