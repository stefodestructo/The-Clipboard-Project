/* usart.c */
#include <avr/io.h>
#include "usart.h"

#define FOSC 8000000
#define BAUD 9600
#define MYUBRR FOSC/16/BAUD-1

void usart_init( unsigned int ubrr)
{
    /* Set baud rate */
    UBRRH = (unsigned char) (ubrr >> 8);    
    UBRRL = (unsigned char) ubrr;    

    /* Enable reciever and transmitter */
    UCSRB = (1 << RXEN) | (1 << TXEN);

    /* 8 data bits, 1 stop bit */
    UCSRC = (1 << UCSZ1) | (1 << UCSZ0);
}

void usart_putchar(uint8_t c)
{
     while ( !(UCSRA & (1<<UDRE) ) );
     UDR = c;
}

unsigned char usart_getchar(void)
{
     while ( !(UCSRA & (1<<RXC) ) );
     return UDR;
}
