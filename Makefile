PREFIX=/usr
APPNAME=pardus-lightdm-greeter-settings
APPDIR=$(PREFIX)/share/pardus/$(APPNAME)
build: buildmo

install: installmo
	# create directory
	mkdir -p $(DESTDIR)$(APPDIR)
	mkdir -p $(DESTDIR)/$(PREFIX)/bin
	mkdir -p $(DESTDIR)/$(PREFIX)/share/icons/hicolor/scalable/apps
	mkdir -p $(DESTDIR)/$(PREFIX)/share/applications
	mkdir -p $(DESTDIR)/$(PREFIX)/share/applications
	mkdir -p $(DESTDIR)/$(PREFIX)/share/polkit-1/actions/
	# copy source code
	cp -prfv src/* $(DESTDIR)$(APPDIR)
	chmod 755 -R $(DESTDIR)$(APPDIR)
	# generate application launch command
	echo "#!/bin/sh" > $(DESTDIR)$(APPDIR)/$(APPNAME).sh
	echo "exec pkexec $(PREFIX)/share/pardus/$(APPNAME)/main.py" \
	    >> $(DESTDIR)$(APPDIR)/$(APPNAME).sh
	# make executable
	chmod 755 $(DESTDIR)$(APPDIR)/$(APPNAME).sh
	# symlink files
	ln -s ../share/pardus/$(APPNAME)/$(APPNAME).sh \
	    $(DESTDIR)/$(PREFIX)/bin/$(APPNAME) || true
	ln -s ../../../../pardus/$(APPNAME)/data/icon.svg \
	    $(DESTDIR)/$(PREFIX)/share/icons/hicolor/scalable/apps/$(APPNAME).svg || true
	ln -s ../pardus/$(APPNAME)/data/$(APPNAME).desktop \
	    $(DESTDIR)/$(PREFIX)/share/applications/$(APPNAME).desktop || true
	# install polkit policy
	install src/data/*.policy $(DESTDIR)/$(PREFIX)/share/polkit-1/actions/
	sed -i "s|@APP@|$(APPDIR)/main.py|g" $(DESTDIR)/$(PREFIX)/share/polkit-1/actions/*.policy

installmo:
	for file in `ls po/*.po`; do \
	    lang=`echo $$file | sed 's@po/@@' | sed 's/\.po//'`; \
	    mkdir -p $(DESTDIR)/usr/share/locale/$$lang/LC_MESSAGES/; \
	    install po/$$lang.mo $(DESTDIR)/usr/share/locale/$$lang/LC_MESSAGES/$(APPNAME).mo ;\
	done

buildmo:
	@echo "Building the mo files"
	for file in `ls po/*.po`; do \
		lang=`echo $$file | sed 's@po/@@' | sed 's/\.po//'`; \
		msgfmt -o po/$$lang.mo $$file; \
	done

pot:
	xgettext -o $(APPNAME).pot --from-code="utf-8" `find src -type f -iname "*.py"`
	for file in `ls po/*.po`; do \
            msgmerge $$file $(APPNAME).pot -o $$file.new ; \
	    echo POT: $$file; \
	    rm -f $$file ; \
	    mv $$file.new $$file ; \
	done
