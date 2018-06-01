// Client side C/C++ program to demonstrate Socket programming
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include <arpa/inet.h>
#define PORT 30001
  
int main(int argc, char const *argv[])
{
    //struct sockaddr_in address;
    char buffer[1024] = {0};
    int sock = 0, result;
    struct sockaddr_in serv_addr;
    char command[1024] = "movej([-1.80, -1.58, 1.16, -1.15, -1.55, 1.18], a=1.0, v=0.1)\n";
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0)
    {
        printf("\n Socket creation error \n");
        return -1;
    }
  
    memset(&serv_addr, '0', sizeof(serv_addr));
  
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
      
    // Convert IPv4 and IPv6 addresses from text to binary form
    if(inet_pton(AF_INET, "140.233.20.115", &serv_addr.sin_addr)<=0) 
    {
        printf("\nInvalid address/ Address not supported \n");
        return -1;
    }
  
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        printf("\nConnection Failed \n");
        return -1;
    }

    result = send(sock, command, 1024, 0);
    if (result < 0) {
        printf("\nSending Failed\n");
    }

    recv(sock, buffer, 1024, 0);
    for (int i = 0; i < 80; i += 8) {
        printf("%02d: ", i);
        for (int j = 0; j< 8; j++) {
            printf("%02x ", (unsigned char)buffer[i+j]);
        }   
        for (int j = 0; j< 8; j++) {
            printf("%c ", (unsigned char)buffer[i+j]);
        }   
        printf("\n");
    }
    return 0;
}