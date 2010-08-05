/* usart.c */
#include <avr/io.h>
#include "usart.h"

#define FOSC 16000000
#define BAUD 9600
#define MYUBRR FOSC/16/BAUD-1

void usart_init( unsigned int ubrr)
{
    /* Set baud rate */
    UBRR0H = (unsigned char) (ubrr >> 8);    
    UBRR0L = (unsigned char) ubrr;    

    /* Enable reciever and transmitter */
    UCSR0B = (1 << RXEN0) | (1 << TXEN0);

    /* 8 data bits, 1 stop bit */
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
}

void usart_putchar(uint8_t c)
{
     while ( !(UCSR0A & (1<<UDRE0) ) );
     UDR0 = c;
}

unsigned char usart_getchar(void)
{
     while ( !(UCSR0A & (1<<RXC0) ) );
     return UDR0;
}
