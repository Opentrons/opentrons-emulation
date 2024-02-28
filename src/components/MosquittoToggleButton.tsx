import React, { useState, useEffect } from 'react';
import electron from 'electron';




export function MosquittoToggleButton(): JSX.Element {
  const [isRunning, setIsRunning] = useState(true);

  const getMosquittoState = async () => {
    const isRunning = await electron.ipcRenderer.invoke("is_mosquitto_running")
    setIsRunning(isRunning)
  }

  const handleToggle = async () => {
    await electron.ipcRenderer.invoke( isRunning ? "stop_mosquitto" : "start_mosquitto" )
    setIsRunning(!isRunning)
    
  }

  getMosquittoState()

  return (
    <div>
      <button onClick={handleToggle}>
        {isRunning ? 'Stop Mosquitto' : 'Start Mosquitto'}
      </button>
    </div>
  );
};