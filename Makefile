CC=./bobc.py
TARGET=hello
all:	$(TARGET).xml

$(TARGET): $(TARGET).bob
	$(CC) -o $@ $<
	@mv $(TARGET) $(TARGET).xml

%.xml:	%.bob
	$(CC) -o $@ $<
	
clean:
	rm *.pyc *.out *tab.py $(TARGET).xml
