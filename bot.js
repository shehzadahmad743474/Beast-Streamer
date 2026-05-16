const mineflayer = require('mineflayer');
const { mineflayer: mineflayerViewer } = require('prismarine-viewer');

// Agar ExtremeCraft me white screen rahe, to 'blocksmc.com' ya 'loyalsmp.com' try kar
const TARGET_SERVER = 'topg.extremecraft.net'; 
const BOT_NAME = 'Spectator_' + Math.floor(Math.random() * 9999);

function createBot() {
  const bot = mineflayer.createBot({
    host: TARGET_SERVER,
    username: BOT_NAME,
    version: false 
  });

  bot.once('spawn', () => {
    console.log('💀 Ghost Spawned!');
    
    // Cracked servers login
    bot.chat('/register beastgpt123 beastgpt123');
    setTimeout(() => { bot.chat('/login beastgpt123'); }, 2000);

    // BEASTGPT MOVEMENT HACK: Force Chunk Rendering!
    // Bot ko lagatar aage chalao taaki game usko aas-paas ka map dikhaye
    bot.setControlState('forward', true);
    bot.setControlState('jump', true);

    try {
      mineflayerViewer(bot, { port: 3000, firstPerson: true });
      console.log('[+] 3D Vision Activated');
    } catch(e) {
      console.log('Viewer already running.');
    }

    // Stalking Logic
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
  
  bot.on('end', () => {
    console.log('Bot Disconnected. Reconnecting in 10s...');
    setTimeout(createBot, 10000);
  });
}

createBot();
