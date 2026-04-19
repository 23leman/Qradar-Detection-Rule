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
    "Accept": "application/json",
    "Version": "12.0"
}

BASE_URL = f"https://{QRADAR_HOST}/api"

def get_existing_rules():
    url = f"{BASE_URL}/analytics/rules?fields=id,name"
    response = requests.get(url, headers=HEADERS, verify=False)
    if response.status_code == 200:
        return {rule["name"]: rule["id"] for rule in response.json()}
    print(f"Failed to get rules: {response.status_code} - {response.text}")
    return {}

def update_rule(rule_id, rule_data):
    url = f"{BASE_URL}/analytics/rules/{rule_id}"
    response = requests.post(url, headers=HEADERS, json=rule_data, verify=False)
    return response

def create_offense_rule(rule_data):
    existing_rules = get_existing_rules()
    rule_name = rule_data["name"]

    if rule_name in existing_rules:
        rule_id = existing_rules[rule_name]
        response = update_rule(rule_id, rule_data)
        if response.status_code in [200, 201]:
            print(f"Updated rule: {rule_name}")
        else:
            print(f"Failed to update {rule_name}: {response.status_code}")
    else:
        print(f"Rule '{rule_name}' logged to QRadar (manual creation required via UI)")

def main():
    rules_dir = "rules"
    for filename in sorted(os.listdir(rules_dir)):
        if filename.endswith(".json"):
            filepath = os.path.join(rules_dir, filename)
            with open(filepath, "r") as f:
                rule_data = json.load(f)
            create_offense_rule(rule_data)
            print(f"Processed: {filename}")

if __name__ == "__main__":
    main()
