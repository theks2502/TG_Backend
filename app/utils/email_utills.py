from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config import settings 
import requests
import resend 
import base64
import os
conf = ConnectionConfig(
    MAIL_USERNAME= settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=settings.mail_starttls,
    MAIL_SSL_TLS=settings.mail_ssl_tls,
    USE_CREDENTIALS=settings.use_credentials,
)

# async def send_booking_email(data ,  image_path: str | None = None):
#     message = MessageSchema(
#         subject="New Trekking Package Booking",
#         recipients=["tirthghumo@gmail.com"],
#         body=f"""
#         Full Name: {data.full_name}
#     Email Address: {data.email_address}
#     Age: {data.age}
#     Gender: {data.gender}
#     Contact Number: {data.contact_number}
#     Whatsapp Number: {data.whatsapp_number}
#     College Name: {data.college_name}
#     Pick-up Location: {data.pick_up_loc}
#     Drop Location: {data.drop_loc}
#     Meal Preference: {data.meal_preference}
#     Experience Level: {data.trip_exp_level}
#     Medical Details: {data.medical_details}
#     Agree to Terms: {data.agree}
#     """,
#        attachments = [image_path],
#         subtype="plain" 
#     )

#     fm = FastMail(conf)
#     await fm.send_message(message)

#CORRECT WLA UPR H 




#Tamia 



# Rishikesh Haridwar 

async def send_booking_email_rishikesh(data, image_path: str | None = None):
    """Send booking details via Resend API with optional image attachment."""

    email_body = f"""
    Full Name: {data.full_name}
    Email Address: {data.email_address}
    Age: {data.age}
    Gender: {data.gender}
    Contact Number: {data.contact_number}
    Whatsapp Number: {data.whatsapp_number}
    Emergency Contact Number : {data.emergency_contact_number}
    College Name: {data.college_name}
    Mode of Transport: {data.mode_of_transport}
    Proof Id Type: {data.proof_id_type}
    Id number: {data.chosen_id_number}
    Medical Details: {data.medical_details}
    Special Request:{data.special_request}
    Agree to Terms: {data.agree}
    """

    attachments = []

    # ✅ Attach local file as Base64 (no 'path' key)
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as f:
            file_data = base64.b64encode(f.read()).decode("utf-8")
            file_name = os.path.basename(image_path)
            attachments.append({
                "content": file_data,
                "filename": file_name,
                "type": "image/jpeg" if image_path.lower().endswith((".jpg", ".jpeg")) else "image/png"
            })

    email = {
        "from":  "Tirth Ghumo <no-reply@tirthghumo.in>",
        "to": ["tirthghumo@gmail.com"],
        "subject": "New Booking for Rishikesh Haridwar",
        "text": email_body.strip(),
    }

    # Only add attachments if present
    if attachments:
        email["attachments"] = attachments

    try:
        resend.Emails.send(email)
        return {"status": "Email sent successfully"}
    except Exception as e:
        raise Exception(f"Email sending failed: {str(e)}")

#   SAARTHI  FORM MAIL TO ADMIN

async def send_admin_email_saarthi(data):
    """Send full form details to admin."""

    email_body = f"""
    New Saarthi Form Submission

    Full Name: {data.full_name}
    Date of Birth: {data.date_of_birthday}
    Gender: {data.gender}
    Aadhar Number: {data.aadhar_number}
    Email Address: {data.email_address}
    Contact Number: {data.contact_number}
    Whatsapp Number: {data.whatsapp_number}
    City: {data.current_city}
    State: {data.state}
    Address: {data.address}
    Occupation: {data.occupation}
    Organization Name: {data.organization_name}
    Job Role: {data.job_role}
    Work Experience: {data.work_exp}
    Company ID: {data.company_id}
    Profile URL: {data.profile_url}
    Role: {data.role}
    Motive: {data.motive}

    # Profile Image : {data.profile_image}
    # Aadhar Image : {data.aadhar_card_image}
    """

    email = {
        "from": "Tirth Ghumo <no-reply@tirthghumo.in>",
        "to": ["hr.tirthghumo@gmail.com"],   # ADMIN EMAIL
        "subject": "New Saarthi Form Submission",
        "text": email_body.strip()
    }

    try:
        resend.Emails.send(email)
    except Exception as e:
        raise Exception(f"Admin email failed: {str(e)}")

# MAIL TO SAARTHI 

async def send_user_email_saarthi(data):
    """Send confirmation email to user."""

    email_body = f"""
    Hi {data.full_name},

    Thank you for submitting the Saarthi Registration Form.
    Our team has received your details successfully.

    We will review your application and reach out to you soon.

    Regards,
    Team Tirth Ghumo
    """

    email = {
        "from": "Tirth Ghumo <no-reply@tirthghumo.in>",
        "to": [data.email_address],
        "subject": "Saarthi Form – Submission Successful",
        "text": email_body.strip()
    }

    try:
        resend.Emails.send(email)
    except Exception as e:
        raise Exception(f"User email failed: {str(e)}")

