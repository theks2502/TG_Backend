import json , shutil , os , qrcode , uuid , tempfile
from fastapi import HTTPException
from app.utils.supabase_uploads import upload_to_supabase_qr
from fastapi import FastAPI ,  HTTPException , Response , status , Depends , APIRouter , Form , File , UploadFile
from app import models , schema  
from sqlalchemy.orm import Session
from app.database import engine , get_db
from app.config import settings 
from fastapi import BackgroundTasks

router = APIRouter()
def generate_payment_qr(amount: int) -> str:
    upi_id = "6260499299@okbizaxis"
    payee_name = "Tirth Ghumo"
    note = "VR Darshan Booking"

    upi_url = (
        f"upi://pay?"
        f"pa={upi_id}"
        f"&pn={payee_name}"
        f"&am={amount}"
        f"&cu=INR"
        f"&tn={note}"
    )

    qr = qrcode.make(upi_url)

    filename = f"vr_darshan_qr_{uuid.uuid4()}.png"

    # ✅ cross-platform temp directory
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)

    qr.save(file_path)

    return file_path

    

@router.get("/vr-darshan/price")
async def calculate_vr_darshan_price(
    number_of_persons: int,
):

    PRICE_PER_SENIOR = 39

    amount = number_of_persons * PRICE_PER_SENIOR

    qr_url = None
    session_id = None

    if amount > 0:
        qr_path = generate_payment_qr(amount)
        qr_url = upload_to_supabase_qr(qr_path, "vr_darshan_qr")
        session_id = str(uuid.uuid4())

    return {
        "payment_qr_url": qr_url,
    }
@router.get("/manali/price")
async def calculate_manali_price(
    sleeper: int , 
    ac : int
):

    PRICE_PER_SLEPPER = 5000
    PRICE_PER_AC = 6000
    amount = (sleeper * PRICE_PER_SLEPPER) + (ac * PRICE_PER_AC)
    qr_path = generate_payment_qr(amount)
    qr_url = upload_to_supabase_qr(qr_path, "manali_qr")
    session_id = str(uuid.uuid4())

    return {
        "payment_qr_url": qr_url
    }





