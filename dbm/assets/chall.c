#include <stdio.h>
#include <string.h>
#include <time.h>

void vuln() {
    char buffer[64];
    printf("%p\n",buffer);
    printf("Enter some text: ");
    read(0, buffer, 133);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    srand(time(NULL));
    int secret = rand();
    printf("Welcome to the guessing game!\n");
    printf("Can you guess the secret number?\n");
    printf("Enter your guess: ");
    int guess;
    scanf("%d", &guess);
    if (guess == secret) {
        vuln();
    } else {
        printf("Sorry, the secret number was %d\n", secret);
    }
    printf("Goodbye!\n");
    return 0;
}