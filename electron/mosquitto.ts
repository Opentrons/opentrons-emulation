import { ipcMain } from 'electron';
import { spawn, ChildProcess } from 'child_process';
import path from 'path';

const MOSQUITTO_EXECUTABLE = 'mosquitto';

export enum MosquittoStatus {
    STOPPED,
    STOPPED_ERROR,
    RUNNING,
}




export class Mosquitto {

    mosquittoPath: string;
    mosquittoProcess: ChildProcess | undefined = undefined;
    status: MosquittoStatus = MosquittoStatus.STOPPED;

    constructor(mosquittoDir: string) {
        this.mosquittoPath = path.join(mosquittoDir, MOSQUITTO_EXECUTABLE);;
    }

    private instanceExists() : boolean {
        return this.mosquittoProcess !== undefined;
    }

    isRunning(): boolean {
        return this.status === MosquittoStatus.RUNNING
    }

    async start() : Promise<MosquittoStatus | Error>{

        if (this.instanceExists()) {
            console.error('Mosquitto is already running.');
            return MosquittoStatus.RUNNING;
        }

        this.mosquittoProcess = spawn(this.mosquittoPath)
            ?? new Error('Failed to start subprocess.');
        this.status = MosquittoStatus.RUNNING;

        
        this.mosquittoProcess.on('error', (err) => {
            this.status = MosquittoStatus.STOPPED_ERROR;
            this.mosquittoProcess = undefined;

            console.error('Failed to start subprocess. Error: ', err);
        });

        this.mosquittoProcess.stdout?.on('data', (data) => {
            console.log(`stdout: ${data}`);
        });

        this.mosquittoProcess.stderr?.on('data', (data) => {
            console.error(`stderr: ${data}`);
        });

        this.mosquittoProcess.on('close', (code) => {
            this.status = MosquittoStatus.STOPPED;
            this.mosquittoProcess = undefined;
            
            console.log(`child process exited with code ${code}`);
        });

        return this.status;
    }

    async stop(): Promise<MosquittoStatus>{
        if (this.mosquittoProcess) {
            this.mosquittoProcess.kill("SIGTERM");
            this.mosquittoProcess = undefined;
            this.status = MosquittoStatus.STOPPED;
        } else {
            console.error('Mosquitto is not running.');
        }

        return this.status;

    }
}