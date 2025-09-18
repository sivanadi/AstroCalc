#!/bin/bash

# Replit-optimized startup script
# Automatically binds to 0.0.0.0:5000 for Replit compatibility

uv run uvicorn main:app --host 0.0.0.0 --port 5000 --reload
