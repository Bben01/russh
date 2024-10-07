//! An SSH library for Python; written in Rust.

use pyo3::prelude::*;

use ssh::*;
use auth::*;

mod ssh;
mod auth;

#[pymodule]
fn russhy(py: Python<'_>, m: &Bound<PyModule>) -> PyResult<()> {
    m.add("SessionException", py.get_type_bound::<SessionException>())?;
    m.add("SFTPException", py.get_type_bound::<SFTPException>())?;
    m.add("SSHException", py.get_type_bound::<SSHException>())?;

    m.add_class::<Password>()?;
    m.add_class::<PrivateKeyFile>()?;
    m.add_class::<PrivateKeyMemory>()?;
    m.add_class::<File>()?;
    m.add_class::<SFTPClient>()?;
    m.add_class::<SSHClient>()?;

    Ok(())
}
