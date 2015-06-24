ChatSecure Push Server
======================

An experimental design for a privacy-minded push server.

Installation
------------

You will need to install RabbitMQ, Postgres, and pip using the method of your choosing:

RabbitMQ is available via Homebrew.

    $ brew install rabbitmq

Postgres is available on Mac with [Postgres.app](http://postgresapp.com) but more readily upgradeable when installed via Homebrew with `brew install postgres`. On Linux, install the latest version of Postgres with the package manager of your choice.

If you don't have the latest version of Python 2.7 and pip, get them.

    $ brew install python (Mac. On Linux, use the package manager of your choice)
    $ easy_install pip

### Virtual Environment

Setup your virtual environment. You'll probably need to do some more stuff too.

    $ pip install virtualenv virtualenvwrapper
    $ mkvirtualenv push
    $ workon push
    
Then you will need to install the following dependencies: 

	(push)$ cd /path/to/ChatSecure-Push-Server/
	(push)$ pip install -r requirements.txt
	
    
Setup
---------

### APNS SSL Certificates

Download your SSL cert(s) from the Apple Provisioning Portal and convert them to the PEM format and put them somewhere:

    $ openssl x509 -in ChatSecureDevCert.cer -inform der -out ChatSecureDevCert.pem
    
    $ openssl pkcs12 -nocerts -out ChatSecureDevKey.pem -in ChatSecureDevKey.p12
    $ (set a strong passphrase here, remember this for APNS_PASSPHRASE in local_settings.py)
    
Copy the private key into the cert file because `apns-client` likes them in the same file.

	$ cat ChatSecureDevCert.pem ChatSecureDevKey.pem > Certificate.pem
	
To remove password on private key:

    $ openssl rsa -in enc_privkey.pem -out privkey.pem
    
### GCM API Key

1. Create a Google Cloud Messaging application using [this wizard](https://developers.google.com/mobile/add). 
2. You'll be prompted for an 'App name' and 'Android package name' (or 'iOS Bundle ID' if you're using GCM for iOS).
3. You'll finally be prompted to choose your Google Services. For our purposes you'll only need 'Cloud Messaging'.
4. The wizard will present a `Server API Key` which you copy to `local_settings.py` as `GCM_API_KEY`
    
### local_settings.py

Copy `local_settings_template.py` to `local_settings.py`. Fill in the following values:

 * `IAP_SHARED_SECRET`: This is if you will be validating In-App Purchases.
 * `APNS_CERT_PATH`: Path to your `Certificate.pem` file.
 * `APNS_PASSPHRASE`: Passphrase to decrypt the APNS SSL private key.
 * The `APNS_DEV_CERT_PATH`, and `APNS_DEV_PASSPHRASE` are the same as above but for the Sandbox mode.
 
 * `GCM_API_KEY` : Your Google Cloud Messaging `Server Api Key`
 
### Sync Database

You need to sync your database before you can do anything.

    (push)$ python manage.py migrate
    
### Running (Development)  

Launch the Django Push Server:

	$ workon push # activate your virtual environment
    (push)$ python manage.py runserver # Start Django Server
    
In a new terminal window:
    
    $ rabbitmq-server

In another new terminal window:
    
    $ workon push # activate your virtual environment
    (push)$ python manage.py celery worker --loglevel=info # Start Celery workers
    
### Running (Production)

TODO
    
API Documentation
-------------

Check out `docs/v2/README.md` for now. The API is constantly in flux right now.
    

License
---------

	ChatSecure Push Server
	Copyright (C) 2015 Chris Ballinger <chris@chatsecure.org>
	
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