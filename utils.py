"""
Utility functions for data collection and report generation.
"""

import pandas as pd
from datetime import datetime
from cc_connector import CcConnector
from excel_formatter import ExcelReportFormatter
from email_utils import send_report_email
from config import CONFIG


def collect_data() -> pd.DataFrame:
    """Collect protected object data and maximum values."""
    print("Connecting to Cyber Controller...")
    cc = CcConnector()
    
    print("Retrieving protected objects...")
    df = cc.get_protected_objects()
    
    if df.empty:
        print("No protected objects found or error occurred.")
        return df
    
    print(f"Found {len(df)} protected objects. Retrieving maximum values...")
    
    # Get max values for each protected object
    for idx, po_name in enumerate(df["PO Name"]):
        print(f"Processing {idx + 1}/{len(df)}: {po_name}")
        max_df = cc.get_max_values_for_po(po_name)
        
        if not max_df.empty:
            for col in max_df.columns:
                df.loc[df["PO Name"] == po_name, col] = max_df.iloc[0][col]
    
    return df


def generate_filename() -> str:
    """Generate a timestamped filename."""
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{CONFIG['OUTPUT_FILENAME_PREFIX']}_{current_time}.xlsx"


def create_excel_report(dataframe: pd.DataFrame, filename: str) -> None:
    """Create and format the Excel report."""
    print(f"Creating Excel report: {filename}")
    
    # Save DataFrame to Excel
    dataframe.to_excel(filename, index=False, engine='openpyxl')
    
    # Apply formatting
    formatter = ExcelReportFormatter(filename)
    formatter.format_report(dataframe)
    formatter.save(filename)
    
    print(f"Data saved to {filename} with formatting")


def send_email_report(filename: str, total_pos: int) -> bool:
    """Send the generated report via email."""
    if not CONFIG['EMAIL_ENABLED']:
        print("Email sending is disabled.")
        return False
    
    print("Sending email with report attachment...")
    success = send_report_email(filename, total_pos)
    
    if success:
        print("Email sent successfully!")
    else:
        print("Failed to send email.")
    
    return success