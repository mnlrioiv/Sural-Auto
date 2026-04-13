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

function decrypt(data) {
    const input = Buffer.from(data, 'base64');
    if (input.length < 16) return '';
    const salt = input.subarray(8, 16);
    const [key, iv] = getKeyAndIv(salt);
    const contents = input.subarray(16);
    const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv);
    return Buffer.concat([decipher.update(contents), decipher.final()]).toString('utf-8');
}

const encrypted = process.argv[2];
const decrypted = decrypt(encrypted);
console.log('Decrypted:', decrypted);
