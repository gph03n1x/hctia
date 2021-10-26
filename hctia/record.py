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

    _, stdout, stderr = ssh.exec_command(command)
    output = "".join(stdout.readlines())
    errors = "".join(stderr.readlines())

    ssh.close()
    return output, errors
