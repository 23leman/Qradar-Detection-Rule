import os
import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QRADAR_HOST = os.environ.get("QRADAR_HOST")
QRADAR_TOKEN = os.environ.get("QRADAR_TOKEN")

HEADERS = {
    "SEC": QRADAR_TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

BASE_URL = f"https://{QRADAR_HOST}/api"

def get_existing_rules():
    url = f"{BASE_URL}/analytics/rules"
    response = requests.get(url, headers=HEADERS, verify=False)
    if response.status_code == 200:
        return {rule["name"]: rule["id"] for rule in response.json()}
    return {}

def create_rule(rule_data):
    existing_rules = get_existing_rules()
    rule_name = rule_data["name"]

    if rule_name in existing_rules:
        rule_id = existing_rules[rule_name]
        url = f"{BASE_URL}/analytics/rules/{rule_id}"
        response = requests.post(url, headers=HEADERS, json=rule_data, verify=False)
        action = "Updated"
    else:
        url = f"{BASE_URL}/analytics/rules"
        response = requests.post(url, headers=HEADERS, json=rule_data, verify=False)
        action = "Created"

    if response.status_code in [200, 201]:
        print(f"{action} rule: {rule_name}")
    else:
        print(f"Failed {rule_name}: {response.status_code} - {response.text}")

def main():
    rules_dir = "rules"
    for filename in sorted(os.listdir(rules_dir)):
        if filename.endswith(".json"):
            filepath = os.path.join(rules_dir, filename)
            with open(filepath, "r") as f:
                rule_data = json.load(f)
            create_rule(rule_data)

if __name__ == "__main__":
    main()
