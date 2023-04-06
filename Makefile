PREFIX=/usr
APPNAME=pardus-lightdm-greeter-settings
APPDIR=$(DESTDIR)/$(PREFIX)/share/pardus/$(APPNAME)
build:
	: no nothing
install:
	# create directory
	mkdir -p $(APPDIR)
	mkdir -p $(DESTDIR)/$(PREFIX)/bin
	mkdir -p $(DESTDIR)/$(PREFIX)/share/icons/hicolor/scalable
	mkdir -p $(DESTDIR)/$(PREFIX)/share/applications
	# copy source code
	cp -prfv src/* $(APPDIR)
	# generate application launch command
	echo "#!/bin/sh" > $(APPDIR)/$(APPNAME).sh
	echo "exec pkexec python3 /$(PREFIX)/share/pardus/$(APPNAME)/main.py" \
	    >> $(APPDIR)/$(APPNAME).sh
	# make executable
	chmod 755 $(APPDIR)/$(APPNAME).sh
	# symlink files
	ln -s ../share/pardus/$(APPNAME)/$(APPNAME).sh \
	    $(DESTDIR)/$(PREFIX)/bin/$(APPNAME)
	ln -s ../../../pardus/$(APPNAME)/data/icon.svg \
	    $(DESTDIR)/$(PREFIX)/share/icons/hicolor/scalable/$(APPNAME).svg
	ln -s ../pardus/$(APPNAME)/data/$(APPNAME).desktop \
	    $(DESTDIR)/$(PREFIX)/share/applications/$(APPNAME).desktop

