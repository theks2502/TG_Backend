from supabase import create_client, Client
import uuid , mimetypes
from app.config import settings

SUPABASE_URL = settings.supabase_url
SUPABASE_KEY = settings.supabase_key
BUCKET = settings.supabase_bucket

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_to_supabase(file, folder: str):
    """
    Upload file to Supabase Storage and return public URL.
    """
    # Get extension
    ext = file.filename.split(".")[-1]

    # Generate unique name
    file_name = f"{uuid.uuid4()}.{ext}"

    # Full path in bucket
    file_path = f"{folder}/{file_name}"

    # Read file bytes from UploadFile
    file_bytes = file.file.read()

    print("DEBUG_URL =", SUPABASE_URL)
    print("DEBUG_KEY =", SUPABASE_KEY[:10])
    print("DEBUG_BUCKET =", BUCKET)
    # Upload (IMPORTANT: use file_bytes, NOT file.file)
    supabase.storage.from_(BUCKET).upload(
        path=file_path,
        file=file_bytes,  # MUST be bytes
        file_options={"content-type": file.content_type}
    )

    # Return public URL
    public_url = supabase.storage.from_(BUCKET).get_public_url(file_path)

    return public_url

def upload_to_supabase_qr(file_path: str, folder: str) -> str:
    """
    Upload local file (QR image) to Supabase
    """
    ext = file_path.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{ext}"
    storage_path = f"{folder}/{file_name}"

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    content_type = mimetypes.guess_type(file_path)[0] or "image/png"

    supabase.storage.from_(BUCKET).upload(
        path=storage_path,
        file=file_bytes,
        file_options={"content-type": content_type}
    )

    return supabase.storage.from_(BUCKET).get_public_url(storage_path)
