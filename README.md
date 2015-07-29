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

Each iOS client application requires separate APNS SSL Certificates for development and production environments. The process below is for a single certificate.

1. Obtained a signed SSL cert from the Apple Provisioning Portal. We'll refer to this cert as `DevCert.cer`.
    
    1. Go to [iOS Identifiers](https://developer.apple.com/account/ios/identifiers/bundle/bundleList.action) and create an entry for your application namespace. 
    1. Select the newly created identifier and then `Edit` from the bottom of the page. Select `Push Notifications` and then `Create Certificate`. This will provide instructions for generating and uploading a `.certSigningRequest` file created with Keychain Access on your Mac. 
    1. Upload the `.certSigningRequest` and download the signed SSL cert as `DevCert.cer`

2. Convert your Apple-issued `DevCert.cer` to `DevCert.pem`.

    ```
    $ openssl x509 -in DevCert.cer -inform der -out DevCert.pem
    ```

3. Export your Keychain Access-generated private key (from 1.ii) as `DevKey.p12`.

    Open Keychain Access, and select `Keys` from the left pane. Select your certificate's Private Key entry and then `Export` to generate the `DevKey.p12` file.
    
4. Convert `DevKey.p12` private key to `DevKey.pem`

    ```
    $ openssl pkcs12 -nocerts -in DevKey.p12 -out DevKey.pem 
    ```
    
5. Remove password on `DevKey.pem` private key, producing `DevKey.NoPassword.pem`:

    ```
    $ openssl rsa -in DevKey.pem -out DevKey.NoPassword.pem
    ```

6. Combine the no-password private key `DevKey.NoPassword.pem` with the Apple-issued and signed cert `DevCert.pem` into the cert file `Certificate.pem`:

    ```
    $ cat DevCert.pem DevKey.NoPassword.pem > Certificate.pem
    ```
	
    
### GCM API Key

1. Create a Google Cloud Messaging application using [this wizard](https://developers.google.com/mobile/add). 
2. You'll be prompted for an 'App name' and 'Android package name' (or 'iOS Bundle ID' if you're using GCM for iOS).
3. You'll finally be prompted to choose your Google Services. For our purposes you'll only need 'Cloud Messaging'.
4. The wizard will present a `Server API Key` which you copy to `local_settings.py` as `GCM_API_KEY`
    
### local_settings.py

Copy `local_settings_template.py` to `local_settings.py`. Fill in the following values:

 * `APNS_CERTIFICATE`: Path to your `Certificate.pem` file.
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
    
### Running (Heroku)

#### Setup

First install the [Heroku toolbelt](https://toolbelt.heroku.com/) and [Foreman](https://devcenter.heroku.com/articles/procfile#developing-locally-with-foreman) on your development machine.

    $ brew install heroku-toolbelt
    $ gem install foreman

To set up a new Heroku instance, invoke the following from the project root:

    $ heroku create appname

To connect to an existing Heroku instance, invoke the following from the project root:

    $ git remote add heroku git@heroku.com:appname.git
    
To modify the value of secret values (currently `GCM_API_KEY`, `APNS_CERTIFICATE`, `DJANGO_SECRET_KEY`, `DATABASE_URL`):

    $ heroku config:set NAME=VALUE

Note that we store the APNS certificate contents in `APNS_CERTIFICATE` and use the `post_compile` hook to copy its value into a certificate file.
    
To add commands that should be run before the `Procfile` is invoked, see `./bin/post_compile`. Currently we invoke `manage.py migrate`.

#### Develop

Use Foreman to locally run the application in the heroku environment.

    $ foreman start

#### Deploy

Push to the Heroku remote's master branch to deploy.

    $ git push heroku master
    
If you need to deploy a non-master local branch:

    $ git push heroku localBranch:master
    
#### Maintain

To run a command on the Heroku instance:

    $ heroku run python push/manage.py some_command

API Documentation
-------------

Check out `docs/v3/README.md` for now. The API is constantly in flux right now.

Tests
-------------
Run tests from the termainal:

    $ python push/manage.py test push

Or directly within PyCharm:

    Edit Configurations -> + Add new -> Django tests


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
