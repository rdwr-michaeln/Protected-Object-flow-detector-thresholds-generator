"""
Email utility for sending reports with attachments.
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from typing import List, Optional
from config import CONFIG


class EmailSender:
    """Handles email sending functionality."""
    
    def __init__(self):
        """Initialize EmailSender with configuration from CONFIG."""
        self.smtp_server = CONFIG['SMTP_SERVER']
        self.smtp_port = CONFIG['SMTP_PORT']
        self.use_tls = CONFIG['SMTP_USE_TLS']
        self.username = CONFIG['SMTP_USERNAME']
        self.password = CONFIG['SMTP_PASSWORD']
        self.from_email = CONFIG['EMAIL_FROM']
    
    def send_report_email(self, filename: str, total_pos: int) -> bool:
        """Send email with the report file attached."""
        try:
            if not CONFIG['EMAIL_ENABLED']:
                print("Email sending is disabled in configuration.")
                return False
            
            if not os.path.exists(filename):
                print(f"Report file {filename} does not exist.")
                return False
            
            # Create message
            msg = self._create_message(filename, total_pos)
            
            # Attach file
            self._attach_file(msg, filename)
            
            # Send email
            return self._send_email(msg)
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def _create_message(self, filename: str, total_pos: int) -> MIMEMultipart:
        """Create the email message with headers and body."""
        msg = MIMEMultipart()
        
        # Email headers
        msg['From'] = self.from_email
        msg['To'] = ", ".join(CONFIG['EMAIL_TO'])
        if CONFIG['EMAIL_CC']:
            msg['Cc'] = ", ".join(CONFIG['EMAIL_CC'])
        msg['Subject'] = CONFIG['EMAIL_SUBJECT']
        
        # Email body
        body = self._format_email_body(total_pos)
        msg.attach(MIMEText(body, 'plain'))
        
        return msg
    
    def _format_email_body(self, total_pos: int) -> str:
        """Format the email body with dynamic content."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        threshold_percentage = int(CONFIG['THRESHOLD_PERCENTAGE'] * 100)
        
        return CONFIG['EMAIL_BODY_TEMPLATE'].format(
            date_time=current_time,
            total_pos=total_pos,
            days_lookback=CONFIG['DAYS_LOOKBACK'],
            threshold_percentage=threshold_percentage
        )
    
    def _attach_file(self, msg: MIMEMultipart, filename: str) -> None:
        """Attach the report file to the email."""
        with open(filename, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {os.path.basename(filename)}'
        )
        msg.attach(part)
    
    def _send_email(self, msg: MIMEMultipart) -> bool:
        """Send the email using SMTP."""
        try:
            print(f"📤 Connecting to SMTP server: {self.smtp_server}:{self.smtp_port}")
            # Create SMTP session
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            
            if self.use_tls:
                print("🔒 Enabling TLS encryption...")
                server.starttls()  # Enable encryption
            
            # Login only if username and password are provided
            if self.username and self.password:
                print("🔑 Authenticating...")
                server.login(self.username, self.password)
            else:
                print("📂 Using anonymous SMTP (no authentication)")
            
            text = msg.as_string()
            
            # Get all recipients (TO + CC)
            recipients = CONFIG['EMAIL_TO'] + CONFIG['EMAIL_CC']
            
            print(f"📨 Sending email to {len(recipients)} recipient(s)...")
            print(f"📧 Recipients: {', '.join(recipients)}")
            print(f"📎 Subject: {msg['Subject']}")
            
            server.sendmail(self.from_email, recipients, text)
            server.quit()
            
            print("=" * 50)
            print("✅ EMAIL SENT SUCCESSFULLY!")
            print(f"📤 From: {self.from_email}")
            print(f"📥 To: {', '.join(recipients)}")
            print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 50)
            return True
            
        except Exception as e:
            print("=" * 50)
            print("❌ EMAIL SENDING FAILED!")
            print(f"🚨 Error: {e}")
            print("=" * 50)
            return False
    
    def test_connection(self) -> bool:
        """Test SMTP connection and authentication."""
        try:
            print(f"Testing connection to {self.smtp_server}:{self.smtp_port}...")
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            if self.use_tls:
                server.starttls()
            
            # Only test login if username and password are provided
            if self.username and self.password:
                print("Testing authentication...")
                server.login(self.username, self.password)
                print("Authentication successful!")
            else:
                print("No authentication required (using anonymous SMTP).")
            
            server.quit()
            
            print("SMTP connection test successful!")
            return True
            
        except Exception as e:
            print(f"SMTP connection test failed: {e}")
            return False


def send_report_email(filename: str, total_pos: int) -> bool:
    """Convenience function to send report email."""
    if not CONFIG['EMAIL_ENABLED']:
        print("Email functionality is disabled.")
        return False
    
    email_sender = EmailSender()
    return email_sender.send_report_email(filename, total_pos)


def test_email_configuration() -> bool:
    """Test email configuration and connection."""
    if not CONFIG['EMAIL_ENABLED']:
        print("Email is disabled in configuration.")
        return False
    
    email_sender = EmailSender()
    return email_sender.test_connection()