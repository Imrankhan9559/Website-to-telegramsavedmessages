import os
import logging
import asyncio
from pathlib import Path
from flask import Flask, request, render_template_string
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
MAX_SIZE_MB = 2048  # 2GB
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'webm'}

# Telegram credentials
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_dir = Path("telegram_session")
session_dir.mkdir(exist_ok=True)
session_path = str(session_dir / "session")

# Flask setup
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", os.urandom(24).hex())
app.config["MAX_CONTENT_LENGTH"] = MAX_SIZE_MB * 1024 * 1024

UPLOAD_FOLDER = Path("uploads").absolute()
UPLOAD_FOLDER.mkdir(exist_ok=True)

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Upload Video to Telegram</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .alert { padding: 15px; margin: 20px 0; border-radius: 4px; }
        .success { background-color: #dff0d8; color: #3c763d; }
        .error { background-color: #f2dede; color: #a94442; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Upload Video to Telegram Saved Messages</h2>
        
        {% if message %}
        <div class="alert {{ message_class }}">{{ message }}</div>
        {% endif %}
        
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="video" accept="video/*" required><br><br>
            <input type="submit" value="Upload">
        </form>
        
        <p>Max file size: 2GB | Allowed formats: {{ allowed_extensions }}</p>
    </div>
</body>
</html>
"""

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def split_file(file_path, chunk_size_mb=MAX_SIZE_MB):
    chunk_size = chunk_size_mb * 1024 * 1024
    file_size = os.path.getsize(file_path)
    
    if file_size <= chunk_size:
        return [file_path]

    parts = []
    with open(file_path, 'rb') as f:
        part_num = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            part_path = f"{file_path}.part{part_num}"
            with open(part_path, 'wb') as pf:
                pf.write(chunk)
            parts.append(part_path)
            part_num += 1
    return parts

# Async sending function
async def send_file_to_telegram(file_path, filename):
    client = TelegramClient(session_path, api_id, api_hash)
    await client.start()

    if not await client.is_user_authorized():
        raise Exception("Telegram client is not authorized")

    parts = split_file(file_path)
    for i, part in enumerate(parts, 1):
        caption = f"{filename} (Part {i}/{len(parts)})" if len(parts) > 1 else filename
        await client.send_file("me", part, caption=caption)
        os.remove(part)

    await client.disconnect()
    return len(parts)

# Flask route
@app.route("/", methods=["GET", "POST"])
def upload_file():
    message = None
    message_class = None

    if request.method == "POST":
        if "video" not in request.files:
            message = "No file selected"
            message_class = "error"
        else:
            file = request.files["video"]
            if file.filename == "":
                message = "No file selected"
                message_class = "error"
            elif not allowed_file(file.filename):
                message = f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
                message_class = "error"
            else:
                try:
                    file_path = UPLOAD_FOLDER / file.filename
                    file.save(file_path)

                    # Run async send_file_to_telegram in new event loop
                    parts_uploaded = asyncio.run(send_file_to_telegram(file_path, file.filename))

                    message = f"Uploaded successfully! ({parts_uploaded} parts)" if parts_uploaded > 1 else "Uploaded successfully!"
                    message_class = "success"

                    if os.path.exists(file_path):
                        os.remove(file_path)

                except Exception as e:
                    message = f"Telegram error: {str(e)}"
                    message_class = "error"
                    logger.error(f"Telegram error: {e}")

    return render_template_string(
        HTML_TEMPLATE,
        message=message,
        message_class=message_class,
        allowed_extensions=", ".join(ALLOWED_EXTENSIONS)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
