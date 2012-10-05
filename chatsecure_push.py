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
from Crypto.Hash import SHA256
from flask import Flask, jsonify, request
from dateutil.relativedelta import relativedelta
from datetime import datetime
from pymongo import Connection
app = Flask(__name__)

connection = Connection()
db = connection['pushdb']
accounts = db['accounts']

''' Data Structure for accounts
    {
      account: {
          "account_id": "randomly assigned account ID"
          "password": "hashed global account password",
          "dpt": ["32 bytes of hex in string format", "This is returned from the iOS device"],
          "pat": ["randomly generated push access tokens"],
          "transaction_id": "hashed original transaction id from IAP receipt",
          "purchase_date": "date of original purchase",
          "expiration_date": "date of account expiration"
      }
    }
'''

# Constants
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
    # print response
    status_code = response['status']
    if status_code != 0 and not status_code == expired_status_code:
        return jsonify(error='The receipt is invalid.')
    if status_code == expired_status_code:
        print 'Status code indicates subscription has expired.'
    receipt = response['receipt']
    product_identifier = receipt['product_id']
    original_transaction_id = receipt['original_transaction_id']
    h = SHA256.new()
    salted_original_transaction_id = secrets.transaction_id_salt + original_transaction_id
    h.update(salted_original_transaction_id)
    hashed_original_transaction_id = h.hexdigest()
    original_purchase_date = receipt['original_purchase_date']
    account = accounts.find_one({'transaction_id': hashed_original_transaction_id})
    if account != None:
        return jsonify(error='Account already exists.')
    account_id = str(random.randint(1000000, 9999999))
    account = accounts.find_one({'account_id': account_id})
    while account != None:
        account_id = str(random.randint(1000000, 9999999))
        account = accounts.find_one({'account_id': account_id})
    print 'new account id: ' + account_id
    date_substring = original_purchase_date[0:10]  # Strip off time info
    date_format = '%Y-%m-%d'
    purchase_date = datetime.strptime(date_substring, date_format)
    num_months = 0
    if product_identifier == chatsecure_1_month_identifier:
        num_months = 1
    elif product_identifier == chatsecure_1_year_identifier:
        num_months = 12
    expiration_date = purchase_date + relativedelta(months=num_months)
    expiration_date_string = datetime.strftime(expiration_date, date_format)
    h = SHA256.new()
    password = str(random.randint(1000000, 9999999))  # TODO: make this more secure
    salted_password = hashed_original_transaction_id + password
    h.update(salted_password)
    hashed_password = h.hexdigest()
    account = {}
    account['account_id'] = account_id
    account['transaction_id'] = hashed_original_transaction_id
    account['purchase_date'] = purchase_date
    account['expiration_date'] = expiration_date
    account['password'] = hashed_password
    accounts.insert(account)
    return jsonify(receipt=receipt, account_id=account_id, password=password, expiration_date=expiration_date_string)
    #print receipt


if __name__ == '__main__':
    app.debug = DEBUG
    app.run(host='0.0.0.0')
