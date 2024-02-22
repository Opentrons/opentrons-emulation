// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod mosquitto;

fn main() {
  let _ = mosquitto::mosquitto();
  app_lib::run();
}
