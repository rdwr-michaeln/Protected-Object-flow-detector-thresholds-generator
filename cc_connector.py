"""
Cyber Controller connector for API interactions.
"""

import requests
import pandas as pd
import math
from datetime import datetime, timedelta, timezone
from typing import Dict
from config import CONFIG


class CcConnector:
    """Handles connection and data retrieval from Cyber Controller."""
    
    def __init__(self, username: str = None, password: str = None):
        """Initialize CcConnector with credentials."""
        self.base_url = CONFIG['BASE_URL']
        self.username = username or CONFIG['DEFAULT_USERNAME']
        self.password = password or CONFIG['DEFAULT_PASSWORD']
        self.session = requests.Session()
        self.login()

    def login(self) -> bool:
        """Authenticate with the Cyber Controller."""
        try:
            url = f"{self.base_url}/mgmt/system/user/login"
            payload = {"username": self.username, "password": self.password}
            response = self.session.post(url, json=payload, verify=False)
            
            if response.status_code == 200:
                print("Login successful")
                return True
            else:
                print(f"Login failed with status code: {response.status_code}")
                if response.text:
                    print(f"Login error response: {response.text[:200]}...")
                return False
        except Exception as e:
            print(f"Exception during login: {e}")
            return False
    
    def get_protected_objects(self) -> pd.DataFrame:
        """Retrieve protected objects and their flow detector thresholds."""
        try:
            url = f"{self.base_url}/mgmt/v2/device/df/restv2/protected-objects/configure/security-settings/?includeNameSort=false"
            payload = {"protectedObjectNames": []}
            response = self.session.post(url, json=payload, verify=False)
            
            if response.status_code != 200:
                print(f"Failed to retrieve PO data with status code: {response.status_code}")
                if response.text:
                    print(f"PO data error response: {response.text[:200]}...")
                return pd.DataFrame()
            
            try:
                response_json = response.json()
            except Exception as json_error:
                print(f"Failed to parse JSON: {json_error}")
                print(f"Response content: {response.text[:500]}")
                return pd.DataFrame()
            
            if response_json is None:
                print("Response is not valid JSON")
                return pd.DataFrame()
            
            return self._parse_protected_objects_response(response_json)
            
        except Exception as e:
            print(f"Exception during PO retrieval: {e}")
            return pd.DataFrame()
    
    def _parse_protected_objects_response(self, response_json: Dict) -> pd.DataFrame:
        """Parse the protected objects API response into a DataFrame."""
        po_details = []
        po_data = response_json.get("protectedObjects", [])
        
        for po_item in po_data:
            po_name = po_item.get("name", "")
            flow_details = po_item.get("flowDetectorThresholdsHostDetails") or {}
            
            po_details.append({
                "PO Name": po_name,
                "TCP Activation Mbps": flow_details.get("tcpMbps", ""),
                "TCP Activation PPS": flow_details.get("tcpPps", ""),
                "UDP Activation Mbps": flow_details.get("udpMbps", ""),
                "UDP Activation PPS": flow_details.get("udpPps", ""),
                "ICMP Activation Mbps": flow_details.get("icmpMbps", ""),
                "ICMP Activation PPS": flow_details.get("icmpPps", ""),
                "Total Activation Mbps": flow_details.get("totalMbps", ""),
                "Total Activation PPS": flow_details.get("totalPps", "")
            })
        
        return pd.DataFrame(po_details)

    def get_max_values_for_po(self, po_name: str) -> pd.DataFrame:
        """Get maximum traffic values for a protected object over the last 7 days."""
        protocols = ["tcp", "udp", "icmp", "total"]
        po_max_values = {}
        
        for protocol in protocols:
            max_values = self._get_protocol_max_values(po_name, protocol)
            po_max_values.update(max_values)
        
        print(f"Max values for {po_name}: {po_max_values}")
        return pd.DataFrame([po_max_values])
    
    def _get_protocol_max_values(self, po_name: str, protocol: str) -> Dict[str, int]:
        """Get maximum BPS and PPS values for a specific protocol."""
        url = f"{self.base_url}/mgmt/vrm/top-talkers/flow-detector/{protocol}"
        payload = {
            "protectedObjectName": po_name,
            "timeInterval": {
                "from": int((datetime.now(timezone.utc) - timedelta(days=CONFIG['DAYS_LOOKBACK'])).timestamp() * 1000),
                "to": None
            }
        }
        
        try:
            response = self.session.post(url, json=payload, verify=False)
            if response.status_code != 200:
                print(f"Failed to retrieve {protocol} max data for PO {po_name} with status code: {response.status_code}")
                return {}
            
            data_map = response.json().get("dataMap", {})
            incoming = data_map.get("incoming", {})
            
            bps_list = incoming.get("bps", [])
            max_bps = max((float(item["row"]["value"]) for item in bps_list), default=0) if bps_list else 0
            
            pps_list = incoming.get("pps", [])
            max_pps = max((float(item["row"]["value"]) for item in pps_list), default=0) if pps_list else 0
            
            # Convert to Mbps and round up
            max_bps_mbps = math.ceil(max_bps / 1024 / 1024)
            max_pps_rounded = math.ceil(max_pps)
            
            protocol_upper = protocol.upper()
            return {
                f"{protocol_upper} Max BPS": max_bps_mbps,
                f"{protocol_upper} Max PPS": max_pps_rounded
            }
            
        except Exception as e:
            print(f"Error getting {protocol} max values for {po_name}: {e}")
            return {}