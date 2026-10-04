from scrapli import Scrapli

device = {
    "host": "10.255.12.5",
    "auth_username": "admin",
    "auth_password": "C1sc0123",
    "auth_strict_key": False,
    "platform": "cisco_iosxe",
    "transport": "system",
    "ssh_config_file": "/home/automation/.ssh/config",  # <--- IDAGDAG ITO
}

try:
    conn = Scrapli(**device)
    conn.open()
    output = conn.send_command("show ip interface brief")
    print(output.result)
    conn.close()
    print("Scrapli test successful!")
except Exception as e:
    print(f"Error: {e}")
