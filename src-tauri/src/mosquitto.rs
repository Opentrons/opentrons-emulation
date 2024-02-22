
pub mod mosquitto {
    use std::fmt;
    use std::process::{Command, Stdio, Child};
    use target_lexicon::Triple;

    pub struct Mosquitto {
        process: Option<Child>,
        state: MosquittoStateValues,
    }

    #[derive(Clone)]
    pub enum MosquittoStateValues {
        Running,
        StoppedWithError,
        Stopped
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


    fn get_triple_target() -> String {
        return Triple::host().to_string()
    }

    fn get_mosquitto_binary_path() -> String {
        return format!("binaries/mosquitto-{}", get_triple_target())
    }

    
    impl Mosquitto {
        pub fn new() -> Mosquitto {
            return Mosquitto {
                process: None,
                state: MosquittoStateValues::Stopped
            };
        }

        pub fn get_mosquitto_state(&mut self) -> MosquittoStateValues {
            return self.state.clone();
        }
    
        pub fn start_mosquitto(&mut self){
            match Command::new(get_mosquitto_binary_path())
            .stdout(Stdio::piped())
            .spawn() {
                Ok(child) => {
                    info!("Mosquitto started");
                    self.process = Some(child);
                    self.state = MosquittoStateValues::Running;
                },
                Err(e) => {
                    error!("Error starting mosquitto: {}", e);
                    self.process = None;
                    self.state = MosquittoStateValues::StoppedWithError;
                }
            }
            
        }
    }
}

