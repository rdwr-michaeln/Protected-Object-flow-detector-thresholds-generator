"""
Configuration settings for the Cyber Controller report generator.
"""

# Configuration
CONFIG = {
    # Cyber Controller HA Configuration
    'PRIMARY_URL': "https://10.213.50.130",    # Primary CC server
    'SECONDARY_URL': "https://10.213.50.140",  # Secondary CC server (backup)
    'DEFAULT_USERNAME': "radware", 
    'DEFAULT_PASSWORD': "radware1!",
    'DAYS_LOOKBACK': 7,
    'THRESHOLD_PERCENTAGE': 0.8,  # 80% threshold for highlighting
    'OUTPUT_FILENAME_PREFIX': "po_flow_detector_thresholds",
    
    # Email Configuration
    'EMAIL_ENABLED': True,  # Set to False to disable email sending
    'SMTP_SERVER': "10.251.0.28",  # Change to your SMTP server
    'SMTP_PORT': 25,  # Common ports: 587 (TLS), 465 (SSL), 25 (unsecured)
    'SMTP_USE_TLS': False,  # Set to False for SSL or no encryption
    'SMTP_USERNAME': "",  # Empty for no authentication
    'SMTP_PASSWORD': "",  # Empty for no authentication
    
    # Email Content
    'EMAIL_FROM': "ILCyberController@radwaretraininglab.com",  # Sender email
    'EMAIL_TO': ["michaeln@radware.com"],  # List of recipient emails
    'EMAIL_CC': [],  # Optional CC recipients
    'EMAIL_SUBJECT': "Cyber Controller - Protected Objects Flow Detector Report",
    'EMAIL_BODY_TEMPLATE': """
Hello,

Please find attached the Protected Objects Flow Detector Thresholds Report generated on {date_time}.

Report Summary:
- Total Protected Objects: {total_pos}
- Report Period: Last {days_lookback} days
- Threshold Violations Highlighted: {threshold_percentage}% of maximum values

The report includes:
- Current activation thresholds for TCP, UDP, ICMP, and Total traffic
- Maximum observed values for the last {days_lookback} days
- Highlighted rows indicate thresholds below {threshold_percentage}% of observed maximums

Best regards,
Cyber Controller Report System
"""
}