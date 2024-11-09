""" An SSH library for Python; written in Rust. """
from _typeshed import GenericPath
from typing import Optional


class SessionException(Exception):
    """ Errors with the SSH session. Could be thrown by either SSH or SFTP operations. """

    ...


class SFTPException(Exception):
    """ SFTP operation errors. """

    ...


class SSHException(Exception):
    """ SSH operation errors. """

    ...


class Password:
    """ Represents password based authentication. """

    def __init__(self, password: str) -> None:
        """
        Creates a new password based authentication method.

        Args:
            password (str): The SSH password.
        """

        ...


class PrivateKeyFile:
    """ Represents private-key file based authentication. """

    def __init__(self, private_key: GenericPath, passphrase: Optional[str] = None) -> None:
        """
        Creates a new private-key based authentication method.

        Args:
            private_key (GenericPath): The path to the private-key file.
            passphrase (Optional[str], optional): The passphrase for the private-key file.
                Defaults to `None`.
        """

        ...


class PrivateKeyMemory:
    """
    Represents private-key based authentication.

    Only available on Unix
    """

    def __init__(self, private_key: str, passphrase: Optional[str] = None) -> None:
        """
        Creates a new private-key based authentication method.

        Args:
            private_key (str): The private-key.
            passphrase (Optional[str], optional): The passphrase for the private-key.
                Defaults to `None`.
        """

        ...


AuthMethod = Password | PrivateKeyFile | PrivateKeyMemory


class ExecOutput:
    """ Represents the output produced when running :func:`SSHClient.exec_command`. """

    def write_stdin(self, data: bytes) -> None:
        """
        Writes the provided data to the `stdin` stream and closes it.

        **NOTE**: Future calls will discard the provided data without doing anything.

        Args:
            data (bytes): The data to write to the stream.

        Returns:
            None
        """

        ...

    def read_stdout(self) -> bytes:
        """
        Reads the contents of the `stdout` stream and consumes it.

        **NOTE**: Future calls will return an empty string.

        Returns:
            The contents of `stdout`.
        """

        ...

    def read_stderr(self) -> bytes:
        """
        Reads the contents of the `stderr` stream and consumes it.

        **NOTE**: Future calls will return an empty string.

        Returns:
            The contents of `stderr`.
        """

        ...

    def exit_status(self) -> int:
        """
        Retrieves the exit status of the command and closes the channel and all streams.

        **NOTE**: Future calls will return 0.

        **NOTE**: Future reads of the `stdout` or `stderr` streams will return empty strings.

        Returns:
            The exit status.
        """

        ...

    def close(self) -> None:
        """
        Consumes all streams and closes the underlying channel if it exists and is active.

        If there is no active channel, then this function does nothing.

        Returns:
            None
        """

        ...


class File:
    """ A file on a remote server. """

    def read(self) -> bytes:
        """
        Reads and returns the contents of the file.

        Returns:
            The contents of the file.
        """

        ...

    def write(self, data: bytes) -> None:
        """
        Writes the specified data to the file.

        Args:
            data (bytes): The data to write to the file.

        Returns:
            None
        """

        ...


class SFTPClient:
    """ The SFTP client. """

    def chdir(self, dir: Optional[GenericPath] = None) -> None:
        """
        Changes the current working directory to the specified directory.

        If the specified directory is `None`, then the current working directory is unset.

        Once the current working directory is set, all SFTP operations will be relative to this path.

        **NOTE**: SFTP does not have a concept of a "current working directory", and so, this function
        tries to emulate it. Currently, only **absolute** paths are supported. This *MAY* change in the
        future, but is not guaranteed.

        Args:
            dir (GenericPath): The directory to change to.

        Returns:
            None
        """

        ...

    def getcwd(self) -> Optional[GenericPath]:
        """
        Returns the current working directory.

        Returns:
            The current working directory.
        """

        ...

    def mkdir(self, dir: GenericPath, mode: int = 511) -> None: ...

    def remove(self, path: GenericPath) -> None: ...

    def rmdir(self, dir: GenericPath) -> None: ...

    def open(self, filename: GenericPath, mode: str = 'r') -> File:
        """
        Opens a file on the remote server.

        Args:
            filename (GenericPath): The name of the file (if file is in `cwd`) OR the path to the file.
            mode (str, optional): Python-style file mode. Defaults to 'r'.

        Returns:
            The opened :class:`File`.
        """

        ...

    def file(self, filename: GenericPath, mode: str = 'r') -> File:
        """
        Opens a file on the remote server.

        **NOTE**: This method is just an alias to :func:`SFTPClient.open` to mimic compatibility with paramiko.

        Args:
            filename (GenericPath): The name of the file (if file is in `cwd`) OR the path to the file.
            mode (str, optional): Python-style file mode. Defaults to 'r'.

        Returns:
            The opened :class:`File`.
        """

        ...

    def get(self, remotepath: GenericPath, localpath: GenericPath) -> None:
        """
        Copies a file from the remote server to the local host.

        Args:
            remotepath (GenericPath): The remote file path.
            localpath (GenericPath): The local path to copy the file to.

        Returns:
            None
        """

        ...

    def put(self, localpath: GenericPath, remotepath: GenericPath) -> None:
        """
        Copies a local file to the remote server.

        Args:
            localpath (GenericPath): The path to the local file.
            remotepath (GenericPath): The remote path to copy the file to.

        Returns:

        """

        ...

    def is_closed(self) -> bool:
        """
        Checks if the SFTP session is closed.

        Returns:
            Whether SFTP session is closed.
        """

        ...

    def close(self) -> None:
        """
        Closes the SFTP session.

        Returns:
            None
        """

        ...


class SSHClient:
    """ The SSH client. """

    def __init__(self) -> None:
        """ Creates a new SSH client. """

        ...

    def connect(
            self,
            host: str,
            auth: AuthMethod,
            username: str = "root",
            port: int = 22,
            timeout: int = 30,
    ) -> None:
        """
        Establishes an SSH connection and sets the created session on the client.

        Args:
            host (str): The host name or address.
            auth (str): The authentication method to use.
            username (str): The SSH username. Defaults to root
            port (int, optional): The SSH port. Defaults to 22.
            timeout (int, optional): The timeout for the TCP connection (in seconds). Defaults to 30.

        Returns:
            None
        """

        ...

    def open_sftp(self) -> SFTPClient:
        """
        Opens an SFTP session using the SSH session.

        Fails if there is no active SSH session (if :func:`SSHClient.connect` was not called).

        Returns:
            The SFTP client.
        """

        ...

    def exec_command(self, command: str, detach: bool = False) -> Optional[ExecOutput]:
        """
        Executes a command using the established session and returns the output.

        Args:
            command (str): The command to run.
            detach (bool): detach the command. Will return None

        Note:
            detach will leak the channel

        Returns:
            The command's output, unless run with detach=True.
        """

        ...

    def invoke_shell(self):
        """
        Invoke a shell
        
        This function doesn't return anything (for now)
        """

        ...

    def authenticated(self) -> bool:
        """ Checks if the current session is authenticated. """

        ...

    def close(self):
        """
        Closes the underlying session.

        Returns:
            None
        """

        ...
