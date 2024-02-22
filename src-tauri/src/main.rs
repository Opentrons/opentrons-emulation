// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::{Config};
use crate::mosquitto::mosquitto::Mosquitto;

extern crate pretty_env_logger;
#[macro_use] extern crate log;

use std::env;
use std::fs;

fn main() {
  // Read the contents of the .env file
  let contents = fs::read_to_string(".env").expect("Failed to read .env file");

  // Parse the contents of the .env file
  for line in contents.lines() {
    let parts: Vec<&str> = line.splitn(2, '=').collect();
    if parts.len() == 2 {
      let key = parts[0].trim();
      let value = parts[1].trim();

      // Set the environment variable
      env::set_var(key, value);
    }
  }

  // Rest of your code...
}
  println!("{:?}", windows);

}
