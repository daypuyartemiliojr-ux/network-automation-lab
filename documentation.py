import json
from scrapli import Scrapli

# ============================================================
# CONFIGURATION
# ============================================================

DEVICES = [
    {"name": "F1", "host": "10.255.12.5"},
    {"name": "S1", "host": "10.255.12.6"},
    {"name": "S2", "host": "10.255.12.102"},
    {"name": "S3", "host": "10.255.13.26"},
    {"name": "S4", "host": "10.255.12.22"},
    {"name": "E1", "host": "10.255.12.13"},
    {"name": "R1", "host": "10.255.12.14"},
    {"name": "C1", "host": "192.168.199.10"},
]

USERNAME = "admin"
PASSWORD = "C1sc0123"
SSH_CONFIG = "/home/automation/.ssh/config"

# ============================================================
# MAIN FUNCTION
# ============================================================

def main():
    documentation = {}

    for device in DEVICES:
        name = device["name"]
        host = device["host"]

        print(f"[*] Collecting data from {name} ({host})...")

        conn_params = {
            "host": host,
            "auth_username": USERNAME,

            "auth_password": PASSWORD,

            "auth_strict_key": False,

            "platform": "cisco_iosxe",

            "transport": "system",

            "ssh_config_file": SSH_CONFIG,

        }



        try:

            conn = Scrapli(**conn_params)

            conn.open()



            # Get hostname

            hostname = conn.send_command("show version").result



            # Get interfaces

            interfaces = conn.send_command("show ip interface brief").result



            # Get routing

            routing = conn.send_command("show ip route summary").result



            conn.close()



            documentation[name] = {

                "hostname": hostname,

                "interfaces": interfaces,

                "routing": routing,

            }



            print(f"    [OK] Collected data from {name}")



        except Exception as e:

            print(f"    [FAIL] {name}: {e}")



    # Save to JSON

    with open("/home/automation/backups/documentation.json", "w") as f:

        json.dump(documentation, f, indent=2)



    print(f"\n{'='*60}")

    print(f"Documentation saved to /home/automation/backups/documentation.json")

    print(f"{'='*60}\n")





if __name__ == "__main__":

    main()
