import os
import json
import asyncio
from dotenv import load_dotenv
from hindsight_client import Hindsight
from groq import Groq

load_dotenv()

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "production-incident-memory")

hindsight = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=HINDSIGHT_API_KEY
)
groq_client = Groq(api_key=GROQ_API_KEY)

class IncidentMindAgent:
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.bank_id = BANK_ID

    def diagnose_incident(self, alert_text: str) -> str:
        print(f"\n🔍 Querying Hindsight Memory Bank [{self.bank_id}]...")
        
        memory_query = f"What past incidents, runbooks, or root cause fixes exist for service {self.service_name} related to: {alert_text}?"
        try:
            reflection = hindsight.reflect(bank_id=self.bank_id, query=memory_query)
            memory_context = getattr(reflection, "text", str(reflection))
        except Exception as e:
            memory_context = "No prior memory found or first-time run."
            print(f"⚠️ Hindsight Memory Note: {e}")

        print(f"🧠 Retained Memory Context:\n{memory_context}\n")

        system_prompt = f"""
You are IncidentMind, an Autonomous DevOps SRE Agent.

PAST INFRASTRUCTURE MEMORIES & RCAs:
{memory_context}

TASK:
Analyze the incoming alert. If past memory contains a matching pattern or verified fix, state it immediately.
Provide:
1. Immediate Root Cause Diagnosis
2. Exact Fix / Actionable Patch
3. Prevention Recommendation
"""

        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"ALERT TELEMETRY:\n{alert_text}"}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    def learn_post_mortem(self, incident_id: str, root_cause: str, fix_applied: str):
        post_mortem_text = f"""
[INCIDENT POST-MORTEM]
ID: {incident_id}
Service: {self.service_name}
Root Cause: {root_cause}
Verified Fix: {fix_applied}
Status: Resolved & Saved to Long-Term Memory
"""
        hindsight.retain(
            bank_id=self.bank_id,
            content=post_mortem_text
        )
        print(f"✅ Successfully retained post-mortem [{incident_id}] into Hindsight Bank [{self.bank_id}].")

    def close(self):
        """Closes async Hindsight client sessions cleanly."""
        try:
            if hasattr(hindsight, 'close'):
                hindsight.close()
        except Exception:
            pass
