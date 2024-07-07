#include <stdio.h>
#include <stdlib.h>
#include <err.h>
#include <ctype.h>
#include <stdarg.h>
#include <string.h>

int nameChecker(char *name)
{
    if (strcmp(name, "/bin/") == 0)
        return 0;
    return 1;
}

void print_error(const char *fmt, ...)
{
    printf("Oops! Something went wrong. You entered a wrong name which is: ");
    va_list args;
    va_start(args, fmt);
    vfprintf(stderr, fmt, args);
    va_end(args);
}

void Akinator()
{
    char name[145];
    printf("Give me your name and I will guess it: ");
    fgets(name, 145, stdin);
    printf("Your name is: ");
    if (nameChecker(name))
        print_error(name);
    else
        printf(name);
    printf("Do you want me to guess your name again? (y/n) ");
    int c = getchar();
    while ((c != '\n') && (getchar() != '\n'));

    if (c == 'y')
        Akinator();
    else
    {
        printf("Goodbye! I'm Akinator, I know everything about you , exactly what's your name which is: ");
        puts(name);
    }
}

int main()
{
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    Akinator();
    return 0;
}
