import { spawn, ChildProcess } from 'child_process';
import path from 'path';

const MOSQUITTO_EXECUTABLE = 'mosquitto';

export enum MosquittoStatus {
    STOPPED,
    STOPPED_ERROR,
    RUNNING,
}

export class Mosquitto {
    mosquittoDir: string;
    mosquittoProcess: ChildProcess | undefined = undefined;
    status: MosquittoStatus = MosquittoStatus.STOPPED;

    constructor(mosquittoDir: string) {
        this.mosquittoDir = mosquittoDir;
    }

    start() {
        const mosquittoPath = path.join(this.mosquittoDir, MOSQUITTO_EXECUTABLE);
        this.mosquittoProcess = spawn(
            mosquittoPath,
            {stdio: "pipe"}
        ) ?? new Error('Failed to start subprocess.');

        
        this.mosquittoProcess.on('error', (err) => {
            console.error('Failed to start subprocess. Error: ', err);
        });

        this.mosquittoProcess.stdout?.on('data', (data) => {
            console.log(`stdout: ${data}`);
        });

        this.mosquittoProcess.stderr?.on('data', (data) => {
            console.error(`stderr: ${data}`);
        });

        this.mosquittoProcess.on('close', (code) => {
            console.log(`child process exited with code ${code}`);
        });
    }
}