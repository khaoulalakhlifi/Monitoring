const express = require('express');
const sqlite3 = require('sqlite3');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 3000;

// Create SQLite database connection
const db = new sqlite3.Database('clients.db');

// Create clients table if not exists
db.run(`
  CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clientType TEXT,
    name TEXT,
    ip_address TEXT,
    longitude REAL,
    latitude REAL,
    mqtt_topic TEXT
  )
`);

app.use(bodyParser.json());

// API endpoint to handle client data submission
app.post('/addClient', (req, res) => {
  const { clientType, name, ip_address, longitude, latitude, mqtt_topic } = req.body;

  const query = `
    INSERT INTO clients (clientType, name, ip_address, longitude, latitude, mqtt_topic)
    VALUES (?, ?, ?, ?, ?, ?)
  `;

  db.run(query, [clientType, name, ip_address, longitude, latitude, mqtt_topic], (err) => {
    if (err) {
      console.error(err);
      res.status(500).json({ error: 'Internal Server Error' });
    } else {
      res.json({ success: true });
    }
  });
});

// Serve static files from the public folder (your HTML, JS, CSS files)
app.use(express.static('public'));

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
