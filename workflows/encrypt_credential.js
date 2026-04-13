const crypto = require('crypto');

const ENCRYPTION_KEY = 'Z+GSvHM0FQpO7jL4s8WWZ/0ClvimPSiF';
const RANDOM_BYTES = Buffer.from('53616c7465645f5f', 'hex');

function getKeyAndIv(salt) {
    const password = Buffer.concat([Buffer.from(ENCRYPTION_KEY, 'binary'), salt]);
    const hash1 = crypto.createHash('md5').update(password).digest();
    const hash2 = crypto.createHash('md5').update(Buffer.concat([hash1, password])).digest();
    const iv = crypto.createHash('md5').update(Buffer.concat([hash2, password])).digest();
    const key = Buffer.concat([hash1, hash2]);
    return [key, iv];
}

function encrypt(data) {
    const salt = crypto.randomBytes(8);
    const [key, iv] = getKeyAndIv(salt);
    const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
    const encrypted = cipher.update(typeof data === 'string' ? data : JSON.stringify(data));
    return Buffer.concat([RANDOM_BYTES, salt, encrypted, cipher.final()]).toString('base64');
}

// SMTP credential data
const credData = {
    host: 'smtp.sural.com.ar',
    port: 587,
    secure: false,
    user: 'noreply@sural.com.ar',
    pass: 'placeholder123',
    fromEmail: 'noreply@sural.com.ar'
};

const encrypted = encrypt(JSON.stringify(credData));
console.log(encrypted);
