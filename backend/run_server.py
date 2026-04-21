#!/usr/bin/env python
"""Script to run the LANCHE MVP server with correct PYTHONPATH"""
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Now run uvicorn
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        access_log=True
    )
