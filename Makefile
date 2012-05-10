CC=./milc.py
TARGET=mean
all:	$(TARGET).xml

$(TARGET): $(TARGET).bob
	$(CC) -o $@ $<
	@mv $(TARGET) $(TARGET).xml

%.xml:	%.lla
	$(CC) -o $@ $<
	
clean:
	rm *.pyc *.out *tab.py $(TARGET)
