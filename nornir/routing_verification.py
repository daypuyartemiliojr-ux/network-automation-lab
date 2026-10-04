from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def check_routing(task):
    result = task.run(task=send_command, command="show ip route summary")
    output = result.result

    return f"Routing table summary:\n{output}"

result = nr.run(task=check_routing)

print_result(result)
