import resend
import base64
import os

async def send_enquiry_email(data):
    """
    Send enquiry details to admin via Resend API
    """

    email_body = f"""
    New Enquiry Received

    Full Name          : {data.full_name}
    Email Address      : {data.email_address}
    Contact Number     : {data.contact_number}

    Category           : {data.category}
    Destination        : {data.destination}
    Custom Destination : {data.custom_destination or "N/A"}
    Additional Dest.   : {data.additional_destination or "N/A"}

    Travel Start Date  : {data.start_date}

    Adults             : {data.adults}
    Children           : {data.children}

    Departure City     : {data.departure_city}

    Referral Source    : {data.referral_source}
    Referral Other     : {data.referral_other or "N/A"}

    Special Requests   : {data.special_requests or "None"}
    """

    email = {
        "from": "Tirth Ghumo <no-reply@tirthghumo.in>",
        "to": ["hr.tirthghumo@gmail.com"],
        "subject": "New Travel Enquiry Received",
        "text": email_body.strip(),
    }

    try:
        resend.Emails.send(email)
        return {"status": "Enquiry email sent successfully"}
    except Exception as e:
        raise Exception(f"Enquiry email sending failed: {str(e)}")
