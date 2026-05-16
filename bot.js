const mineflayer = require('mineflayer');
const { mineflayer: mineflayerViewer } = require('prismarine-viewer');

const TARGET_SERVER = 'topg.extremecraft.net'; 
const BOT_NAME = 'Ghost_' + Math.floor(Math.random() * 99999);

function createBot() {
  const bot = mineflayer.createBot({
    host: TARGET_SERVER,
    username: BOT_NAME,
    version: false 
  });

  bot.once('spawn', () => {
    console.log('💀 BeastGPT Ghost Spawned!');
    
    // Auto-Login for cracked servers
    bot.chat('/register beastgpt123 beastgpt123');
    setTimeout(() => { bot.chat('/login beastgpt123'); }, 2000);

    // Force chunk loading
    bot.setControlState('forward', true);
    bot.setControlState('jump', true);

    try {
      // 3D Viewer start kar rahe hain low render distance ke sath
      mineflayerViewer(bot, { port: 3000, firstPerson: true, viewDistance: 4 });
      console.log('[+] 3D Matrix Online');
    } catch(e) {
      console.log('Viewer running.');
    }

    // Spectator Logic
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

  bot.on('error', err => console.log('Error:', err));
  bot.on('kicked', console.log);
  
  bot.on('end', () => {
    console.log('Bot Disconnected. Resurrecting in 5s...');
    setTimeout(createBot, 5000);
  });
}

createBot();
