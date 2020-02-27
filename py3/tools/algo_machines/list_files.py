from my.utils.algo_machines_1 import am_get_client
from sys import argv

########################################################################################################################

am_index = int(argv[1]) - 1
args = ' '.join(argv[2:])

ssh_client = am_get_client(am_index)

try:
    stdin, stdout, stderr = ssh_client.exec_command(f'ls -lF {args}')

    for line in stdout:
        print(line.strip())

finally:
    ssh_client.close()

########################################################################################################################
