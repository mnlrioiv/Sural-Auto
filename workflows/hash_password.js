const bcrypt = require('/usr/local/lib/node_modules/n8n/node_modules/.pnpm/bcryptjs@2.4.3/node_modules/bcryptjs/dist/bcryptjs.js');

const password = 'Sural2026!';
const hash = bcrypt.hashSync(password, 10);
console.log(hash);
