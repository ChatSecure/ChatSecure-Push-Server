ChatSecure Push Server
======================

An experimental design for a privacy-minded push server.

Deploy to Heroku
----------------

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

After deployment is complete, use the [Heroku Scheduler](https://scheduler.heroku.com/dashboard) to schedule daily expired token cleanup via the `python push/manage.py delete_expired_tokens` command:

![Heroku Scheduler Clean Expired Tokens Task](https://github.com/ChatSecure/ChatSecure-Push-Server/raw/master/art/heroku_scheduler_command.png)

Manual Installation
-------------------

You will need to install RabbitMQ, Postgres, and pip using the method of your choosing:

RabbitMQ is available via Homebrew.

    $ brew install rabbitmq

Postgres is available on Mac with [Postgres.app](http://postgresapp.com) but more readily upgradeable when installed via Homebrew with `brew install postgres`. On Linux, install the latest version of Postgres with the package manager of your choice.

After installing Postgres, add its `bin/` directory to your system path in prepararation for `psycopg2`, the python PostgreSQL adapter.

```bash
# ~/.bash_profile
# ...
# Postgres (Your path will differ if you aren't using Postgress.app)
PATH=${PATH}:/Applications/Postgres.app/Contents/Versions/9.4/bin/

```

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

### Database

Create a PostgrSQL database matching that you specified in your `./push/push/local_settings.py`.

    # From psql console:
    $ create database NAME;
    
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
    $ openssl pkcs12 -nocerts -in DevKey.p12 -out DevKey.pem -nodes
    ```

5. Combine the no-password private key `DevKey.pem` with the Apple-issued and signed cert `DevCert.pem` into the cert file `Certificate.pem`:

    ```
    $ cat DevCert.pem DevKey.pem > Certificate.pem
    ```

6. Configure this Django app to use your prepared certificate

    If using Heroku:

    ```
    heroku config:add APNS_CERTIFICATE="$(cat Certificate.pem)"
    ```

    Else if using your own server, make sure your certificate is accessible at `./private_keys/apns_cert.pem`.
    
### GCM API Key

1. Create a Google Cloud Messaging application using [this wizard](https://developers.google.com/mobile/add). 
2. You'll be prompted for an 'App name' and 'Android package name' (or 'iOS Bundle ID' if you're using GCM for iOS).
3. You'll finally be prompted to choose your Google Services. For our purposes you'll only need 'Cloud Messaging'.
4. The wizard will present a `Server API Key` which you copy to `local_settings.py` as `GCM_API_KEY`
    
### local_settings.py

Copy `local_settings_template.py` to `local_settings.py`. Fill in the following values:

In `PUSH_NOTIFICATION_SETTINGS` (for django-push-notifications app):

 * `APNS_CERTIFICATE` (str): Path to your `Certificate.pem` file. On Heroku this file is generated from the `APNS_CERTIFICATE` environmental variable by the `bin/post_compile` hook.
 * `APNS_HOST` (str) : Address to the APNS Host. Should be one of `settings.APNS_HOST_DEV` or `settings.APNS_HOST_PROD`, depending on which APNS certificate you are using
 * `APNS_FEEDBACK_HOST` (str) : Address to the APNS Feedback Host. Should be one of `settings.APNS_FEEDBACK_HOST_DEV` or `settings.APNS_FEEDBACK_HOST_PROD`, depending on which APNS certificate you are using
 * `APNS_ERROR_TIMEOUT` (float) : A period in seconds to await an APNS error response. Set non-zero to check and log APNS send errors. `0.5` is a typical value.
 * `GCM_API_KEY` (str) : Your Google Cloud Messaging `Server Api Key`

#### Heroku Instructions

On Heroku the default `settings.py` will generate the above settings if you specify the following environmental variables:

 * `GCM_API_KEY` : Your Google Cloud Messaging `Server Api Key`
 * `APNS_CERTIFICATE` : Your APNS certificate contents. This can be added via `heroku config:add APNS_CERTIFICATE=“$(cat Certificate.pem)”`
 * `APNS_USE_SANDBOX` : Either `'true'` or `'false'`. Will supply the appropriate values for `APNS_HOST` and `APNS_FEEDBACK_HOST`

### Database

First create a PostgrSQL database matching that you specified in your `./push/push/local_settings.py`.

    # From psql console:
    $ create database NAME;
    
Next you need to sync your database before you can do anything.

    (push)$ python manage.py migrate

Next add a superuser account for yourself. The below command will start a wizard to guide you.

    (push)$ python manage.py createsuperuser

    
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

First install the [Heroku toolbelt](https://toolbelt.heroku.com/) on your development machine.

    $ brew install heroku-toolbelt

To set up a new Heroku instance, invoke the following from the project root:

    $ heroku create appname

To connect to an existing Heroku instance, invoke the following from the project root:

    $ git remote add heroku git@heroku.com:appname.git
    
To modify the value of secret values (currently `GCM_API_KEY`, `APNS_CERTIFICATE`, `DJANGO_SECRET_KEY`, `DATABASE_URL`):

    $ heroku config:set NAME=VALUE  # This also restarts your app

Note that we store the APNS certificate contents in `APNS_CERTIFICATE` and use the `post_compile` hook to copy its value into a certificate file.
    
To add commands that should be run before the `Procfile` is invoked, see `./bin/post_compile`. Currently we invoke `manage.py migrate`.

#### Develop

Use Heroku Local to locally run the application in the heroku environment.

    $ heroku local

#### Deploy

After creating your Heroku application, add a `Heroku Postgres` addon. To add the free trial database:

    $  heroku addons:create heroku-postgresql:hobby-dev

See other [Heroku Postgres plans](https://devcenter.heroku.com/articles/heroku-postgres-plans).

Push to the Heroku remote's master branch to deploy.

    $ git push heroku master
    
If you need to deploy a non-master local branch:

    $ git push heroku localBranch:master
    
#### Maintain

To run a command on the Heroku instance:

    $ heroku run python push/manage.py some_command


##### Pruning Push Tokens

Push tokens on our Heroku instance older than `settings.CHATSECURE_PUSH['DEFAULT_TOKEN_EXPIRY_TIME_S']` are deleted based on the `tokens/delete_expired_tokens.py` management command.
You can manually invoke this on Heroku (remove `--dry-run` to actually delete expired tokens)`:

    $ heroku run python push/manage.py delete_expired_tokens --dry-run

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
