const express = require('express');
const { exec } = require('child_process');

const app = express();
const port = 3000;

app.use(express.json());

app.post('/get-system-info', (req, res) => {
  const { ip_address } = req.body;

  // Exécute le script PowerShell en passant l'adresse IP en tant qu'argument
  exec(`powershell -File Get-SystemInfo.ps1 -ipAddress ${ip_address}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Erreur lors de l'exécution du script: ${error.message}`);
      return res.status(500).send('Erreur serveur');
    }

    console.log(`Résultat de la commande PowerShell: ${stdout}`);
    res.json({ result: stdout });
  });
});

app.listen(port, () => {
  console.log(`Serveur en cours d'exécution sur http://localhost:${port}`);
});
