#include<stdio.h>
#include<stdlib.h>

int main (void)
{
int *x;
int *y;
x = malloc(sizeof(int));
x =42;
printf("%p\n", &x );
}
