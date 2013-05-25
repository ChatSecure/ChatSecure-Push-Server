ChatSecure Push Server
======================

An experimental design for a privacy-minded push server.

Installation
------------

You will need to install Postgres using the method of your choosing:

On Mac use [Postgres.app](http://postgresapp.com) for its ease or use Homebrew to install a more recent version `brew install postgres`. On Linux, install the latest version of Postgres with the package manager of your choice.

If you don't have the latest version of Python 2.7 and pip, get them.

    $ easy_install pip

Setup your virtual environment. You'll probably need to do some more stuff too.

    $ pip install virtualenv virtualenvwrapper
    $ mkvirtualenv push
    $ workon push
    
Then you will need to install the following dependencies: 

	$ cd /path/to/ChatSecure-Push-Server/
	$ pip install -r requirements.txt
	
This will install the following dependencies:

 * apns-client
 * django
 * pycrypto
 * requests
 * python-dateutil
    
Setup
---------

Download your SSL cert(s) from the Apple Provisioning Portal and convert them to the PEM format and put them in the `private_keys` directory:

    $ openssl x509 -in ChatSecureDevCert.cer -inform der -out ChatSecureDevCert.pem
    
    $ openssl pkcs12 -nocerts -out ChatSecureDevKey.pem -in ChatSecureDevKey.p12
    
    
Create `./push/push/local_settings.py` from the `local_settings_template.py` and fill in values for `IAP_SHARED_SECRET` (from iTunes Connect).    

Launch the Push Server:

	$ workon push # activate your virtual environment
	$ cd push
    $ python manage.py runserver
    
Documentation
-------------

Check out `docs/v2/README.md` for now.
    

License
---------

	ChatSecure Push Server
	Copyright (C) 2013 Chris Ballinger
	
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as
	published by the Free Software Foundation, either version 3 of the
	License, or (at your option) any later version.
	
	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Affero General Public License for more details.
	
	You should have received a copy of the GNU Affero General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.