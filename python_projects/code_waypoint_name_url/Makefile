all : zipfile

IMAGES = 0909141334.jpg 0909141445.jpg 0909141448.jpg 0909141522.jpg 0909141521.jpg 0909141628.jpg

zipfile : 20140909.zip

20140909.zip : process.html $(IMAGES)
	zip $@ $^

