from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def check_ssh_version(task):
    result = task.run(task=send_command, command="show ip ssh")
    output = result.result

    if "SSH Enabled - version 2.0" in output:
        return "[OK] SSH version 2 enabled"
    else:
        return "[FAIL] SSH version 2 NOT enabled"

def check_ntp(task):
    result = task.run(task=send_command, command="show ntp status")
    output = result.result

    if "Clock is synchronized" in output:
        return "[OK] NTP synchronized"
    else:
        return "[FAIL] NTP NOT synchronized"

def check_ospf(task):
    result = task.run(task=send_command, command="show ip ospf neighbor")
    output = result.result

    if "FULL" in output:
        return "[OK] OSPF neighbors FULL"
    else:
        return "[FAIL] OSPF neighbors NOT FULL"

# Run compliance checks
result = nr.run(task=check_ssh_version)
print_result(result)



result = nr.run(task=check_ntp)

print_result(result)



result = nr.run(task=check_ospf)

print_result(result)
