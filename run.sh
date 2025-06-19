#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Run Streamlit application
streamlit run main.py --server.port=8501 