
import json
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def collect_inventory(task):
    # Get hostname
    hostname_result = task.run(task=send_command, command="show version")
    hostname_output = hostname_result.result

    # Get interfaces
    interface_result = task.run(task=send_command, command="show ip interface brief")
    interface_output = interface_result.result

    # Get routing table
    routing_result = task.run(task=send_command, command="show ip route summary")
    routing_output = routing_result.result

    return {
        "hostname": task.host.name,
        "ip": task.host.hostname,
        "platform": task.host.platform,
        "version": hostname_output,
        "interfaces": interface_output,
        "routing": routing_output,
    }

result = nr.run(task=collect_inventory)

# Save to JSON
inventory = {}
for host, task_result in result.items():
    inventory[host] = task_result[0].result



with open("/home/automation/backups/inventory.json", "w") as f:

    json.dump(inventory, f, indent=2)



print_result(result)
