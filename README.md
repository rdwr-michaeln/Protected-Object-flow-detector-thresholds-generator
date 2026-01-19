# Cyber Controller Protected Objects Flow Detector Report Generator

A Python application that connects to a Cyber Controller, retrieves protected object flow detector thresholds and maximum traffic values, then generates a formatted Excel report with threshold violation analysis and optional email delivery.

## Features

- **Automated Data Collection**: Connects to Cyber Controller API to retrieve protected object configurations and traffic statistics
- **Excel Report Generation**: Creates professionally formatted Excel reports with:
  - Current flow detector thresholds
  - Maximum observed traffic values (last 7 days)
  - Color-coded highlighting for threshold violations
  - Auto-adjusted column widths
- **Email Integration**: Automatically sends reports via SMTP with customizable templates
- **Threshold Analysis**: Highlights protected objects where activation thresholds are below 80% of observed maximums
- **Modular Design**: Clean, maintainable code structure with separate modules

## Project Structure

```
project/
├── main.py              # Main entry point
├── config.py            # Configuration settings
├── cc_connector.py      # Cyber Controller API interface
├── excel_formatter.py   # Excel report formatting
├── email_utils.py       # Email functionality
├── utils.py            # Utility functions
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Installation

### Prerequisites
- Python 3.7 or higher
- Access to a Cyber Controller instance
- SMTP server access (if email functionality is desired)

### Setup Steps

1. **Clone or download the project files**
   ```bash
   cd your-project-directory
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the application** (see Configuration section below)

## Configuration

### Basic Configuration

Edit `config.py` to configure your environment:

```python
CONFIG = {
    # Cyber Controller Settings
    'BASE_URL': "https://your-cc-server.com",
    'DEFAULT_USERNAME': "your-username",
    'DEFAULT_PASSWORD': "your-password",
    
    # Report Settings
    'DAYS_LOOKBACK': 7,                    # Days to look back for max values
    'THRESHOLD_PERCENTAGE': 0.8,           # 80% threshold for highlighting
    'OUTPUT_FILENAME_PREFIX': "po_flow_detector_thresholds",
    
    # Email Settings (optional)
    'EMAIL_ENABLED': True,                 # Set to False to disable email
    'SMTP_SERVER': "smtp.your-domain.com",
    'SMTP_PORT': 587,
    'SMTP_USERNAME': "your-email@domain.com",
    'SMTP_PASSWORD': "your-password",
    'EMAIL_TO': ["recipient@domain.com"],
    # ... more email settings
}
```

### Email Configuration Examples

**Gmail (with App Password):**
```python
'SMTP_SERVER': "smtp.gmail.com",
'SMTP_PORT': 587,
'SMTP_USE_TLS': True,
'SMTP_USERNAME': "your-email@gmail.com",
'SMTP_PASSWORD': "your-app-password",  # Generate at https://myaccount.google.com/apppasswords
```

**Microsoft 365/Outlook:**
```python
'SMTP_SERVER': "smtp.office365.com",
'SMTP_PORT': 587,
'SMTP_USE_TLS': True,
'SMTP_USERNAME': "your-email@company.com",
'SMTP_PASSWORD': "your-password",
```

**Corporate Exchange Server:**
```python
'SMTP_SERVER': "mail.yourcompany.com",
'SMTP_PORT': 25,  # or 587
'SMTP_USE_TLS': True,
'SMTP_USERNAME': "your-username",
'SMTP_PASSWORD': "your-password",
```

## Usage

### Running the Report

```bash
python main.py
```

### What the Script Does

1. **Connects** to your Cyber Controller server
2. **Retrieves** all protected objects and their flow detector thresholds
3. **Collects** maximum traffic values for each protocol (TCP, UDP, ICMP, Total) over the last 7 days
4. **Generates** an Excel report with:
   - Current activation thresholds
   - Maximum observed values
   - Color-coded highlighting for potential issues
5. **Sends email** (if configured) with the report attached

### Sample Output

```
Connecting to Cyber Controller...
Login successful
Retrieving protected objects...
Found 25 protected objects. Retrieving maximum values...
Processing 1/25: web-server-01
Processing 2/25: database-server
...
Creating Excel report: po_flow_detector_thresholds_2026-01-19_14-30-25.xlsx
Data saved to po_flow_detector_thresholds_2026-01-19_14-30-25.xlsx with formatting
Testing email configuration...
SMTP connection test successful!
Sending email with report attachment...
Email sent successfully to: admin@company.com, security@company.com

Report generation completed successfully!
Report saved as: po_flow_detector_thresholds_2026-01-19_14-30-25.xlsx
```

## Report Details

### Excel Report Structure

The generated Excel file contains:

| Column | Description |
|--------|-------------|
| PO Name | Protected Object name |
| TCP Activation Mbps | Current TCP Mbps threshold |
| TCP Activation PPS | Current TCP PPS threshold |
| UDP Activation Mbps | Current UDP Mbps threshold |
| UDP Activation PPS | Current UDP PPS threshold |
| ICMP Activation Mbps | Current ICMP Mbps threshold |
| ICMP Activation PPS | Current ICMP PPS threshold |
| Total Activation Mbps | Current Total Mbps threshold |
| Total Activation PPS | Current Total PPS threshold |
| TCP Max BPS | Maximum TCP traffic observed (Mbps) |
| TCP Max PPS | Maximum TCP packets observed (PPS) |
| ... | Additional max values for UDP, ICMP, Total |

### Color Coding

- **Green Header**: Current Thresholds section
- **Yellow Header**: Maximum Values section  
- **Blue Header**: Column headers
- **Red Rows**: Protected objects where any activation threshold is below 80% of the observed maximum

### Threshold Logic

The system highlights rows where:
- Any activation threshold < (80% × corresponding maximum value)
- Only compares configured thresholds (empty/zero thresholds are ignored)

## Troubleshooting

### Common Issues

**Login Failed:**
- Verify BASE_URL, username, and password in config.py
- Check network connectivity to Cyber Controller
- Ensure user has appropriate API permissions

**Email Sending Failed:**
- Verify SMTP settings in config.py
- Check if firewall blocks SMTP ports
- For Gmail: Use App Password instead of account password
- Test email configuration: set EMAIL_ENABLED to True and run script

**No Data Retrieved:**
- Check if protected objects exist in Cyber Controller
- Verify user has permission to view protected object configurations
- Check API endpoint availability

**Module Import Errors:**
- Run: `pip install -r requirements.txt`
- Ensure all project files are in the same directory

### Disable Email Temporarily

Set in `config.py`:
```python
'EMAIL_ENABLED': False,
```

## Security Considerations

- Store sensitive credentials securely (consider environment variables)
- Use App Passwords for Gmail instead of account passwords
- Regularly rotate API credentials
- Restrict network access to trusted sources
- Consider using encrypted password storage

## Customization

### Modify Report Appearance

Edit `excel_formatter.py` to customize:
- Colors and styling
- Column widths
- Additional formatting rules

### Change Threshold Logic

Edit `_should_highlight_row()` in `excel_formatter.py` to modify:
- Threshold percentage (currently 80%)
- Which protocols to compare
- Highlighting conditions

### Modify Email Template

Edit the `EMAIL_BODY_TEMPLATE` in `config.py` to customize:
- Email subject and content
- Dynamic variables
- Formatting

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify configuration settings
3. Review log output for specific error messages
4. Test individual components (email, API connection) separately

## Version History

- **v1.0**: Initial release with basic report generation
- **v1.1**: Added email functionality and improved error handling
- **v1.2**: Enhanced threshold logic to skip unconfigured values