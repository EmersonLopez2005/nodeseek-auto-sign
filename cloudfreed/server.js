const express = require('express');
const app = express();
app.use(express.json());

app.post('/solve', (req, res) => {
  setTimeout(() => res.json({ token: 'fake-token' }), 500);
});

app.get('/', (_, res) => res.json({ status: 'ok' }));
app.listen(3000, () => console.log('CloudFreed listening on :3000'));
