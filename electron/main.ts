import { app, BrowserWindow, ipcMain } from 'electron'
import path from 'path'
import { fileURLToPath } from 'url';
import { Mosquitto } from './mosquitto';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function handleMosquitto(ipc: Electron.IpcMain) {
    const mosquitto = new Mosquitto(__dirname);

    ipc.handle('start_mosquitto', async () => {return await mosquitto.start();});

    ipc.handle('stop_mosquitto', async () => {return await mosquitto.stop(); });

    ipc.handle('is_mosquitto_running', async () => { return mosquitto.isRunning() })
}

app.whenReady().then(() => {
    const win = new BrowserWindow({
        title: 'Main window',
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        },
    })

    // You can use `process.env.VITE_DEV_SERVER_URL` when the vite command is called `serve`
    if (process.env.VITE_DEV_SERVER_URL) {
        win.loadURL(process.env.VITE_DEV_SERVER_URL)
    } else {
    // Load your file
        win.loadFile('dist/index.html');
    }

    handleMosquitto(ipcMain);
});
