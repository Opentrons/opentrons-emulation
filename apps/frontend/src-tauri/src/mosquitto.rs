use tauri::command;
use std::process::{Command, Stdio};

#[command]
pub fn mosquitto() -> Result<String, String> {
    match Command::new("binaries/mosquitto-x86_64-unknown-linux-gnu")
        .stdout(Stdio::piped())
        .spawn() {
            Ok(_child) => {
                // Optionally, handle the child process's output or wait for it to finish
                // For example, let output = child.wait_with_output().expect("failed to wait on child");
                Ok("Child process spawned successfully".into())
            },
            Err(e) => Err(format!("Failed to spawn child process: {}", e)),
        }
}
