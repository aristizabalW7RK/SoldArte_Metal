from fastapi import UploadFile
from backend.core.config import settings
import os, uuid, shutil


def save_upload(file: UploadFile, subdir: str = "") -> str:
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    ext = file.filename.split(".")[-1] if "." in (file.filename or "") else "jpg"
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(settings.UPLOAD_DIR, filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return f"/uploads/{filename}"
