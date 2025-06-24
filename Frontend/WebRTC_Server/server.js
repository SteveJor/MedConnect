// server.js
import fs from "fs";
import path from "path";
import express from "express";
import https from "https";
import { ExpressPeerServer } from "peer";
import { v4 as uuidv4 } from "uuid";
import { fileURLToPath } from "url";
import { dirname } from "path";

// Corrige __dirname en ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// App
const app = express();
app.use(express.json());

// Dossier public (optionnel : peut pointer vers un build Vite)
app.use(express.static(path.join(__dirname, "public")));

// HTTPS Server avec certificat
const httpsServer = https.createServer({
  key: fs.readFileSync(path.join(__dirname, "server.key")),
  cert: fs.readFileSync(path.join(__dirname, "server.crt")),
}, app);

// PeerJS Signaling Server
const peerServer = ExpressPeerServer(httpsServer, { debug: true });
app.use("/peer", peerServer);

// === Consultation temporaire en mémoire ===
const consultations = {};

// Créer une salle
app.post("/api/consultations", (req, res) => {
  const { peerId } = req.body;
  const id = uuidv4().split("-")[0];
  consultations[id] = { doctor: peerId };
  res.json({ id });
});

// Récupérer la salle
app.get("/api/consultations/:id", (req, res) => {
  const consult = consultations[req.params.id];
  if (!consult) return res.status(404).json({ error: "Consultation non trouvée" });
  res.json(consult);
});

// Démarrer serveur
httpsServer.listen(443, () => {
  console.log("✅ Serveur HTTPS en ligne sur le port 443");
});
