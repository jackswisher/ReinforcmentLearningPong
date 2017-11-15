#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct
{
    char *name;
    char *dorm;
}
student;

int cmp(const void *a, const void *b);

int main(void)
{
    student heads[] =
    {
        {"Stelios", "Branford"},
        {"Maria", "Cabot"},
        {"Anushree", "Ezra Stiles"},
        {"Brian", "Winthrop"}
    };
    printf("Before:\n");
    for (int i = 0; i < 4; i++)
    {
        printf("%s from %s\n", heads[i].name, heads[i].dorm);
    }
    qsort(heads, 4, sizeof(student), cmp);
    printf("After:\n");
    for (int i = 0; i < 4; i++)
    {
        printf("%s from %s\n", heads[i].name, heads[i].dorm);
    }
}

int cmp(const void *a, const void *b)
{
    // retrieve the two strings of names
    const char *arg1 = ((const student *)a) -> name;
    const char *arg2 = ((const student *)b) -> name;

    // now compare them! (returns a negative if a < b, 0 if equal, and a positive if a > b)
    return strcmp(arg1, arg2);
}
