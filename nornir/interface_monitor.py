from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def check_interfaces(task):
    result = task.run(task=send_command, command="show ip interface brief")
    output = result.result

    down_interfaces = []
    for line in output.splitlines():
        if "administratively down" in line or " down " in line:
            down_interfaces.append(line.strip())

    if down_interfaces:
        return f"[WARNING] Down interfaces: {down_interfaces}"
    else:
        return "[OK] All interfaces up"

result = nr.run(task=check_interfaces)

print_result(result)
