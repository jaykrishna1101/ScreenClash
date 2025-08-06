#include <stdio.h>

int top = -1, stack[5];
int isempty();
int isfull();
void addto_stack();
void remove_stack();
void display();

int main(){
    int ch;
    
    while(1)
    {
        printf("Enter choice: \n1. ADD TO STACK \n2. REMOVE FROM STACK \n3. DISPLAY\n4. EXIT\n");
        scanf("%d",&ch);
        switch (ch)
        {
        case 1:
            if(isfull())
                printf("stack overflow\n");
            else
                addto_stack();
            break;
        case 2:
            if(isempty())
                printf("stack is empty\n");
            else
                remove_stack();
            break;
        case 3:
            if(isempty())
                printf("stack is empty\n");
            else
                display();
            break;
        default:
            break;
        }
        if(ch == 4)
            break;
    }
    return 0;
}

int isempty(){
    if(top == -1)
        return 1;
    else 
        return 0;
}

int isfull(){
    if(top == 4)
        return 1;
    else
        return 0;
}

void addto_stack(){
    printf("enter element to add: ");
    top++;
    scanf("%d",&stack[top]);
    return;
}

void remove_stack(){
    top--;
    return;
}

void display(){
    for(int i  = 0; i <= top; i++){
        printf("%d\t",stack[i]);
    }
    printf("\n");
    return;
}

