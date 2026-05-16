const mineflayer = require('mineflayer');
const { mineflayer: mineflayerViewer } = require('prismarine-viewer');

// YAHAN KISI BHI PUBLIC CRACKED SERVER KA IP DAAL
const TARGET_SERVER = 'pika.host'; 
const BOT_NAME = 'Spectator_007_' + Math.floor(Math.random() * 1000);

const bot = mineflayer.createBot({
  host: TARGET_SERVER,
  username: BOT_NAME,
  version: false // Auto-detect version
});

bot.once('spawn', () => {
  console.log('💀 Ghost Spawned in Server!');
  
  // Start WebGL Renderer
  mineflayerViewer(bot, { port: 3000, firstPerson: true });
  console.log('[+] 3D Vision Activated on port 3000');

  // Har 30 second me kisi ko spectate karega
  setInterval(() => {
    const players = Object.keys(bot.players);
    if (players.length > 1) {
      let randomPlayer = players[Math.floor(Math.random() * players.length)];
      if(randomPlayer !== bot.username && bot.players[randomPlayer].entity) {
        console.log(`[Target Locked] Stalking: ${randomPlayer}`);
        const targetEntity = bot.players[randomPlayer].entity;
        bot.lookAt(targetEntity.position.offset(0, targetEntity.height, 0));
      }
    }
  }, 30000);
});

bot.on('error', err => console.log('Error:', err));
bot.on('end', () => console.log('Bot Disconnected.'));
