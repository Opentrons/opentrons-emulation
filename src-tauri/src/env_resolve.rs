// Functions for resolving values based on environment variables

use std::env;
use std::path::{Path, PathBuf};

pub fn get_external_binary_path() -> PathBuf {
    let is_dev = env::var("ENVIRONMENT") == Ok("DEV".to_string());
    println!("Is dev: {}", is_dev);
    let current_dir = match env::current_dir() {
        Ok(path) => path,
        Err(e) => panic!("Couldn't get current directory: {}", e),
    };
    let binary_location = if is_dev { "binaries" } else { "" };

    return Path::new(&current_dir).join(binary_location);
}
