from my.utils.algo_machines_1 import am_get_client
from sys import argv
from sys import stdout
from pathlib import Path
from scp import SCPClient

########################################################################################################################

am_index = int(argv[1]) - 1
local_path = Path(argv[2]).resolve(True)

if len(argv) > 3:
    remote_path = Path(argv[3])
else:
    remote_path = Path(str(local_path).replace(str(Path.home()), '~'))

print(f'src (local): "{local_path}"')
print(f'dst (am{am_index+1}): "{remote_path}"')

progress_width = 1


def progress(filename, size, sent):
    global progress_width
    msg = f'put: {filename} ({sent/size:.1%}*{size:,})'
    print(f'{msg:{progress_width}}', end='\r')
    progress_width = len(msg)


ssh_client = am_get_client(am_index)

remote_parent = str(remote_path.parent)

if remote_parent != '.':
    ssh_client.exec_command(f'mkdir -p {remote_parent}')

scp_client = SCPClient(
    ssh_client.get_transport(),
    progress=progress,
)

with scp_client as scp:
    scp.put(
        files=str(local_path),
        remote_path=str(remote_path),
        recursive=True,
    )

print(f'{"done":{progress_width}}')

########################################################################################################################
