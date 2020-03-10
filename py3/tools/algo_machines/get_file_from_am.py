from my.utils.algo_machines_1 import am_get_client
from sys import argv
from pathlib import Path
from scp import SCPClient

########################################################################################################################

am_index = int(argv[1]) - 1
remote_path = Path(argv[2])

if len(argv) > 3:
    local_path = Path(argv[3]).resolve()
else:
    local_path = remote_path

if local_path.is_file():
    local_path.unlink()

elif local_path.is_dir():
    local_path = local_path.joinpath(remote_path.name)

print(f'src (am{am_index+1}): "{remote_path}"')
print(f'dst (local): "{local_path}"')

progress_width = 1


def progress(filename, size, sent):
    global progress_width
    msg = f'get: {filename} ({sent/size:.1%}*{size:,})'
    print(f'{msg:{progress_width}}', end='\r')
    progress_width = len(msg)


ssh_client = am_get_client(am_index)

scp_client = SCPClient(
    ssh_client.get_transport(),
    progress=progress,
)

with scp_client as scp:
    scp.get(
        remote_path=str(remote_path),
        local_path=str(local_path),
        recursive=True,
    )

print(f'{"done":{progress_width}}')

########################################################################################################################
