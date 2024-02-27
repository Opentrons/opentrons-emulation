import { app, BrowserWindow } from 'electron'
import path from 'path'
import { fileURLToPath } from 'url';
import { Mosquitto } from './mosquitto.ts';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

app.whenReady().then(() => {
    const win = new BrowserWindow({
        title: 'Main window',
    })

    // You can use `process.env.VITE_DEV_SERVER_URL` when the vite command is called `serve`
    if (process.env.VITE_DEV_SERVER_URL) {
        win.loadURL(process.env.VITE_DEV_SERVER_URL)
    } else {
    // Load your file
        win.loadFile('dist/index.html');
    }

    const mosquitto = new Mosquitto(__dirname);
    mosquitto.start();
   
})