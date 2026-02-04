from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import json

class ReportMetadata(BaseModel):
    report_id: str
    title: str
    severity: str = Field(default="unknown")
    bounty: float = Field(default=0.0)
    published_at: datetime
    cve: Optional[str] = None
    attack_vector: Optional[str] = None
    technique: Optional[str] = None
    link: str

class VulnerabilityReport(BaseModel):
    page_content: str
    metadata: ReportMetadata

    def to_dict(self):
        return self.model_dump(mode='json')

class DataLoader:
    @staticmethod
    def save_raw(reports: List[VulnerabilityReport], filepath: str):
        data = [r.to_dict() for r in reports]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def load_raw(filepath: str) -> List[VulnerabilityReport]:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [VulnerabilityReport(**item) for item in data]
