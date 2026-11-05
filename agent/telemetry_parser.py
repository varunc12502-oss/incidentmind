import json
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class TelemetryAlert(BaseModel):
    service: str = Field(..., description="Target microservice name")
    environment: str = Field(default="production", description="Environment stage")
    error_code: str = Field(..., description="HTTP or System Error Code")
    message: str = Field(..., description="Error message or exception text")
    stack_trace: str = Field(..., description="Raw stack trace or system log output")
    metadata: Optional[Dict[str, Any]] = None

    def to_formatted_prompt(self) -> str:
        return f"""
SERVICE: {self.service} ({self.environment})
ERROR CODE: {self.error_code}
MESSAGE: {self.message}
STACK TRACE:
{self.stack_trace}
"""

def parse_raw_log(raw_json: str) -> TelemetryAlert:
    data = json.loads(raw_json)
    return TelemetryAlert(**data)
