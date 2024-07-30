const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const util = require('util');
const fs = require('fs').promises;
const path = require('path');
const FormData = require('form-data');

const app = express();
app.use(bodyParser.json());

const MAIN_BACKEND_URL = "https://codebase-6d2v.onrender.com";
const AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2NjhmYzkyZWVkNDFkZDRjYmM2YWZhNzQiLCJpYXQiOjE3MjIzNDY2MjMsImV4cCI6MTcyMjQzMzAyM30.FNmoH2gfMsbIICwRfT15Yl878qdI0fGWHp_riFpuMho";

const execAsync = util.promisify(exec);

app.post('/initiate-compilation', async (req, res) => {
    try {
        const { 
            projectId, 
            rootFolderId, 
            mainFileId, 
            testcasesCount 
        } = req.body;

        // Download project files
        const downloadResponse = await axios({
            method: 'post',
            url: `${MAIN_BACKEND_URL}/api/v1/file/download-project-files/${projectId}`,
            responseType: 'arraybuffer'
        });

        // Save the downloaded file
        const fileName = `project-${projectId}.zip`;
        const filePath = path.join(process.cwd(), fileName);
        await fs.writeFile(filePath, downloadResponse.data);

        // Send immediate response
        res.status(200).json({ message: `Project downloaded successfully as ${fileName} and compilation initiated` });

        // Execute m4.py asynchronously
        try {
            const { stdout, stderr } = await execAsync(`python m4.py ${filePath}`);
            console.log('Python script output:', stdout);
            if (stderr) console.error('Python script error:', stderr);

            // Read output files and send them back to the main backend
            const outputFiles = await readOutputFiles();
            await sendOutputToBackend(mainFileId, outputFiles);
        } catch (error) {
            console.error('Error executing Python script:', error);
        }
    } catch (error) {
        console.error('Error in initiate-compilation:', error);
        res.status(500).json({ error: 'Failed to download project or initiate compilation', details: error.message });
    }
});

async function readOutputFiles() {
    const outputDir = path.join(process.cwd(), 'outputs');
    const files = await fs.readdir(outputDir);
    const outputFiles = [];

    for (const file of files) {
        const content = await fs.readFile(path.join(outputDir, file), 'utf8');
        outputFiles.push({
            name: file,
            content: content
        });
    }

    return outputFiles;
}

async function sendOutputToBackend(mainFileId, outputFiles) {
    const formData = new FormData();
    outputFiles.forEach((file, index) => {
        formData.append('outputFile', Buffer.from(file.content), {
            filename: file.name,
            contentType: 'text/plain',
        });
    });

    try {
        const response = await axios.post(
            `${MAIN_BACKEND_URL}/api/v1/file/add-output/${mainFileId}`,
            formData,
            {
                headers: {
                    ...formData.getHeaders(),
                    'Authorization': `Bearer ${AUTH_TOKEN}`
                }
            }
        );
        console.log('Outputs sent to backend successfully:', response.data);
    } catch (error) {
        console.error('Error sending outputs to backend:', error.message);
    }
    
}

const PORT = 3001;
app.listen(PORT, () => {
    console.log(`Compiler server running on port ${PORT}`);
});