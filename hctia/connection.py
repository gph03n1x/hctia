import tempfile
from typing import Dict

from hctia.pages.step import construct_step
from hctia.record import retrieve_authorized_keys, upload_authorized_keys
from hctia.settings import KEYS_FILE


def add_to_remote_host(host: Dict, entry: str):
    if host["identityfile"]:
        try:
            auth_file = retrieve_authorized_keys(
                host=host["hostname"],
                port=host["port"],
                username=host["user"],
                target=KEYS_FILE,
                ssh_key=host["identityfile"][0],
            )
        except Exception as e:
            return construct_step(
                host["alias"],
                f"Couldn't retrieve the key, error: {e}",
                icon="close",
                color="red",
            )

        entries = [line.strip() for line in auth_file]
        auth_file.close()

        new_auth_file = tempfile.NamedTemporaryFile(mode="w+")

        if entry in entries:
            return construct_step(
                host["alias"],
                "Key already exists ... skipping",
                icon="exclamation",
                color="orange",
            )

        entries.append(entry)
        new_auth_file.write("\n".join(entries))

        new_auth_file.seek(0)

        try:
            upload_authorized_keys(
                host=host["hostname"],
                port=host["port"],
                username=host["user"],
                file=new_auth_file,
                target=KEYS_FILE,
                ssh_key=host["identityfile"][0],
            )
        except Exception as e:
            return construct_step(
                host["alias"],
                f"Couldn't upload the key, error: {e}",
                icon="close",
                color="red",
            )

        return construct_step(
            host["alias"], "Key added successfully", icon="check", color="green"
        )


def rm_from_remote_host(host: Dict, entry: str):
    if host["identityfile"]:
        try:
            auth_file = retrieve_authorized_keys(
                host=host["hostname"],
                port=host["port"],
                username=host["user"],
                target=KEYS_FILE,
                ssh_key=host["identityfile"][0],
            )
        except Exception as e:
            return construct_step(
                host["alias"],
                f"Couldn't retrieve the key, error: {e}",
                icon="close",
                color="red",
            )

        entries = [line.strip() for line in auth_file]
        auth_file.close()

        if entry not in entries:
            return construct_step(
                host["alias"],
                "Key doesn't exist ... skipping",
                icon="exclamation",
                color="orange",
            )

        entries.remove(entry)

        new_auth_file = tempfile.NamedTemporaryFile(mode="w+")
        new_auth_file.write("\n".join(entries))
        new_auth_file.seek(0)

        try:
            upload_authorized_keys(
                host=host["hostname"],
                port=host["port"],
                username=host["user"],
                file=new_auth_file,
                target=KEYS_FILE,
                ssh_key=host["identityfile"][0],
            )
        except Exception as e:
            return construct_step(
                host["alias"],
                f"Couldn't upload the key, error: {e}",
                icon="close",
                color="red",
            )

        return construct_step(
            host["alias"], "Key removed successfully", icon="check", color="green"
        )
