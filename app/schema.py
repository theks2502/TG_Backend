from pydantic import BaseModel, EmailStr , Field , validator , HttpUrl
from typing import Optional , List
from datetime import date , datetime


#One Day trek 
class ODTBase(BaseModel):
    full_name: str
    email_address: str
    age: int
    gender: str
    contact_number: str
    whatsapp_number: str
    college_name:str
    pick_up_loc: str
    drop_loc: str
    meal_preference: str
    trip_exp_level: Optional[str] = None
    medical_details: Optional[str] = None
    payment_screenshot: Optional[str] = None
    agree: bool

    @validator(
        "full_name", "email_address", "gender", "contact_number",
        "whatsapp_number", "college_name", "pick_up_loc", "drop_loc",
        "meal_preference"
    )
    def no_empty_or_blank(cls, v):
        if v is None or not v.strip():
            raise ValueError("Field cannot be empty or blank")
        return v


class ODTCreate(ODTBase):
    pass  # same as base for now

class ODTResponse(ODTBase):
    id: int
    submitted_at: datetime

    class Config:
        from_attributes = True

class Manali(BaseModel):
    full_name:str
    gender:str
    age:int
    email_address:str
    contact_number :str
    whatsapp_number : str 
    emergency_contact_number : str 
    college_name : str 
    proof_id_type : str 
    chosen_id_number : str 
    id_image : str 
    medical_details : Optional[str] = None
    special_request :str 
    agree : bool

class Tamia(BaseModel):
    full_name:str
    gender:str
    age:int
    email_address:str
    contact_number :str
    whatsapp_number : str 
    emergency_contact_number : str 
    college_name : str 
    mode_of_transport : str
    proof_id_type : str 
    chosen_id_number : str 
    id_image : str 
    medical_details : Optional[str] = None
    special_request :str 
    agree : bool

class Rishikesh(Tamia):
    pass


class SaarthiForm(BaseModel):
    full_name: str
    date_of_birthday: date
    gender: str
    aadhar_number: str
    aadhar_card_image: str
    profile_image: str
    email_address: EmailStr
    contact_number: str
    whatsapp_number: str
    current_city: str
    state: str
    address: str
    occupation: str
    organization_name: str
    job_role: str
    work_exp: str
    company_id: str | None = None
    profile_url: str
    role: str
    motive: str

class EnquiryCreateSchema(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=150)
    email_address: EmailStr
    contact_number: str = Field(..., min_length=8, max_length=15)

    category: str = Field(..., max_length=100)
    destination: str = Field(..., max_length=150)
    custom_destination: Optional[str] = Field(None, max_length=150)
    additional_destination: Optional[str] = Field(None, max_length=150)

    start_date: date

    adults: int = Field(..., gt=0)
    children: int = Field(0, ge=0)

    departure_city: str = Field(..., max_length=100)

    referral_source: str = Field(..., max_length=100)
    referral_other: Optional[str] = Field(None, max_length=100)

    special_requests: Optional[str]

    class Config:
        from_attributes = True

class HiringApplicationCreateSchema(BaseModel):
    # ---------------- Personal Info ----------------
    full_name: str = Field(..., min_length=2, max_length=150)
    email_address: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=15)

    
    gender: Optional[str] = Field(None, max_length=20)
    current_city: str = Field(..., max_length=100)

    education_qualification: Optional[str] = Field(None, max_length=100)
    college_name: Optional[str] = Field(None, max_length=150)
    
    # ---------------- Position ----------------
    position_applied: str = Field(..., max_length=100)
    why_this_role: str = Field(..., min_length=20, max_length=2000)

    # ---------------- Experience & Skills ----------------
    resume_file: HttpUrl

    key_skills: List[str] = Field(..., min_items=1)
    # Example: ["Communication", "Marketing", "Web Developer"]

    work_proof_links: Optional[List[HttpUrl]] = None

    worked_in_travel_company: bool = False
    previous_travel_role: Optional[str] = Field(None, max_length=2000)

    # ---------------- Travel Knowledge ----------------
    top_3_destinations: Optional[List[str]] = None
    travel_expertise_rating: Optional[int] = Field(None, ge=1, le=10)
    managed_group_trips: Optional[bool] = None
    comfortable_24x7: Optional[bool] = None

    # ---------------- Identity ----------------
    id_proof_type: Optional[str] = Field(None, max_length=50)
    id_proof_file: Optional[HttpUrl] = None

    linkedin_profile: Optional[HttpUrl] = None
    portfolio_url: Optional[HttpUrl] = None

    # ---------------- Final ----------------
    why_should_we_hire_you: str = Field(..., min_length=20, max_length=3000)
    referral_source: Optional[str] = Field(None, max_length=100)
    agreement_confirmed: bool

    class Config:
        from_attributes = True


# VR DARSHAN

class VRDarshanDevoteeSchema(BaseModel):
    id: int
    full_name: str = Field(..., min_length=2, max_length=150)
    age: int = Field(..., ge=1, le=120)
    gender: str = Field(..., max_length=20)
    address: str
    aadhar_image_url: str
    created_at: datetime

    class Config:
        from_attributes = True

class VRDarshanBookingSchema(BaseModel):
    # ---------------- Contact Details ----------------
    contact_number: str = Field(..., min_length=10, max_length=15)
    whatsapp_number: str = Field(..., min_length=10, max_length=15)
    email_address: EmailStr

    # ---------------- Darshan Details ----------------
    spiritual_place: str = Field(..., max_length=150)
    preferred_date: date
    time_slot: str = Field(..., max_length=50)
    special_request: Optional[str] = None
    payment_screenshot: Optional[str] = None


    # ---------------- Devotees ----------------
    devotees: List[VRDarshanDevoteeSchema]

    class Config:
        from_attributes = True