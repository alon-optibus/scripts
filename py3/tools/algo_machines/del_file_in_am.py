from my.utils.algo_machines_1 import am_get_client
from sys import argv
from pathlib import Path

am_index = int(argv[1]) - 1
remote_path = Path(argv[2])

print(f'del from am{am_index+1}: "{remote_path}"')

ssh_client = am_get_client(am_index)

try:
    stdin, stdout, stderr = ssh_client.exec_command(f'rm -r {remote_path}')
finally:
    ssh_client.close()

########################################################################################################################
