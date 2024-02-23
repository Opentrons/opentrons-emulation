// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use dotenv;

mod env_resolve;

mod mosquitto;
use mosquitto::mosquitto::{Mosquitto};

fn main() {
    dotenv::dotenv().ok();
    tauri::Builder::default()
        .setup(|_app| {
            let mut mosquitto = Mosquitto::new();
            mosquitto.start_mosquitto();
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
