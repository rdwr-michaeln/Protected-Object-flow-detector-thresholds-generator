"""
Cyber Controller Protected Objects Flow Detector Thresholds Report Generator

This script connects to a Cyber Controller, retrieves protected object flow detector 
thresholds and maximum values, then generates a formatted Excel report with analysis.
"""

import urllib3
from utils import collect_data, generate_filename, create_excel_report, send_email_report
from email_utils import test_email_configuration
from config import CONFIG

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    """Main function to orchestrate the report generation."""
    try:
        # Test email configuration if email is enabled
        if CONFIG['EMAIL_ENABLED']:
            print("Testing email configuration...")
            if not test_email_configuration():
                print("Email configuration test failed. Proceeding with report generation only.")
                print("Please check your email settings in config.py")
        
        # Collect data from Cyber Controller
        df = collect_data()
        
        if df.empty:
            print("No data to process. Exiting.")
            return
        
        # Generate timestamped filename
        filename = generate_filename()
        
        # Create and format Excel report
        create_excel_report(df, filename)
        
        print(f"\nReport generation completed successfully!")
        print(f"Report saved as: {filename}")
        
        # Send email if enabled and configured
        if CONFIG['EMAIL_ENABLED']:
            total_pos = len(df)
            email_success = send_email_report(filename, total_pos)
            
            if email_success:
                print(f"Report emailed to: {', '.join(CONFIG['EMAIL_TO'])}")
            else:
                print("Email sending failed, but report file is available locally.")
        else:
            print("Email sending is disabled.")
        
    except Exception as e:
        print(f"Error during report generation: {e}")
        raise


if __name__ == "__main__":
    main()