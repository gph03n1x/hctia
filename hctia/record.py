import os.path
import tempfile

import paramiko


def retrieve_authorized_keys(
    host: str, port: int, username: str, target: str, ssh_key: str
):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        host,
        port,
        username=username,
        allow_agent=True,
        key_filename=ssh_key,
        timeout=10,
    )
    sftp = ssh.open_sftp()

    temp = tempfile.NamedTemporaryFile(mode="w+")
    sftp.get(target, temp.name)
    sftp.close()
    ssh.close()

    return temp


def upload_authorized_keys(
    host: str,
    port: int,
    username: str,
    file: tempfile.NamedTemporaryFile,
    target: str,
    ssh_key: str,
):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        host,
        port,
        username=username,
        allow_agent=True,
        key_filename=ssh_key,
        timeout=10,
    )
    sftp = ssh.open_sftp()

    sftp.put(file.name, target)
    sftp.close()
    ssh.close()

    file.close()


def mkdir_p(sftp, remote_directory):
    """Change to this directory, recursively making new folders if needed.
    Returns True if any folders were created."""
    if remote_directory == "/":
        # absolute path so change directory to root
        sftp.chdir("/")
        return
    if remote_directory == "":
        # top-level relative directory must exist
        return
    try:
        sftp.chdir(remote_directory)  # sub-directory exists
    except IOError:
        dirname, basename = os.path.split(remote_directory.rstrip("/"))
        mkdir_p(sftp, dirname)  # make parent directories
        sftp.mkdir(basename)  # sub-directory missing, so created it
        sftp.chdir(basename)
        return True


def connect_and_execute_command(
    host: str, port: int, username: str, ssh_key: str, command: str
):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        host,
        port,
        username=username,
        allow_agent=True,
        key_filename=ssh_key,
        timeout=10,
    )
    sftp = ssh.open_sftp()
    bash_file = tempfile.NamedTemporaryFile(mode="w+")
    bash_file.write(command)
    bash_file.seek(0)
    filename = bash_file.name.split("/")[-1]
    target_path = f"{filename}.sh"

    mkdir_p(sftp, ".hctia")
    sftp.put(bash_file.name, target_path)
    sftp.close()

    _, stdout, stderr = ssh.exec_command(
        f"bash .hctia/{target_path}; rm .hctia/{target_path}"
    )

    output = "".join(stdout.readlines())
    errors = "".join(stderr.readlines())

    ssh.close()
    bash_file.close()

    return output, errors
