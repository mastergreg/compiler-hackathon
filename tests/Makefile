CC=./bobc.py

TARGET=$(patsubst %.bob,%.xml,$(wildcard *.bob))

all:$(TARGET) 
%.xml:	%.bob $(CC)
	$(CC) -o $@ $<
	
clean:
	rm -f *.pyc *.out *tab.py $(TARGET)

.PHONY:	clean all
