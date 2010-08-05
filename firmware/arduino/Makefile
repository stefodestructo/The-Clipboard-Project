CC=/usr/bin/avr-gcc
CFLAGS=-Os -Wall -mmcu=attiny2313
OBJ2HEX=/usr/bin/avr-objcopy 
AVRDUDE=/usr/bin/avrdude 
#-U lfuse:w:0xed:m
program : main.hex
	$(AVRDUDE) -c usbtiny -p attiny2313 -U  flash:w:main.hex:i
%.obj : %.o
	$(CC) $(CFLAGS) usart.c main.c -o $@

%.hex : %.obj
	$(OBJ2HEX) -R .eeprom -O ihex $< $@

clean :
	rm -f *.hex *.obj *.o

