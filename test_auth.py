import json
from agent.telemetry_parser import parse_raw_log
from agent.incident_agent import IncidentMindAgent

def test_auth_alert():
    print("=" * 60)
    print("🧪 TESTING NEW ALERT: AUTH SERVICE CRASH")
    print("=" * 60)

    # Load synthetic log index 1 (Auth Service)
    with open("data/synthetic_logs.json", "r") as f:
        logs = json.load(f)

    auth_alert = parse_raw_log(json.dumps(logs[1]))
    agent = IncidentMindAgent(service_name=auth_alert.service)

    # 1. Cold Diagnosis
    alert_prompt = auth_alert.to_formatted_prompt()
    diagnosis = agent.diagnose_incident(alert_prompt)
    print("\n--- AGENT DIAGNOSIS ---")
    print(diagnosis)

    # 2. Retain New Memory
    agent.learn_post_mortem(
        incident_id="INC-500-JWT",
        root_cause="JWT secret cache missed sync across worker thread #4 under heavy load.",
        fix_applied="Implemented atomic token cache sync with Redis Pub/Sub in auth_worker.py."
    )

if __name__ == "__main__":
    test_auth_alert()
