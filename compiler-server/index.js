const express = require('express');
const axios = require('axios');
const FormData = require('form-data');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

const MAIN_BACKEND_URL = "https://codebase-6d2v.onrender.com"

const fs = require('fs');
const path = require('path');

app.post('/initiate-compilation', async (req, res) => {
    try {
        const { 
            projectId, 
            rootFolderId, 
            mainFileId, 
            testcasesCount 
        } = req.body;

        const downloadResponse = await axios({
            method: 'post',
            url: `${MAIN_BACKEND_URL}/api/v1/file/download-project-files/${projectId}`,
            responseType: 'arraybuffer'
        });

        // Save the downloaded file
        const fileName = `project-${projectId}.zip`;
        const filePath = path.join(process.cwd(), fileName);
        fs.writeFileSync(filePath, downloadResponse.data);

        res.status(200).json({ message: `Project downloaded successfully as ${fileName}` });
    } catch (error) {
        console.error('Error in initiate-compilation:', error);
        res.status(500).json({ error: 'Failed to download project', details: error.message });
    }
});

// function runPythonScript(filePath) {
//     return new Promise((resolve, reject) => {
//         const scriptPath = path.join(__dirname, 'main.py');
//         const args = [filePath]; // Add any arguments you need to pass to the Python script

//         execFile('python3', [scriptPath, ...args], (error, stdout, stderr) => {
//             if (error) {
//                 console.error('Error executing Python script:', error);
//                 reject(stderr);
//             } else {
//                 console.log('Python script output:', stdout);
//                 resolve(stdout);
//             }
//         });
//     });
// }

// async function sendOutputsToBackend(projectId, outputs) {
//     try {
//         const formData = new FormData();
//         formData.append('projectId', projectId);
//         formData.append('outputs', outputs);

//         const response = await axios.post(`${MAIN_BACKEND_URL}/api/v1/outputs/submit`, formData, {
//             headers: formData.getHeaders()
//         });

//         console.log('Outputs sent successfully:', response.data);
//     } catch (error) {
//         console.error('Error sending outputs to backend:', error);
//     }
// }


const PORT = 3001;
app.listen(PORT, () => {
    console.log(`Compiler server running on port ${PORT}`);
});