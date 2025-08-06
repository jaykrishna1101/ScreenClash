// Online C compiler to run C program online
#include <stdio.h>
#define SIZE 5
int queue[SIZE];
int f = -1;
int r = -1;
int ticket;

void enqueue(){
    if ((f == 0 && r == SIZE-1) || f-r == 1){
        printf("Ticket Line is full\n");
    }
    else{
        if (f == -1)f=0;
        r = (r + 1) % SIZE;
        printf("Add the person in Ticket Line:");
        scanf("%d",&ticket);
        queue[r] = ticket;
        printf("Person added in Ticket line.\n");
    }
}

void dequeue(){
    if (f == -1){
        printf("Tickets Line is Empty\n");
    }
    else{
        printf("sold the ticket to :%d\n",queue[f]);
        if(f == r){
            r = -1;
            f = -1;
        }
        else
            f = (f + 1) % SIZE;
    }
}

int display(){
    if (f == -1){
        printf("Tickets Line is Empty\n");
    }
    else if(f <= r){
        for(int i=f;i<=r;i++){
            printf("Person in Ticket Line is:%d\n",queue[i]);
        }
    }
    else{
        for(int i = f; i <= SIZE - 1; i++)
        {
            printf("Person in Ticket Line is:%d\n",queue[i]);
        }
        for(int i = 0; i <= r; i++)
        {
            printf("Person in Ticket Line is:%d\n",queue[i]);
        }
    }
}
int main() {
    int ch;
    
    while(1){
        printf("\n");
        printf("WELCOME TO THE MOVIE CENTER\n");
        printf(" 1.Join the ticket Line\n 2.Withdraw the Ticket\n 3.Display the people in line\n");
        printf("Enter your choice:");
        scanf("%d",&ch);
        
        switch(ch){
            case 1:
                enqueue();
                break;
            case 2:
                dequeue();
                break;
            case 3:
                display();
                break;
        }
    }
}