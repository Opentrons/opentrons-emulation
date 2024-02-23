pub mod mosquitto {
    use crate::env_resolve::get_external_binary_path;
    use std::fmt;
    use std::process::{Child, Command, Stdio};
    use target_lexicon::Triple;

    pub struct Mosquitto {
        process: Option<Child>,
        state: MosquittoStateValues,
    }

    #[derive(Clone)]
    pub enum MosquittoStateValues {
        Running,
        StoppedWithError,
        Stopped,
    }

    impl fmt::Display for MosquittoStateValues {
        fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
            match *self {
                MosquittoStateValues::Running => write!(f, "RUNNING"),
                MosquittoStateValues::StoppedWithError => write!(f, "STOPPED_WITH_ERROR"),
                MosquittoStateValues::Stopped => write!(f, "STOPPED"),
            }
        }
    }

    pub fn get_triple_target() -> String {
        return format!("{}-{}", "mosquitto", Triple::host().to_string());
    }

    impl Mosquitto {
        pub fn new() -> Mosquitto {
            return Mosquitto {
                process: None,
                state: MosquittoStateValues::Stopped,
            };
        }

        pub fn start_mosquitto(&mut self) {
            let binary_path = get_external_binary_path().join(get_triple_target());
            match Command::new(binary_path).stdout(Stdio::piped()).spawn() {
                Ok(child) => {
                    println!("Mosquitto started");
                    self.process = Some(child);
                    self.state = MosquittoStateValues::Running;
                }
                Err(e) => {
                    println!("Error starting mosquitto: {}", e);
                    self.process = None;
                    self.state = MosquittoStateValues::StoppedWithError;
                }
            }
        }
    }
}
