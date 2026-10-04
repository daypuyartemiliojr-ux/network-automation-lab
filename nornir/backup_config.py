import os
from datetime import datetime
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

OUTPUT_DIR = "/home/automation/backups"
os.makedirs(OUTPUT_DIR, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

def backup_config(task):
    result = task.run(task=send_command, command="show running-config")
    hostname = task.host.name
    config = result.result

    filename = f"{OUTPUT_DIR}/{hostname}_nornir_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(config)

    return f"Saved to {filename}"

result = nr.run(task=backup_config)

print_result(result)
