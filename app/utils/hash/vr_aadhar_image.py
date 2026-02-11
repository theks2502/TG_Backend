import hashlib

async def generate_image_hash(upload_file)-> str:
    file_bytes = await upload_file.read()
    return hashlib.sha256(file_bytes).hexdigest() , file_bytes