const mineflayer = require('mineflayer');
const { mineflayer: mineflayerViewer } = require('prismarine-viewer');

const TARGET_SERVER = 'blocksmc.com'; // Try this or another cracked server
const BOT_NAME = 'Spectator_' + Math.floor(Math.random() * 9999);

function createBot() {
  const bot = mineflayer.createBot({
    host: TARGET_SERVER,
    username: BOT_NAME,
    version: false 
  });

  bot.once('spawn', () => {
    bot.setControlState('jump', true);
    console.log('💀 Ghost Spawned!');
    
    // Cracked servers ke liye login command (Agar zaroorat pade)
    bot.chat('/register beastgpt123 beastgpt123');
    setTimeout(() => { bot.chat('/login beastgpt123'); }, 2000);

    try {
      mineflayerViewer(bot, { port: 3000, firstPerson: true });
      console.log('[+] 3D Vision Activated');
    } catch(e) {
      console.log('Viewer already running.');
    }

    setInterval(() => {
      const players = Object.keys(bot.players);
      if (players.length > 1) {
        let randomPlayer = players[Math.floor(Math.random() * players.length)];
        if(randomPlayer !== bot.username && bot.players[randomPlayer].entity) {
          console.log(`[Target] Stalking: ${randomPlayer}`);
          const targetEntity = bot.players[randomPlayer].entity;
          bot.lookAt(targetEntity.position.offset(0, targetEntity.height, 0));
        }
      }
    }, 15000);
  });

  bot.on('kicked', (reason) => console.log('Kicked:', reason));
  bot.on('error', err => console.log('Error:', err));
  
  // Auto-Reconnect Logic
  bot.on('end', () => {
    console.log('Bot Disconnected. Reconnecting in 10s...');
    setTimeout(createBot, 10000);
  });
}

createBot();
