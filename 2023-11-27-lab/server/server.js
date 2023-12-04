const express = require('express');
const crypto = require('crypto');
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');
const app = express();

app.use(bodyParser.json());
app.use(express.static('../webpages'))

const usersFile = 'users.json';

// Check if the file exists, if not, create an empty file
if (!fs.existsSync(usersFile)) {
    fs.writeFileSync(usersFile, '[]', 'utf-8');
}
  
app.get('/manifest.json', (req, res) => {
    res.sendFile(path.join(__dirname, 'webpages', 'manifest.json'));
});
  
  // Serve the service worker
app.get('/service-worker.js', (req, res) => {
    res.sendFile(path.join(__dirname, 'webpages', 'service-worker.js'));
});  

function getHashPassword(password) {
    var hash = crypto.createHash('sha256');
    data = hash.update(password, 'utf-8');
    return data.digest('hex');
}



app.post('/signup', (req, res) => {
    try {
        let { firstName, lastName, email, password } = req.body;

        // Load users from JSON file
        let users = JSON.parse(fs.readFileSync(usersFile, 'utf-8'));
        if (!Array.isArray(users)) {
            users = [];
        }
        console.log(users)

        // Check if the email already exists
        if (users.some(user => user.email === email)) {
            res.status(400).send('User with email already exists');
        } else {
            // Add new user data to the array
            password = getHashPassword(password)
            users.push({ firstName, lastName, email, password});

            // Save the updated users to the JSON file
            fs.writeFileSync(usersFile, JSON.stringify(users, null, 2), 'utf-8');

            res.status(200).send('User logged in successfully');
        }
    } catch (error) {
        console.error('Error on signup:', error);
        res.status(500).send('Internal server error');
    }
});

app.post('/login', (req, res) => {
    try {
        const { email, password } = req.body;

        // Load users from JSON file
        let users = JSON.parse(fs.readFileSync(usersFile, 'utf-8'));

        // Check if the user exists and the password matches
        const user = users.find(user => user.email === email && user.password === getHashPassword(password));
        if (user) {
            res.status(200).send('Login successful');
        } else {
            res.status(401).send('Invalid credentials');
        }
    } catch (error) {
        console.error('Error on login:', error);
        res.status(500).send('Internal server error');
    }
});

app.listen(5000, () => {
    console.log('Server is running on port 5000');
});
