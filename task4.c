#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_SEQ_LENGTH 100005  

typedef struct 
{
    char data[MAX_SEQ_LENGTH];
    int top;
} Stack;

void initStack(Stack *s) 
{
    s->top = -1;
}

int isEmpty(Stack *s) 
{
    return s->top == -1;
}

void push(Stack *s, char c) 
{
    s->data[++(s->top)] = c;
}

char pop(Stack *s) 
{
    if (isEmpty(s)) return '\0';
    return s->data[(s->top)--];
}

char peek(Stack *s) 
{
    if (isEmpty(s)) return '\0';
    return s->data[s->top];
}

int isMatching(char opening, char closing) 
{
    return (opening == '(' && closing == ')') ||
           (opening == '[' && closing == ']') ||
           (opening == '{' && closing == '}') ||
           (opening == '<' && closing == '>');
}

int isOpeningParenthesis(char c) 
{
    return c == '(' || c == '[' || c == '{' || c == '<';
}


int isClosingParenthesis(char c) 
{
    return c == ')' || c == ']' || c == '}' || c == '>';
}

int countErrors(char *sequence) 
{
    Stack stack;
    int i;
    char current, top;
    
    initStack(&stack);
    int err_count = 0;
    int len = strlen(sequence);
    
    for (i = 0; i < len; i++) 
	{
        char current = sequence[i];
        
        if (!isOpeningParenthesis(current) && !isClosingParenthesis(current)) 
		{
            continue;
        }
        
        if (isOpeningParenthesis(current)) 
		{
            push(&stack, current);
        } 
		else 
		{
            if (isEmpty(&stack)) 
			{
                err_count++;
            } 
			else 
			{
                char top = pop(&stack);
                if (!isMatching(top, current)) 
				{
                    err_count++;
                }
            }
        }
    }

    err_count += stack.top + 1;
    
    return err_count;
}

int main() 
{
    int N, i, len, err_count;
    char sequence[MAX_SEQ_LENGTH];
    
    scanf("%d", &N);
    
    getchar();
    
    for (i = 0; i < N; i++) 
	{
        if (fgets(sequence, MAX_SEQ_LENGTH, stdin) != NULL) 
		{
            int len = strlen(sequence);
            if (len > 0 && sequence[len-1] == '\n') 
			{
                sequence[len-1] = '\0';
            }
            
            int err_count = countErrors(sequence);
            printf("%d\n", err_count);
        }
    }
    
    return 0;
}
