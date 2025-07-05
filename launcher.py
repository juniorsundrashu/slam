import os
import sys
import runpy

# Ensure current directory is the project root (where bot/ folder exists)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

# Add current directory to sys.path so "bot" can be imported
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# Launch the bot using bot/main.py
runpy.run_module("bot.main", run_name="__main__")
