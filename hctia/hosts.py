from fnmatch import fnmatch
from pathlib import PosixPath

from paramiko import SSHConfig

WILDCARD_HOST = ("*",)


def read_ssh_config(path, details=True, matching="*", excluded_hosts=WILDCARD_HOST):
    config = SSHConfig()
    config_path = PosixPath(path).expanduser().resolve()
    config.parse(open(config_path))
    if details:
        return [
            {"alias": host_alias, **config.lookup(host_alias)}
            for host_alias in config.get_hostnames()
            if host_alias not in excluded_hosts and fnmatch(host_alias, matching)
        ]
    return [
        host_alias
        for host_alias in config.get_hostnames()
        if host_alias not in excluded_hosts and fnmatch(host_alias, matching)
    ]
