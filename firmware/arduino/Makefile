CC=/usr/bin/avr-gcc
CFLAGS=-Os -Wall -mmcu=atmega328p
OBJ2HEX=/usr/bin/avr-objcopy 
AVRDUDE=/usr/bin/avrdude 
#-U lfuse:w:0xed:m
program : main.hex
	$(AVRDUDE) -c stk500v1 -b 57600 -P /dev/ttyUSB0  -p atmega328p -U  flash:w:main.hex:i
%.obj : %.o
	$(CC) $(CFLAGS) usart.c main.c -o $@

%.hex : %.obj
	$(OBJ2HEX) -R .eeprom -O ihex $< $@

clean :
	rm -f *.hex *.obj *.o

