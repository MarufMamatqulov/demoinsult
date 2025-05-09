import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from backend.core.crud import get_user_contact_info

def send_alert(user_id, message, method):
    """
    Send an alert to the user via the specified method.

    Args:
        user_id (int): The ID of the user to send the alert to.
        message (str): The alert message to send.
        method (str): The method to use for sending the alert ('telegram' or 'email').

    Returns:
        None
    """
    contact_info = get_user_contact_info(user_id)

    if method == 'telegram':
        telegram_token = "<YOUR_TELEGRAM_BOT_TOKEN>"
        chat_id = contact_info.get('telegram_chat_id')
        if not chat_id:
            raise ValueError("User does not have a Telegram chat ID configured.")

        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message
        }
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            raise Exception(f"Failed to send Telegram message: {response.text}")

    elif method == 'email':
        email_address = contact_info.get('email')
        if not email_address:
            raise ValueError("User does not have an email address configured.")

        sender_email = "<YOUR_EMAIL_ADDRESS>"
        sender_password = "<YOUR_EMAIL_PASSWORD>"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email_address
        msg['Subject'] = "Health Alert"

        msg.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

    else:
        raise ValueError("Invalid method. Use 'telegram' or 'email'.")
