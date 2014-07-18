antixps
=======

Antix.io print server

#Prep ubuntu

    $ sudo apt-get install git openssh-server python3-pip
    $ sudo pip3 install virtualenv

#Prep virutalenv

    $ mkdir antixps
    $ cd antixps
    $ virtualenv ENV
    $ source ENV/bin/activate

#Install Dependencies

    $ wget https://github.com/walac/pyusb/tarball/master
    $ tar -xzf master
    $ cd walac-pyusb*
    $ python setup.py install
    $ rm master
    $ rm -rf walac-pyusb*

    $ wget https://github.com/lincolnloop/python-qrcode/archive/v5.0.1.tar.gz
    $ tar -xzf v5.0.1.tar.gz
    $ cd python-qrcode-5.0.1/
    $ python setup.py install
    $ cd ..
    $ rm v5.0.1.tar.gz
    $ rm -rf python-qrcode-5.0.1

    $ pip install bottle
    $ pip install Pillow
    $ pip install pyserial
    $ pip install cherrypy
    
#Install antixps
    $ git clone https://github.com/realrunner/antixps.git
    $ cp antixps/upstart-example.conf /etc/init/antixps.conf
    $ # edit /etc/init/antixps.conf to have correct path information