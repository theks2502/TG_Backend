from sqlalchemy import  Column , Integer , String , Boolean, Text , ForeignKey  , Date , text ,CheckConstraint, func ,DateTime , UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from datetime  import date , datetime 


class ODT(Base):
    __tablename__ = "odt_bookings"

    id = Column(Integer , primary_key= True , index=  True )
    full_name = Column(String(100), nullable=False )
    email_address = Column(String(100), nullable=False )
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)
    contact_number = Column(String(20), nullable=False)
    whatsapp_number = Column(String(20), nullable=False)
    college_name = Column(String(200), nullable=False)
    pick_up_loc = Column(String(50), nullable=False)
    drop_loc = Column(String(50), nullable=False)
    meal_preference = Column(String(30), nullable=False)
    trip_exp_level = Column(String(40))
    medical_details = Column(String(100))
    payment_screenshot = Column(String(255), nullable=False)
    agree = Column(Boolean, default=False)
    submitted_at = Column(TIMESTAMP(timezone=True) , nullable= False ,server_default = text('now()') ) 

    __table_args__ = (
        CheckConstraint("full_name <> '' AND TRIM(full_name) <> ''", name="full_name_not_blank"),
        CheckConstraint("email_address <> '' AND TRIM(email_address) <> ''", name="email_not_blank"),
        CheckConstraint("gender <> '' AND TRIM(gender) <> ''", name="gender_not_blank"),
        CheckConstraint("college_name <> '' AND TRIM(college_name) <> ''", name="college_not_blank"),
    )


class Tamia(Base):
    __tablename__="tamia"

    id = Column(Integer , primary_key = True , index = True )
    full_name = Column(String(100) , nullable = False)
    gender = Column(String(20) , nullable = False)
    age = Column(Integer , nullable = False)
    email_address = Column(String(100) , nullable =  False)
    contact_number = Column(String(20), nullable=False)
    whatsapp_number = Column(String(20), nullable=False)
    emergency_contact_number = Column(String(20), nullable=False)
    college_name = Column(String(200), nullable=False)
    proof_id_type = Column(String(200) , nullable = False) 
    mode_of_transport = Column(String(50) , nullable = False)
    chosen_id_number = Column(String(50) , nullable = False) 
    id_image = Column(String(255) , nullable = False) 
    medical_details = Column(String(200))
    special_request = Column(String(300))
    agree = Column(Boolean, default=False)
    submitted_at = Column(TIMESTAMP(timezone=True) , nullable= False ,server_default = text('now()') ) 


class Rishikesh_Haridwar(Base):
    __tablename__="rishikesh_haridwar"

    id = Column(Integer , primary_key = True , index = True )
    full_name = Column(String(100) , nullable = False)
    gender = Column(String(20) , nullable = False)
    age = Column(Integer , nullable = False)
    email_address = Column(String(100) , nullable =  False)
    contact_number = Column(String(20), nullable=False)
    whatsapp_number = Column(String(20), nullable=False)
    emergency_contact_number = Column(String(20), nullable=False)
    college_name = Column(String(200), nullable=False)
    proof_id_type = Column(String(200) , nullable = False) 
    mode_of_transport = Column(String(50) , nullable = False)
    chosen_id_number = Column(String(50) , nullable = False) 
    id_image = Column(String(255) , nullable = False) 
    medical_details = Column(String(200))
    special_request = Column(String(300))
    agree = Column(Boolean, default=False)
    submitted_at = Column(TIMESTAMP(timezone=True) , nullable= False ,server_default = text('now()') ) 

class Saarthi_Form(Base):
    __tablename__="saarthi_form"
    id = Column(Integer , primary_key = True , index = True )
    full_name = Column(String(50) , nullable = False)
    date_of_birthday = Column(Date , nullable = False)
    gender = Column(String(20) , nullable = False)
    aadhar_number = Column(String(50) , nullable = False)
    aadhar_card_image = Column(String(255) , nullable = False)
    profile_image = Column(String(255) , nullable = False)
    email_address = Column(String(100) , nullable =  False)
    contact_number = Column(String(20), nullable=False)
    whatsapp_number = Column(String(20), nullable=False)
    current_city = Column(String(30) , nullable = False) 
    state = Column(String(30) , nullable = False)
    address = Column(String(100) , nullable = False)
    occupation = Column(String(50) , nullable = False)
    organization_name = Column(String(70) , nullable = False)
    job_role = Column(String(50) , nullable = False)
    work_exp = Column(String(30) , nullable = False)
    company_id = Column(String(255))
    profile_url = Column(String(300) , nullable = False)
    role = Column(String(100) , nullable = False) 
    motive = Column(String(300) , nullable = False)

class Enquiry_Form(Base):
    __tablename__ = "enquiry_form"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(150), nullable=False)
    email_address = Column(String(255), nullable=False, index=True)
    contact_number = Column(String(15), nullable=False)

    category = Column(String(100), nullable=False)
    destination = Column(String(150), nullable=False)
    custom_destination = Column(String(150))
    additional_destination = Column(String(150))

    start_date = Column(Date, nullable=False)

    adults = Column(Integer, nullable=False)
    children = Column(Integer, nullable=False, server_default="0")

    departure_city = Column(String(100), nullable=False)

    referral_source = Column(String(100), nullable=False)
    referral_other = Column(String(100))

    special_requests = Column(Text)

    submitted_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint('adults > 0', name='check_adults_positive'),
        CheckConstraint('children >= 0', name='check_children_non_negative'),
    )

class HiringApplication(Base):
    __tablename__ = "hiring_application"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email_address = Column(String(255), nullable=False, index=True)
    phone_number = Column(String(15), nullable=False)

    
    gender = Column(String(20))
    current_city = Column(String(100), nullable=False)

    education_qualification = Column(String(100))
    college_name = Column(String(150))
    

    position_applied = Column(String(100), nullable=False)
    why_this_role = Column(Text, nullable=False)

    resume_file = Column(Text , nullable=True)

    key_skills = Column(Text, nullable=False)

    work_proof_links = Column(Text)
    # Example: [{"type":"GitHub","url":"..."},{"type":"Instagram","url":"..."}]

    worked_in_travel_company = Column(Boolean, default=False)
    previous_travel_role = Column(Text)

    # ---------------- Travel Knowledge ----------------
    top_3_destinations = Column(Text)
    # Example: ["Goa","Manali","Kedarnath"]

    travel_expertise_rating = Column(Integer)
    managed_group_trips = Column(Boolean)
    comfortable_24x7 = Column(Boolean)

    # ---------------- Identity ----------------
    id_proof_type = Column(String(50) , nullable=True)
    id_proof_file = Column(Text , nullable=True)

    linkedin_profile = Column(Text)
    portfolio_url = Column(Text)

    # ---------------- Final ----------------
    why_should_we_hire_you = Column(Text, nullable=False)
    referral_source = Column(String(100))
    agreement_confirmed = Column(Boolean, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

class VRBenefitClaim(Base):
    __tablename__ = "vr_benefit_claims"

    id = Column(Integer, primary_key=True, index=True)
    benefit_code = Column(String(100), nullable=False)
    aadhar_image_hash = Column(String(64), nullable=False)
    claimed_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            "benefit_code",
            "aadhar_image_hash",
            name="uq_benefit_aadhar"
        ),
    )
class VRDarshanBooking(Base):
    __tablename__ = "vr_darshan_booking"

    id = Column(Integer, primary_key=True, index=True)

    

    # ---------------- Contact Details ----------------
    contact_number = Column(String(15), nullable=False)
    whatsapp_number = Column(String(15), nullable=False)
    email_address = Column(String(255), nullable=False)

    # ---------------- Darshan Details ----------------
    spiritual_place = Column(String(150), nullable=False)
    preferred_date = Column(Date, nullable=False)
    time_slot = Column(String(50), nullable=False)
    special_request = Column(Text)
    payment_screenshot = Column(String(255), nullable=True)

    # ---------------- Meta ----------------
    is_confirmed = Column(Boolean, default=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    devotees = relationship(
        "VRDarshanDevotee",
        backref="booking",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<VRDarshanBooking id={self.id} place={self.spiritual_place}>"

class VRDarshanDevotee(Base):
    __tablename__ = "vr_darshan_devotee"

    id = Column(Integer, primary_key=True, index=True)

    booking_id = Column(
        Integer,
        ForeignKey("vr_darshan_booking.id", ondelete="CASCADE"),
        nullable=False
    )

    # ---------------- Devotee Details ----------------
    full_name = Column(String(150), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)
    address = Column(Text, nullable=False)

    # ---------------- Identity ----------------
    aadhar_image_url = Column(Text, nullable=False)
    aadhar_image_hash = Column(String(64) , nullable = False )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    def __repr__(self):
        return f"<VRDarshanDevotee id={self.id} name={self.full_name}>"

#Instant VR Darshan Booking Model

class InstantVRDarshan(Base):
    __tablename__ = "instant_vr_darshan"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)
    darshanCategory = Column(String(100), nullable=False)
    darshan = Column(String(150), nullable=False)
    contact_number = Column(String(15), nullable=False)
    aadhar_image_url = Column(Text, nullable=False)
    aadhar_image_hash = Column(String(64) , nullable = False )
    payment_option = Column(String(255), nullable=True)
    submitted_at =  Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

#MANALI TRIP
class ManaliTripBooking(Base):
    __tablename__ = "manali_trip_booking"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    contact_number = Column(String, nullable=False)
    whatsapp_number = Column(String, nullable=False)
    emergency_number = Column(String, nullable=True)
    college_name = Column(String, nullable=True)
    proof_id_type = Column(String, nullable=True)
    id_number = Column(String, nullable=True)
    id_image_url = Column(String, nullable=True)
    medical_detail = Column(String, nullable=True)
    special_request = Column(String, nullable=True)
    train_type = Column(String, nullable=False)
    no_of_passengers = Column(Integer, nullable=False)
    agreed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    payment_screenshot = Column(String(255), nullable=True)
    passengers = relationship(
        "ManaliTripPassenger",
        back_populates="booking",
        cascade="all, delete"
    )

class ManaliTripPassenger(Base):
    __tablename__ = "manali_trip_passengers"

    id = Column(Integer, primary_key=True, index=True)

    booking_id = Column(
        Integer,
        ForeignKey("manali_trip_booking.id"),
        nullable=False
    )

    full_name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    contact_number = Column(String, nullable=False)
    train_type = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    booking = relationship("ManaliTripBooking", back_populates="passengers")





