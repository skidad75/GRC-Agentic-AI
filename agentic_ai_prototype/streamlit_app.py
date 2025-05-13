import os
import sys
import streamlit as st

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import *

# The rest of the app will be imported from main.py 