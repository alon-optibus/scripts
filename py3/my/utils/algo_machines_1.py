from _local__optiprod import *
from paramiko import SSHClient
from paramiko import RSAKey
from paramiko import AutoAddPolicy

OPTIPROD_KEY = RSAKey.from_private_key_file(str(OPTIPROD_KEY_FILE))


def am_get_client(am_index):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(ALGO_MACHINE_IP[am_index], username='ubuntu', pkey=OPTIPROD_KEY)
    return ssh


########################################################################################################################
