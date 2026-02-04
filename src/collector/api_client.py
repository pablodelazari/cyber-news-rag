import requests
import os
from datetime import datetime
from typing import List
from dotenv import load_dotenv
from loguru import logger
from .data_loader import VulnerabilityReport, ReportMetadata

# Ensure environment variables are loaded
load_dotenv()

class HackerOneAPIClient:
    def __init__(self):
        self.api_identifier = os.getenv("HACKERONE_API_IDENTIFIER")
        self.api_token = os.getenv("HACKERONE_API_TOKEN")
        self.base_url = "https://api.hackerone.com/v1"
        
        if not self.api_identifier or not self.api_token:
            logger.warning("HackerOne API credentials not found in environment variables. Real data fetch will fail.")

    def fetch_new_reports(self, limit: int = 10) -> List[VulnerabilityReport]:
        """
        Fetches reports using the official HackerOne API.
        Endpoint: /hackers/hacktivity
        """
        if not self.api_identifier or not self.api_token:
            logger.error("Cannot fetch from API: Missing credentials.")
            return []

        url = f"{self.base_url}/hackers/hacktivity"
        params = {
            "page[size]": limit,
            "queryString": "disclosed:true"
        }
        
        try:
            logger.info(f"Connecting to HackerOne API: {url}")
            response = requests.get(
                url, 
                auth=(self.api_identifier, self.api_token),
                params=params,
                timeout=15
            )
            
            if response.status_code == 401:
                logger.error("API Authentication Failed. Check your Identifier and Token.")
                return []
            
            response.raise_for_status()
            data = response.json()
            
            reports = []
            for item in data.get('data', []):
                attr = item.get('attributes', {})
                relationships = item.get('relationships', {})
                program_data = relationships.get('program', {}).get('data', {}).get('attributes', {})
                reporter_data = relationships.get('reporter', {}).get('data', {}).get('attributes', {})
                
                # Build a rich page_content for RAG context
                cve_list = attr.get('cve_ids') or []
                cve_str = ', '.join(cve_list) if cve_list else 'N/A'
                
                # Handle None values explicitly
                severity = attr.get('severity_rating') or 'unknown'
                title = attr.get('title') or 'Untitled'
                cwe = attr.get('cwe') or 'N/A'
                url = attr.get('url') or f"https://hackerone.com/reports/{item.get('id')}"
                
                page_content = f"""
Title: {title}
Severity: {severity}
Weakness/CWE: {cwe}
CVEs: {cve_str}
Program: {program_data.get('name') or 'Unknown'}
Reporter: {reporter_data.get('username') or 'Unknown'}
Votes: {attr.get('votes') or 0}
Bounty Awarded: ${attr.get('total_awarded_amount') or 0}
URL: {url}
"""
                
                report = VulnerabilityReport(
                    page_content=page_content.strip(),
                    metadata=ReportMetadata(
                        report_id=str(item.get('id') or 'unknown'),
                        title=title,
                        severity=severity,
                        bounty=float(attr.get('total_awarded_amount') or 0.0),
                        published_at=datetime.now(),
                        cve=cve_str,
                        attack_vector="Web",
                        technique=cwe,
                        link=url
                    )
                )
                reports.append(report)
                
            logger.info(f"Successfully fetched {len(reports)} reports via API.")
            return reports

        except Exception as e:
            logger.error(f"API Request failed: {e}")
            return []
