PREFIX=/usr
APPNAME=pardus-lightdm-greeter-settings
APPDIR=$(shell realpath $(DESTDIR)$(PREFIX)/share/pardus/$(APPNAME))
build:
	: no nothing
install:
	# create directory
	mkdir -p $(APPDIR)
	mkdir -p $(DESTDIR)/$(PREFIX)/bin
	mkdir -p $(DESTDIR)/$(PREFIX)/share/icons/hicolor/scalable
	mkdir -p $(DESTDIR)/$(PREFIX)/share/applications
	mkdir -p $(DESTDIR)/$(PREFIX)/share/applications
	mkdir -p $(DESTDIR)/$(PREFIX)/share/polkit-1/actions/
	# copy source code
	cp -prfv src/* $(APPDIR)
	chmod 755 -R $(APPDIR)
	# generate application launch command
	echo "#!/bin/sh" > $(APPDIR)/$(APPNAME).sh
	echo "exec pkexec $(PREFIX)/share/pardus/$(APPNAME)/main.py" \
	    >> $(APPDIR)/$(APPNAME).sh
	# make executable
	chmod 755 $(APPDIR)/$(APPNAME).sh
	# symlink files
	ln -s ../share/pardus/$(APPNAME)/$(APPNAME).sh \
	    $(DESTDIR)/$(PREFIX)/bin/$(APPNAME) || true
	ln -s ../../../pardus/$(APPNAME)/data/icon.svg \
	    $(DESTDIR)/$(PREFIX)/share/icons/hicolor/scalable/$(APPNAME).svg || true
	ln -s ../pardus/$(APPNAME)/data/$(APPNAME).desktop \
	    $(DESTDIR)/$(PREFIX)/share/applications/$(APPNAME).desktop || true
	# install polkit policy
	install src/data/*.policy $(DESTDIR)/$(PREFIX)/share/polkit-1/actions/
	sed -i "s|@APP@|$(APPDIR)/main.py|g" $(DESTDIR)/$(PREFIX)/share/polkit-1/actions/*.policy