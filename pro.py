import imaplib
import smtplib
from email.message import EmailMessage
import email
from queue import Queue
import streamlit as st
# Gmail credentials (hardcoded or input manually in Streamlit for testing)
GMAIL_USER = "dsproject490@gmail.com"  # Replace with your Gmail
GMAIL_PASS = "eyyb zkyv jptu nlip"     # Replace with app-specific password
# Function to send an automated response
def send_response_email(receiver_email, subject, message_body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = GMAIL_USER
    msg['To'] = receiver_email
    msg.set_content(message_body)
    # Set up the SMTP server
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)  # Login to Gmail
            server.send_message(msg)
            return True
    except Exception as e:
        st.error(f"Failed to send email to {receiver_email}: {e}")
        return False
# Pre-defined response message
def generate_response():
    return "Thank you for contacting us. We have received your inquiry and will respond shortly.
    https://todo-list21050.netlify.app/"
# Function to read unread emails from Gmail
def get_unread_emails():
    try:
        # Log in to the email account
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_USER, GMAIL_PASS)
        mail.select("inbox")
        # Search for all unread emails
        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()
        return email_ids, mail
    except Exception as e:
        st.error(f"Failed to retrieve emails: {e}")
        return [], None
# Function to process unread emails
def process_emails(email_queue, mail):
    sent_emails = []
    while not email_queue.empty():
        email_id = email_queue.get()
        # Fetch the email by ID
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                # Extract the email sender
                email_from = email.utils.parseaddr(msg['From'])[1]
                st.write(f"Processing email from: {email_from}")
                # Send an automated response
                response_message = generate_response()
                if send_response_email(email_from, "Thank you for contacting us", response_message):
                    sent_emails.append(email_from)
    return sent_emails
# Main function to activate the process
def start_automatic_response():
    # Queue to hold the email IDs
    email_queue = Queue()
    # Get unread emails
    email_ids, mail = get_unread_emails()
    if mail and email_ids:
        # Enqueue all unread emails
        for email_id in email_ids:
            email_queue.put(email_id)
        # Process emails and send responses
        sent_emails = process_emails(email_queue, mail)
        # Logout from the mail server
        mail.logout()
        # Store the list of sent emails in session state to display later
        st.session_state['sent_emails'] = sent_emails
    else:
        st.write("No unread emails found or failed to connect to the mail server.")
# Streamlit UI
st.title("AUTOMATIC EMAIL RESPONSE SYSTEM")
# Button to start the email response system
if 'sent_emails' not in st.session_state:
    st.session_state['sent_emails'] = []
if st.button('Start Automatic Email Response'):
    start_automatic_response()
    st.write("Processing unread emails and sending automatic responses...")
# Display the emails to which responses were sent
if st.session_state['sent_emails']:
    st.write("Response emails sent to the following addresses:")
    for email in st.session_state['sent_emails']:
        st.write(email)


