import os

class Config:
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit

def create_directories():
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
