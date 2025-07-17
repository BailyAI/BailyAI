from flask import Flask
from threading import Thread
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return "Baily Bot is alive 💖", 200

@app.route('/health')
def health():
    return {"status": "healthy", "bot": "Baily Bot"}, 200

def run():
    """Run the Flask app"""
    try:
        app.run(host='0.0.0.0', port=8080, debug=False)
    except Exception as e:
        logger.error(f"Flask server error: {e}")

def keep_alive():
    """Start Flask server in a separate thread"""
    logger.info("Starting Flask keep-alive server on port 8080")
    t = Thread(target=run)
    t.daemon = True
    t.start()
    logger.info("Flask keep-alive server started successfully")