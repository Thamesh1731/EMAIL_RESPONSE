# Automated Email Response System

This is a small project I built to save time replying to routine emails. It connects to my Gmail inbox, checks for unread messages, and sends back a simple acknowledgment automatically — all with a single click from a Streamlit web page.

---

## What It Does
- Logs into Gmail over IMAP  
- Finds unread messages in the inbox  
- Sends a polite “thanks, we’ll get back to you soon” email to each sender  
- Shows which addresses were responded to inside the Streamlit app

---

## How I Built It
The app is written in **Python** and uses:
- **Streamlit** for the simple one-page interface  
- **imaplib** and **smtplib** for reading and sending email  
- A **Queue** to handle processing in order

---

## Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/automated-email-response.git
   cd automated-email-response
   ```

2. **Install Streamlit**
   ```bash
   pip install streamlit
   ```

3. **Enable Gmail IMAP and create an App Password**
   - In Gmail Settings, turn on IMAP  
   - Generate an App Password (Google Account → Security → App passwords)

4. **Add your Gmail credentials**  
   In `app.py`, fill in:
   ```python
   GMAIL_USER = "your_email@gmail.com"
   GMAIL_PASS = "your_app_password"
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```
   Then click **Start Automatic Email Response** to scan unread emails and send replies.

---

## A Few Notes
- Keep your credentials safe — avoid pushing real passwords to GitHub.  
- The default reply is short and polite, but you can edit the `generate_response()` function to say whatever you want.  
- Works best when used for light “we received your message” auto-replies.

---

## Ideas for Later
- Multiple reply templates based on subject  
- Logging all responses to a CSV  
- A nicer dashboard for viewing history
