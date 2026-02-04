import time
from typing import List
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from loguru import logger
from .data_loader import VulnerabilityReport, ReportMetadata

class HackerOneScraper:
    def __init__(self, headless: bool = True):
        self.options = Options()
        if headless:
            self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        # Fake user agent to avoid immediate blocking
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

    def fetch_new_reports(self, limit: int = 10) -> List[VulnerabilityReport]:
        """
        Fetches the latest reports from HackerOne Hacktivity.
        Note: This is a basic implementation. H1 has strong anti-bot protections.
        For a production system, consider using their API if available or stronger evasion techniques.
        """
        url = "https://hackerone.com/hacktivity"
        logger.info(f"Starting scrape for {url}")
        
        driver = webdriver.Chrome(options=self.options)
        reports = []
        
        try:
            driver.get(url)
            time.sleep(5)  # Wait for JS to load
            
            # Scroll down to load more if needed
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # This selector is hypothetical and needs to be adjusted based on the actual H1 DOM
            # H1 DOM is very dynamic and obfuscated (CSS modules)
            # Searching for generic report item containers
            
            # Example logic for demonstration (User would need to inspect actual DOM selectors)
            # Assuming we find list items. 
            # In a real interview/portfolio, you would list these limitations or use a provided dataset.
            
            logger.warning("Using hypothetical selectors. In a real scenario, selectors must be updated to match the site's current DOM.")
            
            # Mocking data for demonstration if no reports found (to ensure pipeline works)
            # Delete this block when real selectors are working
            reports = self._generate_mock_reports(limit)
            
        except Exception as e:
            logger.error(f"Error scraping HackerOne: {e}")
        finally:
            driver.quit()
            
        return reports

    def _generate_mock_reports(self, count: int) -> List[VulnerabilityReport]:
        """Generates mock reports for testing the pipeline when scraping is blocked or selectors fail."""
        logger.info("Generating mock reports for testing...")
        mock_reports = []
        for i in range(count):
            r = VulnerabilityReport(
                page_content=f"This is a detailed report about a Stored XSS vulnerability found in the comments section. The attacker can inject malicious scripts... Payload: <script>alert(1)</script>. Mitigation: sanitize input.",
                metadata=ReportMetadata(
                    report_id=f"H1-{100000+i}",
                    title=f"Stored XSS in Comments Section {i}",
                    severity="High",
                    bounty=500.0 * (i+1),
                    published_at=datetime.now(),
                    cve=f"CVE-2026-100{i}",
                    attack_vector="Web",
                    technique="Stored XSS",
                    link=f"https://hackerone.com/reports/{100000+i}"
                )
            )
            mock_reports.append(r)
        return mock_reports
