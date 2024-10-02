use pyo3::prelude::*;
use ssh2::Session;
use std::path::{Path, PathBuf};

pub trait Auth {
    /// This function should authenticate the session with the chosen authentication method
    fn authenticate(&self, username: &str, session: &mut Session) -> Result<(), ssh2::Error>;
}

#[derive(FromPyObject)]
pub enum AuthMethod {
    #[pyo3(transparent, annotation = "Password")]
    Password(Password),
    #[pyo3(transparent, annotation = "PrivateKeyFile")]
    PrivateKeyFile(PrivateKeyFile),
    #[pyo3(transparent, annotation = "PrivateKeyMemory")]
    #[cfg(unix)]
    PrivateKeyMemory(PrivateKeyMemory),
}

impl Auth for AuthMethod {
    fn authenticate(&self, username: &str, session: &mut Session) -> Result<(), ssh2::Error> {
        match self {
            AuthMethod::Password(p) => p.authenticate(username, session),
            AuthMethod::PrivateKeyFile(p) => p.authenticate(username, session),
            #[cfg(unix)]
            AuthMethod::PrivateKeyMemory(p) => p.authenticate(username, session),
        }
    }
}

#[pyclass]
#[derive(Clone)]
/// Represents password-based authentication.
pub struct Password(pub String);

#[pymethods]
impl Password {
    #[new]
    /// Creates a new [`Password`].
    ///
    /// # Arguments
    ///
    /// * `password` - The password.
    pub fn new(password: String) -> Self {
        Self(password)
    }
}

impl Auth for Password {
    fn authenticate(&self, username: &str, session: &mut Session) -> Result<(), ssh2::Error> {
        session.userauth_password(username, &self.0)
    }
}

#[pyclass]
#[derive(Clone)]
/// Represents private-key-based authentication.
pub struct PrivateKeyFile {
    /// The path to the private-key file.
    pub private_key: PathBuf,
    /// The passphrase for the private-key file.
    pub passphrase: Option<String>,
}

#[pymethods]
impl PrivateKeyFile {
    #[new]
    #[pyo3(signature = (private_key, passphrase=None))]
    /// Creates a new [`PrivateKeyFile`].
    ///
    /// # Arguments
    ///
    /// * `private_key` - The path to the private-key file.
    /// * `passphrase` - The password for the private-key file.
    pub fn new(private_key: PathBuf, passphrase: Option<String>) -> Self {
        Self {
            private_key,
            passphrase,
        }
    }
}

impl Auth for PrivateKeyFile {
    fn authenticate(&self, username: &str, session: &mut Session) -> Result<(), ssh2::Error> {
        session.userauth_pubkey_file(
            username,
            None,
            Path::new(&self.private_key),
            self.passphrase.as_deref(),
        )
    }
}

#[cfg(unix)]
#[pyclass]
#[derive(Clone)]
/// Represents private-key-based authentication.
pub struct PrivateKeyMemory {
    /// The private-key.
    pub private_key: String,
    /// The passphrase for the private-key.
    pub passphrase: Option<String>,
}

#[cfg(unix)]
#[pymethods]
impl PrivateKeyMemory {
    #[new]
    #[pyo3(signature = (private_key, passphrase=None))]
    /// Creates a new [`crate::auth::PrivateKeyMemory`].
    ///
    /// # Arguments
    ///
    /// * `private_key` - The private-key.
    /// * `passphrase` - The password for the private-key.
    pub fn new(private_key: String, passphrase: Option<String>) -> Self {
        Self {
            private_key,
            passphrase,
        }
    }
}

#[cfg(unix)]
impl Auth for PrivateKeyMemory {
    fn authenticate(&self, username: &str, session: &mut Session) -> Result<(), ssh2::Error> {
        session.userauth_pubkey_memory(
            username,
            None,
            &self.private_key,
            self.passphrase.as_deref(),
        )
    }
}
