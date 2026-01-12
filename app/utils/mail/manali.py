from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config import settings 
import requests
import resend 
import base64
import os

# async def send_booking_email_manali(data, image_path: str | None = None):
#     """Send booking details via Resend API with optional image attachment."""

#     email_body = f"""
#     Full Name: {data.full_name}
#     Email Address: {data.email_address}
#     Age: {data.age}
#     Gender: {data.gender}
#     Contact Number: {data.contact_number}
#     Whatsapp Number: {data.whatsapp_number}
#     Emergency Contact Number : {data.emergency_contact_number}
#     College Name: {data.college_name}
#     Proof Id Type: {data.proof_id_type}
#     Id number: {data.chosen_id_number}
#     Medical Details: {data.medical_details}
#     Special Request:{data.special_request}
#     Agree to Terms: {data.agree}
#     """

#     attachments = []

#     # ✅ Attach local file as Base64 (no 'path' key)
#     if image_path and os.path.exists(image_path):
#         with open(image_path, "rb") as f:
#             file_data = base64.b64encode(f.read()).decode("utf-8")
#             file_name = os.path.basename(image_path)
#             attachments.append({
#                 "content": file_data,
#                 "filename": file_name,
#                 "type": "image/jpeg" if image_path.lower().endswith((".jpg", ".jpeg")) else "image/png"
#             })

#     email = {
#         "from":  "Tirth Ghumo <no-reply@tirthghumo.in>",
#         "to": ["hr.tirthghumo@gmail.com"],
#         "subject": "New Booking for Manali",
#         "text": email_body.strip(),
#     }

#     # Only add attachments if present
#     if attachments:
#         email["attachments"] = attachments

#     try:
#         resend.Emails.send(email)
#         return {"status": "Email sent successfully"}
#     except Exception as e:
#         raise Exception(f"Email sending failed: {str(e)}")

async def send_booking_email_manali(booking, passengers , payment_screenshot_file=None):

    

    approve = f"http://127.0.0.1:8000/admin/manali/action?booking_id={booking.id}&action=approve"
    decline_payment = f"http://127.0.0.1:8000/admin/manali/action?booking_id={booking.id}&action=decline_payment"

    """
    Sends Manali booking details to admin email.
    booking  -> ManaliTripBooking ORM object
    passengers -> list[ManaliTripPassenger]
    """

    # -----------------------------
    # Build passengers section
    # -----------------------------
    passenger_details = ""
    for idx, p in enumerate(passengers, start=1):
        passenger_details += (
            f"\nPassenger {idx}:\n"
            f"  Name: {p.full_name}\n"
            f"  Gender: {p.gender}\n"
            f"  Age: {p.age}\n"
            f"  Contact: {p.contact_number or 'N/A'}\n"
            f"  Train Type: {p.train_type}\n"
        )

    # -----------------------------
    # Email body
    # -----------------------------
    email_body = f"""
NEW MANALI TRIP BOOKING RECEIVED

LEADER DETAILS
--------------
Full Name: {booking.full_name}
Email: {booking.email}
Age: {booking.age}
Gender: {booking.gender}
Contact Number: {booking.contact_number}
WhatsApp Number: {booking.whatsapp_number}
College Name: {booking.college_name}

BOOKING DETAILS
---------------
Train Type: {booking.train_type}
Total Passengers: {booking.no_of_passengers}

PASSENGERS
----------
{passenger_details}

ACTIONS
-------
Approve Booking:
{approve}
Decline Booking (Payment Not Received):
{decline_payment}
    """.strip()

    attachments = []

    # -----------------------------
    # Attach payment screenshot FILE
    # -----------------------------
    if payment_screenshot_file:
        payment_screenshot_file.file.seek(0)

        file_bytes = payment_screenshot_file.file.read()
        if not file_bytes:
            raise Exception("Payment screenshot file is empty")

        encoded = base64.b64encode(file_bytes).decode("utf-8")

        attachments.append({
            "filename": payment_screenshot_file.filename,
            "content": encoded,
            "type": payment_screenshot_file.content_type or "image/png"
        })

    

    # -----------------------------
    # Email payload
    # -----------------------------
    email = {
        "from": "Tirth Ghumo <no-reply@tirthghumo.in>",
        "to": ["hr.tirthghumo@gmail.com"],
        "subject": "🚍 New Manali Trip Booking",
        "text": email_body,
    }
    if attachments:
        email["attachments"] = attachments

    try:
        resend.Emails.send(email)
        return {"status": "Email sent to admin"}
    except Exception as e:
        raise Exception(f"Admin email failed: {str(e)}")

async def send_user_approval_mail_manali(b):
    resend.Emails.send({
        "from": "Tirth Ghumo <no-reply@tirthghumo.in>",
        "to": [b.email],
        "subject": "Your Manali Trip Booking Is Approved – TirthGhumo",
        "text": f"""
Dear {b.full_name},

Greetings from TirthGhumo 🌄

We’re happy to inform you that your Manali Trip booking has been successfully verified and approved ✅. All the details shared by you, including payment and documents, have been carefully reviewed by our team.

Your booking is now officially confirmed 🎊
Further details related to the travel itinerary, reporting schedule, accommodation, and important instructions will be shared with you shortly via email and WhatsApp 📩📱.

Please keep this email for future reference. If any updates or additional requirements arise, our team will proactively get in touch with you.

For any queries or assistance, feel free to reach out to us at "hr.tirthghumo@gmail.com" 💬.

Thank you for choosing TirthGhumo 🙏
We look forward to making your journey safe, smooth, and truly memorable ✨

Warm regards,
Team TirthGhumo

"""
    })

async def send_user_decline_payment_mail_manali(b):
    resend.Emails.send({
        "from": "Tirth Ghumo <no-reply@tirthghumo.in>",
        "to": [b.email],
        "subject": "Payment Verification Required – TirthGhumo",
        "text": f"""
Dear {{b.full_name}},

Greetings from TirthGhumo 🌄

We hope you are doing well.

While reviewing your Manali Trip booking, we were unable to locate or verify the payment record, or there appears to be a small discrepancy. This may be due to a technical delay.

We kindly request you to please share the payment screenshot or transaction details once again for verification on {6260499299}. Our team will review it promptly and proceed further.

Thank you for your understanding and cooperation 🙏
For any assistance, feel free to contact.

Warm regards,
Team TirthGhumo

"""
    })