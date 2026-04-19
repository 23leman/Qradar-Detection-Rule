import requests
import json
import urllib3

# SSL xəbərdarlıqlarını gizlətmək üçün
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Sənin QRadar məlumatların
QRADAR_IP = "16.170.165.124"
SEC_TOKEN = "18c4048c-20a8-4266-a65c-337a30341135"

headers = {
    "SEC": SEC_TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def deploy_rule(json_file_path):
    print(f"[*] Oxunur: {json_file_path}...")
    with open(json_file_path, 'r', encoding='utf-8') as file:
        rule_payload = json.load(file)
    
    url = f"https://{QRADAR_IP}/api/analytics/rules"
    
    print(f"[*] QRadar-a göndərilir: {rule_payload.get('name')}")
    response = requests.post(url, headers=headers, json=rule_payload, verify=False)
    
    if response.status_code in [200, 201]:
        print(f"✅ Uğurlu! Qayda QRadar-a yazıldı.")
    else:
        print(f"❌ Xəta! Status: {response.status_code}\nDetallar: {response.text}")

if __name__ == "__main__":
    # GitHub-dan yüklədiyimiz 1-ci qaydanın yolu (fayl eyni qovluqdadırsa, belə qalır)
    deploy_rule("rules/01_admin_group_add.json")
