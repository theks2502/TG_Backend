from fastapi import FastAPI ,  HTTPException , Response , status , Depends , APIRouter , Form , File , UploadFile
from app import models , schema  
from sqlalchemy.orm import Session
from app.database import engine , get_db
from app.config import settings  
from app.utils.mail.hiring_mail import send_hiring_email
import shutil, os , json
from fastapi import BackgroundTasks
from app.utils.invoice_generator import generate_invoice
from datetime import date
from app.utils.supabase_uploads import upload_to_supabase



router = APIRouter()

def parse_work_proofs(value: str | None):
    if not value:
        return []

    proofs = []
    for line in value.splitlines():
        line = line.strip()
        if not line:
            continue

        if ":" in line:
            ptype, url = line.split(":", 1)
            proofs.append({
                "type": ptype.strip(),
                "url": url.strip()
            })
        else:
            proofs.append({
                "type": "Link",
                "url": line
            })
    return proofs

def parse_skills(value: str):
    value = value.strip()
    if value.startswith("["):
        skills = json.loads(value)
    else:
        skills = value.split(",")

    return sorted(
        {s.strip().title() for s in skills if s.strip()}
    )


@router.post("/hiring/apply", status_code=status.HTTP_201_CREATED)
async def apply_for_hiring(
    background_tasks: BackgroundTasks,
    # -------- Personal Info --------
    full_name: str = Form(...),
    email_address: str = Form(...),
    phone_number: str = Form(...),
    gender: str = Form(None),
    current_city: str = Form(...),

    education_qualification: str = Form(None),
    college_name: str = Form(None),
    

    # -------- Position --------
    position_applied: str = Form(...),
    why_this_role: str = Form(...),

    # -------- Experience --------
    worked_in_travel_company: bool = Form(False),
    previous_travel_role: str = Form(None),

    travel_expertise_rating: int = Form(None),
    managed_group_trips: bool = Form(False),
    comfortable_24x7: bool = Form(False),

    why_should_we_hire_you: str = Form(...),
    referral_source: str = Form(None),
    agreement_confirmed: bool = Form(...),

    linkedin_profile: str = Form(None),
    portfolio_url: str = Form(None),

    # -------- Multi-value fields --------
    key_skills: str = Form(...),        # JSON OR comma-separated
    work_proof_link: str = Form(None),  # JSON list

    # -------- Files --------
    resume_file: UploadFile | None = File(None),
    id_proof_type: str = Form(...),
    id_proof_file: UploadFile | None = File(None),

    db: Session = Depends(get_db)
):
    # ---------------- BASIC VALIDATION ----------------
    if not agreement_confirmed:
        raise HTTPException(400, "Agreement must be accepted")


    try:
        skills_list = parse_skills(key_skills)
        skills_text = ", ".join(skills_list)
        work_proof_list = parse_work_proofs(work_proof_link) if work_proof_link else []
    except Exception:
        raise HTTPException(400, "Invalid skills or work_proofs format")

    if not skills_list:
        raise HTTPException(400, "At least one skill is required")

    # ---------------- FILE UPLOADS ----------------
    print(resume_file, id_proof_file)
    resume_url = None
    id_proof_url = None

    if resume_file and resume_file.filename and resume_file.size > 0:
        resume_url = upload_to_supabase(resume_file, folder="resumes")

    if id_proof_file and id_proof_file.filename and id_proof_file.size > 0:
        id_proof_url = upload_to_supabase(id_proof_file, folder="id_proofs")
    # ---------------- DB INSERT ----------------
    application = models.HiringApplication(
        full_name=full_name,
        email_address=email_address,
        phone_number=phone_number,
        gender=gender,
        current_city=current_city,
        education_qualification=education_qualification,
        college_name=college_name,
        position_applied=position_applied,
        why_this_role=why_this_role,
        worked_in_travel_company=worked_in_travel_company,
        previous_travel_role=previous_travel_role,
        travel_expertise_rating=travel_expertise_rating,
        managed_group_trips=managed_group_trips,
        comfortable_24x7=comfortable_24x7,
        key_skills=skills_text,
        work_proof_links=json.dumps(work_proof_list) if work_proof_list else None,
        why_should_we_hire_you=why_should_we_hire_you,
        referral_source=referral_source,
        agreement_confirmed=agreement_confirmed,
        linkedin_profile=linkedin_profile,
        portfolio_url=portfolio_url,
        resume_file=resume_url,
        id_proof_type=id_proof_type,
        id_proof_file=id_proof_url,
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    background_tasks.add_task(send_hiring_email, application)


    return {
        "message": "Application submitted successfully",
        "application_id": application.id
    }

