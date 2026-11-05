import json
from agent.telemetry_parser import parse_raw_log
from agent.incident_agent import IncidentMindAgent

def run_demo():
    print("=" * 60)
    print("🚀 INCIDENTMIND: AUTONOMOUS SRE AGENT DEMO")
    print("=" * 60)

    with open("data/synthetic_logs.json", "r") as f:
        logs = json.load(f)

    payment_alert = parse_raw_log(json.dumps(logs[0]))
    agent = IncidentMindAgent(service_name=payment_alert.service)

    print("\n--- PHASE 1: FIRST INCIDENT (Cold Memory Run) ---")
    alert_prompt = payment_alert.to_formatted_prompt()
    diagnosis_1 = agent.diagnose_incident(alert_prompt)
    print("--- AGENT DIAGNOSIS (Cold Run) ---")
    print(diagnosis_1)

    print("\n" + "=" * 60)
    print("--- PHASE 2: SRE TRAINS AGENT VIA POST-MORTEM ---")
    print("=" * 60)
    agent.learn_post_mortem(
        incident_id="INC-504-REDIS",
        root_cause="Redis connection pool maxed out at 100 under flash sale traffic.",
        fix_applied="Increased max_connections to 500 and configured connection pool recycling in redis_config.py."
    )

    print("\n" + "=" * 60)
    print("--- PHASE 3: SIMILAR INCIDENT (Warm Memory Recall) ---")
    print("=" * 60)
    diagnosis_2 = agent.diagnose_incident(alert_prompt)
    print("--- AGENT DIAGNOSIS (Warm Run - Instant Recall) ---")
    print(diagnosis_2)

if __name__ == "__main__":
    run_demo()
