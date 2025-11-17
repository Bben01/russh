import os
import time
from pathlib import Path

import pytest

from russhy import SSHClient, Password

HOST = os.environ.get("SSH_HOST", "localhost")
PORT = int(os.environ.get("SSH_PORT", "22"))
USER = os.environ.get("SSH_USER", "russhy")
PASS = os.environ.get("SSH_PASS", "russhy")


@pytest.fixture
def client() -> SSHClient:
    ssh = SSHClient()
    ssh.connect(HOST, Password(PASS), username=USER, port=PORT)
    assert ssh.authenticated()
    yield ssh
    ssh.close()


def test_detach(client: SSHClient):
    # in detached mode, the command should not block and we should be able to run
    # another command right after
    client.exec_command("sleep 3 && touch /tmp/test_detach", detach=True)
    res = client.exec_command("echo ok")
    assert res.read_stdout().decode() == "ok\n"


def test_stress_detach(client: SSHClient):
    # in detached mode, the command should not block and we should be able to run
    # up to 1024 commands according to the ssh protocol.
    # We test with 32 to be safe
    for i in range(32):
        client.exec_command(f"touch /tmp/test_stress_detach_{i}", detach=True)
    res = client.exec_command("echo ok")
    assert res.read_stdout().decode() == "ok\n"


def test_tunnel(client: SSHClient):
    # we open a tunnel to the local ssh server and check that we can communicate
    # with it
    tunnel = client.open_tunnel("localhost", 22)
    time.sleep(1)
    res = tunnel.read()
    assert b"SSH" in res
    tunnel.close()
