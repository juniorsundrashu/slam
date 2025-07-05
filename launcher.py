import runpy
import os
import sys

# Ensure 'bot' folder is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Run the bot.main module
runpy.run_module("bot.main", run_name="__main__")
