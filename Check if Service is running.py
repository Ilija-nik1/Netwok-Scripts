import subprocess
remote_ip = "xxx.xxx.xxx.xxx"
service_name = "Service_Name"

check_service = None

try:
  check_service = subprocess.check_output(
    ["ssh", remote_ip, "service", service_name, "status"]
  ).decode().strip()
except Exception as e:
  print(f'[ERROR] {e}')

if 'running' in check_service.lower():
  print(f'{service_name} service on the {remote_ip} is running.')
elif 'stopped' in check_service.lower():
  print(f'{service_name} service on the {remote_ip} is stopped.')
else:
  print(f'{service_name} service on the {remote_ip} is in an unknown state.')