from fastapi import FastAPI ,  HTTPException , Response , status , Depends , APIRouter , Form , File , UploadFile , Request
from app import models , schema  
from sqlalchemy.orm import Session 
from sqlalchemy.exc import IntegrityError
from app.database import engine , get_db
from app.config import settings  
from app.utils.mail.vr_admin_mail import send_admin_vr_darshan_email
import shutil, os , json
from fastapi import BackgroundTasks
from app.utils.invoice_generator import generate_invoice
from datetime import date
from app.utils.supabase_uploads import upload_to_supabase
from app.models import InstantVRDarshan , ShivratriVRDarshan
from app.schema import InstantVRDarshanRequest
from app.utils.hash.vr_aadhar_image import generate_image_hash


router = APIRouter()

@router.post(
    "/vr-darshan/booking",
    status_code=status.HTTP_201_CREATED
)
async def create_vr_darshan_booking(
    background_tasks: BackgroundTasks,
    # ---------- Contact Details ----------

    contact_number: str = Form(...),
    whatsapp_number: str = Form(...),
    email_address: str = Form(...),

    # ---------- Darshan Details ----------
    spiritual_place: str = Form(...),
    preferred_date: date = Form(...),
    time_slot: str = Form(...),
    special_request: str | None = Form(None),

    # ---------- Devotees ----------
    devotees: str = Form(...),  # JSON string
    aadhar_images: list[UploadFile] = File(...),
    payment_screenshot: UploadFile = File(None),

    db: Session = Depends(get_db)
):
    """
    Create VR Darshan booking with multiple devotees
    """

    # ---------------- Parse Devotees ----------------
    try:
        devotees_data = json.loads(devotees)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid devotees format. Must be valid JSON."
        )

    if not isinstance(devotees_data, list) or not devotees_data:
        raise HTTPException(
            status_code=400,
            detail="At least one devotee is required."
        )

    if len(devotees_data) != len(aadhar_images):
        raise HTTPException(
            status_code=400,
            detail="Devotees count and Aadhaar images count must match."
        )
    payment_screenshot_url = None

    if payment_screenshot:
        try:
            payment_screenshot_url = upload_to_supabase(
                payment_screenshot,
                folder="vr_darshan_payments"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload payment screenshot: {str(e)}"
            )

    # ---------------- Create Booking ----------------
    booking = models.VRDarshanBooking(
        contact_number=contact_number,
        whatsapp_number=whatsapp_number,
        email_address=email_address,
        spiritual_place=spiritual_place,
        preferred_date=preferred_date,
        time_slot=time_slot,
        special_request=special_request,
        payment_screenshot=payment_screenshot_url
    )

    db.add(booking)
    db.flush()

    # ---------------- Create Devotees ----------------
    for index, devotee in enumerate(devotees_data):
        required_fields = ["full_name", "age", "gender", "address"]

        if not all(field in devotee for field in required_fields):
            raise HTTPException(
                status_code=400,
                detail=f"Missing devotee fields at index {index}"
            )

        image_hash , file_bytes = await generate_image_hash(aadhar_images[index])

        if devotee["age"] >= 60:
            try:
                claim = models.VRBenefitClaim(
                    benefit_code="FREE_VR_60_PLUS",
                    aadhar_image_hash=image_hash
                )
                db.add(claim)
                db.flush()  # triggers UNIQUE constraint

            except IntegrityError:
                db.rollback()
                raise HTTPException(
                    status_code=400,
                    detail="This Aadhaar has already claimed free VR Darshan."
                )
        aadhar_images[index].file.seek(0)

        # Upload Aadhaar
        aadhar_url = upload_to_supabase(
            aadhar_images[index],
            folder="vr_darshan_aadhar"
            # file_bytes=file_bytes
        )
        
        
        db.add(
            models.VRDarshanDevotee(
                booking_id=booking.id,
                full_name=devotee["full_name"],
                age=devotee["age"],
                gender=devotee["gender"],
                address=devotee["address"],
                aadhar_image_url=aadhar_url,
                aadhar_image_hash=image_hash
            )
        )

        db.flush()

        

    db.commit()
    background_tasks.add_task(send_admin_vr_darshan_email, booking)

    return {
        "message": "VR Darshan booking created successfully",
        "booking_id": booking.id
    }

@router.post("/instant-vr-darshan")
async def add_multiple(devotees: str = Form(...),          
    paymentMode: str = Form(...),
    aadhar_images: list[UploadFile] = File(...),
     db: Session = Depends(get_db)):
    
    devotees_list = json.loads(devotees)
    if len(devotees_list) != len(aadhar_images):
        raise HTTPException(
            status_code=400,
            detail="Devotees count and Aadhar images count must match."
        )
    rows = []

   

    for index , d in enumerate(devotees_list):
        #hash first
        image_hash,_ = await generate_image_hash(aadhar_images[index])

        if d["age"] >= 60:
            try:
                claim = models.VRBenefitClaim(
                    benefit_code="FREE_VR_60_PLUS",
                    aadhar_image_hash=image_hash
                )
                db.add(claim)
                db.flush()  # triggers UNIQUE constraint

            except IntegrityError:
                db.rollback()
                raise HTTPException(
                    status_code=400,
                    detail="This Aadhaar has already claimed free VR Darshan."
                )
        
        aadhar_images[index].file.seek(0)

        aadhar_url = upload_to_supabase(
            aadhar_images[index],
            folder="instant_vr_aadhar"
        )

        
        row = InstantVRDarshan(
            full_name=d["name"],              # frontend → DB
            age=d["age"],
            gender=d["gender"],
            darshanCategory=d["category"],    # IMPORTANT
            darshan=d["darshan"],
            contact_number="NA",              # frontend doesn’t send it
            payment_option=paymentMode.upper(),
            aadhar_image_url=aadhar_url,
            aadhar_image_hash=image_hash
        )
        db.add(row)
            

        
    db.commit()

    return {
        "inserted": len(devotees_list)
    }

@router.post("/shivratri-vr-darshan")
async def add_multiple(
    request: Request,
    devotees: str = Form(...),
    db: Session = Depends(get_db)
):
    # Validate JSON
    try:
        devotees_list = json.loads(devotees)
        if not isinstance(devotees_list, list):
            raise ValueError
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid devotees data")

    form = await request.form()

    try:
        for index, d in enumerate(devotees_list):

            aadhar_url = None
            file_key = f"aadhar_{index}"

            # Explicit file mapping per devotee
            if file_key in form:
                file = form[file_key]
                if file and hasattr(file, "filename") and file.filename:
                    aadhar_url = upload_to_supabase(
                        file,
                        folder="shivratri_vr_darshan"
                    )

            row = ShivratriVRDarshan(
                full_name=d.get("name") or None,
                age=int(d["age"]) if d.get("age") not in [None, ""] else None,
                gender=d.get("gender") or None,
                darshanCategory=d.get("category") or None,
                darshan=d.get("darshan") or None,
                contact_number=d.get("contact_number") or None,
                aadhar_image_url=aadhar_url
            )

            db.add(row)

        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"inserted": len(devotees_list)}