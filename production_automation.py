#!/usr/bin/env python3
import os
import yaml
import logging
from datetime import datetime
from scrapli import Scrapli

INVENTORY_FILE = "/home/automation/inventory.yaml"
USERNAME = "admin"
PASSWORD = "C1sc0123"
SSH_CONFIG = "/home/automation/.ssh/config"
OUTPUT_DIR = "/home/automation/backups"
LOG_FILE = "/home/automation/automation.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    with open(INVENTORY_FILE) as f:
        inventory = yaml.safe_load(f)

    devices = inventory["devices"]

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"\n{'='*60}")
    print(f"Production Automation - {timestamp}")
    print(f"{'='*60}\n")

    success_count = 0
    fail_count = 0

    for device in devices:
        name = device["name"]
        host = device["host"]
        platform = device["platform"]
        role = device["role"]

        print(f"[*] Connecting to {name} ({host}) - {role}...")



        conn_params = {

            "host": host,

            "auth_username": USERNAME,

            "auth_password": PASSWORD,

            "auth_strict_key": False,

            "platform": platform,

            "transport": "system",

            "ssh_config_file": SSH_CONFIG,

        }



        try:

            conn = Scrapli(**conn_params)

            conn.open()

            output = conn.send_command("show ip interface brief")

            conn.close()



            filename = f"{OUTPUT_DIR}/{name}_{timestamp}.txt"

            with open(filename, "w") as f:

                f.write(output.result)



            print(f"    [OK] Success - saved to {filename}")

            logging.info(f"{name} ({host}) - SUCCESS")

            success_count += 1



        except Exception as e:

            print(f"    [FAIL] Failed - {e}")

            logging.error(f"{name} ({host}) - FAILED: {e}")

            fail_count += 1



    print(f"\n{'='*60}")

    print(f"SUMMARY: {success_count} success, {fail_count} failed")

    print(f"{'='*60}\n")



    logging.info(f"Automation complete: {success_count} success, {fail_count} failed")



if __name__ == "__main__":

    main() 
