console.log("App started");

const webroot = "http://localhost";
const express = require('express');
const fs = require('fs');
const expressfileUpload = require('express-fileupload');
const { spawn } = require('child_process');

const app = express();
app.use(expressfileUpload());

function queryDataset(filename) {
    console.log(filename);
    let pythonProcess = spawn('python', ['C:\\Users\\Uni\\PycharmProjects\\ProjectRefactor\\Main.py', '--api', filename]);

    pythonProcess.stdout.on('data', function(data) {
        console.log(data.toString());
    });
}

app.get('/query', (req, res) => {
    const filename = req.query.filename;
    if (!filename) {
        return res.status(400).send("Parameter missing!");
    }
    const filePath = __dirname + '/processed/' + 'RESULTS-' + filename + '.csv';
    console.log(filePath);
    if (!fs.existsSync(filePath)) {
        return res.status(404).send("File not found!");
    }
    console.log("Found file.");
    
    res.download(filePath, (err) => {
        if (err) {
            // Handle error, if any
            console.error("Error sending file:", err);
            res.status(500).send("Error downloading file");
        } else {
            console.log("File sent successfully");
        }
    });
});

app.post('/upload', (req, res) => {
    
    if (!req.body.filename) {
        return res.status(400);
    }
    if (!req.files) {
        return res.status(400);
    }

    console.log("Begin uploading:", req.body.filename);
    const sampleFile  = req.files.csvFile;

    const fileName = req.body.filename + '.csv';
    savePath = __dirname + '/toProcess/' + fileName;

    // Check to see if the file exists before fet
    if (fs.existsSync(savePath)) {
        queryDataset(fileName)
        return res.status(200).send("Processing!");
    }

    sampleFile.mv(savePath, function(err) {
        // If server can't move the file, then return internal server error 500.
        if (err) return res.status(500).send(err);
    

        res.send('File uploaded! Begin processing');
        queryDataset(fileName);
        res.end();
        
    }); 
    
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});