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

const PORT = 3001;
app.listen(PORT, () => {
    console.log(`Compiler server running on port ${PORT}`);
});