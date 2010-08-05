#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/delay.h>
#include <stdlib.h>
#include "usart.h"

#define FOSC 8000000
#define BAUD 9600
#define MYUBRR FOSC/16/BAUD-1
//#define DDR_DEBUG 
//#define DEBUG_PIN
/*
#define DD_MOSI	3
#define DD_MISO	4
#define DD_SCK	5
#define DD_SS   2
#define DDR_SPI	DDRB
*/
//#define DDR_SPI	DDRB

volatile unsigned int pulse_count = 0;

void init_timer(void)
{
   // Prescaler = FCPU/1024
   //TCCR0|=(1<<CS02)|(1<<CS00);

   //Enable Overflow Interrupt Enable
   TCCR0A = 0x00;	//Timer counter control register

   TCCR0B = (1 << CS00) | (1 << CS02);	//WGM = 0, prescaler at 8

   TIMSK |= (1 << TOIE0);	//Set bit 1 in TIMSK to enable Timer0 overflow interrupt.


   TIMSK|=(1<<TOIE0);

   //Initialize Counter
   TCNT0=0;

}

void init_counter(void)
{
     // set Pin 7 (PD3) as the pin to be used to monitor the sensor
     PCMSK |= (1 << PIND2);

     // interrupt on INT1 pin rising edge (sensor triggered)
     MCUCR = (1 << ISC01) | (1 << ISC00);

     // turn on interrupts
     GIMSK |= (1 << INT0);
}

void main(void)
{   
    usart_init(MYUBRR);
    init_counter();
    init_timer();
    sei();

    while(1) {
     //usart_putchar('c');
    }
}

ISR(TIMER0_OVF_vect)
{
     char buffer[10];
     int i = 0;
     //cli();

     //usart_putchar('a');
     utoa(pulse_count, buffer, 10);

     while (buffer[i])
     {
	  usart_putchar(buffer[i]);
	  i++;
     }

     usart_putchar('\n');

     pulse_count = 0;
     //sei();
}

ISR(INT0_vect)
{
     //usart_putchar('b');
     pulse_count++;
}
