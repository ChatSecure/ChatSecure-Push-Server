#    ChatSecure Push Server
#    Copyright (C) 2012 Chris Ballinger
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

DEBUG = True

import requests
import secrets
import json

from Crypto.Random import random
from flask import Flask, jsonify, request
from flaskext.couchdbkit import CouchDBKit
import datetime
app = Flask(__name__)
app.config['COUCHDB_DATABASE'] = 'accounts'
couchdb = CouchDBKit(app)


class Account(couchdb.Document):
    account_id = couchdb.StringProperty()
    password = couchdb.StringProperty()
    dpts = couchdb.ListProperty()
    pats = couchdb.ListProperty()
    transaction_ids = couchdb.ListProperty()
    purchase_date = couchdb.DateTimeProperty()
    expiration_date = couchdb.DateTimeProperty()


chatsecure_1_month_identifier = 'ChatSecure_Push_1Month'
chatsecure_1_year_identifier = 'ChatSecure_Push_1Year'
expired_status_code = 21006

if DEBUG == False:
    itunes_verify_url = 'https://buy.itunes.apple.com/verifyReceipt'
else:
    itunes_verify_url = 'https://sandbox.itunes.apple.com/verifyReceipt'


@app.route('/request_product_identifiers', methods=['GET'])
def request_product_identifiers():
    product_identifiers = [chatsecure_1_month_identifier, chatsecure_1_year_identifier]
    return jsonify(identifiers=product_identifiers)


@app.route('/register', methods=['POST'])
def register():
    if request.json == None:
        return jsonify(error='You must POST JSON.')
    post_data = request.json
    if post_data['receipt-data'] == None:
        return jsonify(error='Missing receipt-data.')
    post_data['password'] = secrets.iap_shared_secret
    verify = not DEBUG  # This is to prevent failure when SSL mismatch occurs on sandbox server
    r = requests.post(itunes_verify_url, json.dumps(post_data), verify=verify)
    response = r.json
    print response
    status_code = response['status']
    if status_code != 0 and not status_code == expired_status_code:
        return jsonify(error='The receipt is invalid.')
    if status_code == expired_status_code:
        print 'Status code indicates subscription has expired.'
    receipt = response['receipt']
    product_identifier = receipt['product_id']
    transaction_id = receipt['transaction_id']
    print receipt


if __name__ == '__main__':
    app.debug = DEBUG
    app.run(host='0.0.0.0')
