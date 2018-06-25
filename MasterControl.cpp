#include <unistd.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string>
#include <arpa/inet.h>
#include <iostream>
#include <sstream>
#define PORT0 30000
#define PORT1 30002
using namespace std;

int client();
int server();
int restore();
int next();
int freedrive();
int end_freedrive();
int pose();
// int joints(int server_sock);
int move_pose(string pose, float a, float v);

int main()
{
    string input;
    string y;
    string a;
    string v;

    // // SOCKET CONNECTION ON PORT 30000
    // int server_fd, new_socket;
    // struct sockaddr_in address;
    // int addrlen = sizeof(address);
      
    // // Creating socket file descriptor
    // if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
    // {
    //     perror("socket failed");
    //     exit(EXIT_FAILURE);
    // }
      
    // address.sin_family = AF_INET;
    // address.sin_addr.s_addr = INADDR_ANY;
    // address.sin_port = htons(PORT0);

    // bind(server_fd, (struct sockaddr *)&address, sizeof(address));

    // if (listen(server_fd, 3) < 0)
    // {
    //     perror("listen");
    //     exit(EXIT_FAILURE);
    // }
    // if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen))<0)
    // {
    //     perror("accept");
    //     exit(EXIT_FAILURE);
    // }

    // Take inputs to determine which instructions to call
    while(true) 
    {
        cout << "Enter instrunctions: ";
        cin >> input;
        if (input == "done")
        {
            break;
        }
        // if (input == "freedrive")
        // {
        //     freedrive();
        // }
        // if (input == "end_freedrive")
        // {
        //     end_freedrive();
        // }
        if (input == "next")
        {
            next();
        }
        // if (input == "pose")
        // {
        //     pose();
        // }
        // if (input == "joints")
        // {
        //     joints(new_socket);
        // }
        if (input == "restore")
        {
            restore();
        }
        if (input == "movepose")
        {
            cout << "Enter the pose: ";
            cin >> y;
            cout << "Enter the acceleration: ";
            cin >> a;
            cout << "Enter the velocity: ";
            cin >> v;
            stringstream temp1(a);
            float acceleration = 0;
            temp1 >> acceleration;
            stringstream temp2(v);
            float velocity = 0;
            temp2 >> velocity;
            move_pose(y, acceleration, velocity);
        }
    }
    return 0;
}

int client()
{
    // SOCKET CONNECTION ON PORT 30001
    int sock = 0;
    struct sockaddr_in serv_addr;
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0)
    {
        printf("\n Socket creation error \n");
        return -1;
    }
  
    memset(&serv_addr, '0', sizeof(serv_addr));
  
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT1);
      
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
    return sock;
}

int server()
{
    // SOCKET CONNECTION ON PORT 30000
    int server_fd, new_socket;
    struct sockaddr_in address;
    int addrlen = sizeof(address);
      
    // Creating socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
    {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }
      
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT0);

    bind(server_fd, (struct sockaddr *)&address, sizeof(address));

    if (listen(server_fd, 3) < 0)
    {
        perror("listen");
        exit(EXIT_FAILURE);
    }
    if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen))<0)
    {
        perror("accept");
        exit(EXIT_FAILURE);
    }

    return new_socket;
}

int restore()
{
    int client_sock;
    client_sock = client();
    
    char original[1024] = "movel([2.03577, -2.07755, 1.96136, -6.04823, 0.129896, -4.590090000000001], a = 2, v = 2)\n";
    int result;
    result = send(client_sock, original, 1024, 0);
    if (result < 0) {
        printf("\nSending Failed\n");
    }

    return 0;
}

int next()
{
    int client_sock;
    client_sock = client();
    char next[1024] = "movel([2.5, -2.0619333333333336, 1.953428888888889, -6.09665888888889, 0.27998333333333336, -4.548638888888889], a = 2.0, v = 2.0)\n";
    int result;

    result = send(client_sock, next, 1024, 0);
    if (result < 0) {
        printf("\nSending Failed\n");
    }

    return 0;
}

int freedrive()
{
    int server_sock;
    server_sock = server();
    char freedrive[256] = "freedrive\n";
    int result;

    result = send(server_sock , freedrive , 256 , 0 );
    if (result < 0) {
        printf("\nSending Failed\n");
    }
    
    return 0;
}

int end_freedrive()
{
    int server_sock;
    server_sock = server();
    char end_freedrive[256] = "end_freedrive\n";
    int result;

    result = send(server_sock , end_freedrive , 256 , 0 );
    if (result < 0) {
        printf("\nSending Failed\n");
    }

    return 0;
}

// int joints(int server_sock)
// {
//     char joints[256] = "return_joint_positions\n";
//     int result;

//     result = send(server_sock , joints , 256 , 0 );
//     if (result < 0) {
//         printf("\nSending Failed\n");
//     }
//     return 0;
// }

int pose()
{
    int server_sock;
    server_sock = server();
    char pose[256] = "return_pose\n";
    int result;

    result = send(server_sock , pose , 256 , 0 );
    if (result < 0) {
        printf("\nSending Failed\n");
    }
    return 0;
}

int move_pose(string pose, float a, float v)
{
    int client_sock;
    client_sock = client();
    string s;
    int result;

    s = "movel(p[" + pose + "], a = " + to_string(a) + ", v = " + to_string(v) + ")\n";
    printf("%s\n",s.c_str());
    int n = s.length(); 
    char command[n+1]; 
    strcpy(command, s.c_str());

    result = send(client_sock, command, n+1, 0);
    if (result < 0) {
        printf("\nSending Failed\n");
    }
    return 0;
}   
