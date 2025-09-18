"""
AWS Elastic Beanstalk entry point for Vedic Astrology Calculator
"""
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from main import app

# For Elastic Beanstalk, the application should be named 'application'
application = app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(application, host="0.0.0.0", port=port)