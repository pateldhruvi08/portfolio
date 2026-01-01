const express = require('express');
const path = require('path');
const cors = require('cors');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('.'));

// Serve HTML
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'my.html'));
});

// Resume download API
app.get('/api/resume', (req, res) => {
    const resumePath = path.join(__dirname, 'assets', 'Dhruvi_Patel_Resume.pdf');
    
    if (fs.existsSync(resumePath)) {
        res.download(resumePath, 'Dhruvi_Patel_Resume.pdf', (err) => {
            if (err) {
                console.error('Error downloading resume:', err);
                res.status(500).json({ error: 'Error downloading resume' });
            }
        });
    } else {
        res.status(404).json({ error: 'Resume file not found' });
    }
});

// Contact form API (optional - can use mailto instead)
app.post('/api/contact', (req, res) => {
    try {
        const { name, email, message } = req.body;
        
        if (!name || !email || !message) {
            return res.status(400).json({ error: 'All fields are required' });
        }
        
        // Here you can add email sending logic or just log it
        console.log('New contact form submission:');
        console.log('Name:', name);
        console.log('Email:', email);
        console.log('Message:', message);
        
        res.json({ message: 'Message received successfully!' });
    } catch (error) {
        console.error('Error processing contact form:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
    console.log(`Resume API: http://localhost:${PORT}/api/resume`);
});

