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
import os

from Crypto.Random import random
from Crypto.Hash import SHA256
from flask import Flask, jsonify, request
from dateutil.relativedelta import relativedelta
from datetime import datetime
from pymongo import Connection
from apns import APNs, Payload, PayloadAlert
app = Flask(__name__)

connection = Connection()
db = connection['pushdb']
accounts = db['accounts']

PROJECT_DIR = os.path.dirname(__file__)
KEYS_DIR = os.path.join(PROJECT_DIR, 'private_keys/')

cert_file_name = ''
key_file_name = ''
if DEBUG == True:
    cert_file_name = 'ChatSecureDevCert.pem'
    key_file_name = 'ChatSecureDevKey.pem'

apns = APNs(use_sandbox=DEBUG, cert_file=os.path.join(KEYS_DIR, cert_file_name), key_file=os.path.join(KEYS_DIR, key_file_name))

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

itunes_verify_url = ''
if DEBUG == False:
    itunes_verify_url = 'https://buy.itunes.apple.com/verifyReceipt'
else:
    itunes_verify_url = 'https://sandbox.itunes.apple.com/verifyReceipt'


# TODO: Replace these with a more secure hashing function
def hash_password(account, password):
    h = SHA256.new()
    salted_password = account['transaction_id'] + password
    h.update(salted_password)
    hashed_password = h.hexdigest()
    return hashed_password


# TODO: Replace these with a more secure hashing function
def verify_password(account, password):
    if account == None:
        return False
    hashed_password = hash_password(account, password)
    if hashed_password != account['password']:
        return False
    return True


def verify_receipt(receipt_data):
    receipt_post = {'receipt-data': receipt_data, 'password': secrets.iap_shared_secret}
    verify = not DEBUG  # This is to prevent failure when SSL mismatch occurs on sandbox server
    r = requests.post(itunes_verify_url, json.dumps(receipt_post), verify=verify)
    response = r.json
    # print response
    status_code = response['status']
    if status_code != 0 and not status_code == expired_status_code:  # TODO: Fix this in a better way for production
        return None
    if status_code == expired_status_code:
        print 'Status code indicates subscription has expired.'
        if not DEBUG:
            return None
    receipt = response['receipt']
    return receipt


def get_verified_account_from_post_data(post_data):
    if post_data == None:
        return None
    account_id = post_data.get('account_id')
    password = post_data.get('password')
    account = get_account_from_account_id(account_id)
    if not verify_password(account, password):
        return None
    return account


def get_account_from_account_id(account_id):
    account = accounts.find_one({'account_id': account_id})
    return account


def hash_original_transaction_id(original_transaction_id):
    h = SHA256.new()
    salted_original_transaction_id = secrets.transaction_id_salt + original_transaction_id
    h.update(salted_original_transaction_id)
    hashed_original_transaction_id = h.hexdigest()
    return hashed_original_transaction_id


def find_account_by_hashed_transaction_id(hashed_original_transaction_id):
    account = accounts.find_one({'transaction_id': hashed_original_transaction_id})
    return account


@app.route('/request_product_identifiers', methods=['GET'])
def request_product_identifiers():
    product_identifiers = [chatsecure_1_month_identifier, chatsecure_1_year_identifier]
    return jsonify(identifiers=product_identifiers)


@app.route('/register', methods=['POST'])
def register():
    if request.json == None:
        return jsonify(error='You must POST JSON.')
    post_data = request.json
    receipt_data = post_data.get('receipt-data')
    if receipt_data == None:
        return jsonify(error='Missing receipt-data.')
    receipt = verify_receipt(receipt_data)
    if receipt == None:
        return jsonify(error='Receipt is invalid or has expired.')
    product_identifier = receipt['product_id']
    original_transaction_id = receipt['original_transaction_id']
    original_purchase_date = receipt['original_purchase_date']

    reset_account = post_data.get('reset')
    hashed_original_transaction_id = hash_original_transaction_id(original_transaction_id)
    account = find_account_by_hashed_transaction_id(hashed_original_transaction_id)
    if account != None and not reset_account:
        return jsonify(error='Account already exists.')
    if reset_account == True:
        print 'Resetting account.'
        accounts.remove(account['_id'])
    account_id = str(random.randint(1000000, 9999999))
    account = accounts.find_one({'account_id': account_id})
    while account != None:
        account_id = str(random.randint(1000000, 9999999))
        account = accounts.find_one({'account_id': account_id})
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
    password = str(random.randint(1000000, 9999999))  # TODO: make this more secure
    hashed_password = hash_password(account, password)
    account = {}
    account['account_id'] = account_id
    account['transaction_id'] = hashed_original_transaction_id
    account['purchase_date'] = purchase_date
    account['expiration_date'] = expiration_date
    account['password'] = hashed_password
    accounts.insert(account)
    return jsonify(receipt=receipt, account_id=account_id, password=password, expiration_date=expiration_date_string)
    #print receipt


@app.route('/add_dpt', methods=['POST'])
def add_dpt():
    post_data = request.json
    account = get_verified_account_from_post_data(post_data)
    if account == None:
        jsonify(error='Invalid account ID or password.')
    dpt = post_data.get('dpt')
    dpts = account.get('dpt')
    if dpts == None:
        dpts = []
    for temp_dpt in dpts:
        if dpt == temp_dpt:
            return jsonify(error='DPT already added to account.')
    dpts.append(dpt)
    account['dpt'] = dpts
    accounts.save(account)
    return jsonify(success='Added DPT to account.')


@app.route('/request_pat', methods=['POST'])
def request_pat():
    post_data = request.json
    account = get_verified_account_from_post_data(post_data)
    if account == None:
        return jsonify(error='Invalid account ID or password.')
    pats = account.get('pat')
    if pats == None:
        pats = []
    pat = str(random.randint(1000000, 9999999))  # TODO: make this more secure
    pats.append(pat)
    account['pat'] = pats
    accounts.save(account)
    return jsonify(pat=pat)


@app.route('/change_password', methods=['POST'])
def change_password():
    post_data = request.json
    new_password = post_data.get('new_password')
    if len(new_password) < 8:
        return jsonify(error='Password length should be longer than 7.')
    account = get_verified_account_from_post_data(post_data)
    if account == None:
        jsonify(error='Invalid account ID or password.')
    hashed_password = hash_password(account, new_password)
    account['password'] = hashed_password
    accounts.save(account)
    return jsonify(success='Password changed.')


@app.route('/list_pat', methods=['POST'])
def list_pat():
    post_data = request.json
    account = get_verified_account_from_post_data(post_data)
    if account == None:
        return jsonify(error='Invalid account ID or password.')
    pats = account.get('pat')
    if pats == None or len(pats) == 0:
        return jsonify(error='No PATs are associated with this account.')
    return jsonify(pats=pats)


@app.route('/knock', methods=['POST'])
def knock():
    post_data = request.json
    account_id = post_data.get('account_id')
    account = get_account_from_account_id(account_id)
    if account == None:
        return jsonify(error='Invalid account ID or password.')
    pat = post_data.get('pat')
    anonymous = post_data.get('anonymous')
    dpts = account.get('dpt')
    pats = account.get('pat')
    if pats == None:
        pats = []
    pat_found = False
    for temp_pat in pats:  # This won't scale well with large lists of PATs
        if pat == temp_pat:
            pat_found = True
    if not pat_found:
        return jsonify(error='Invalid PAT')
    for dpt in dpts:
        # Send a notification
        print 'sending push to ' + dpt
        payload_alert = PayloadAlert("", loc_key="Someone has requested to chat with you securely.")
        if anonymous == True:
            payload = Payload(payload_alert, sound="default")
        else:
            payload = Payload(payload_alert, sound="default", custom={'pat': pat})
        apns.gateway_server.send_notification(dpt, payload)

    # Get feedback messages
    bad_tokens = False
    for (token_hex, fail_time) in apns.feedback_server.items():
        # do stuff with token_hex and fail_time
        print 'bad token: ' + token_hex
        bad_tokens = True
        dpts = filter(lambda a: a != token_hex, dpts)
    if bad_tokens == True:
        account['dpt'] = dpts
        accounts.save(account)
    return jsonify(success='Push(es) sent!')


if __name__ == '__main__':
    app.debug = DEBUG
    app.run(host='0.0.0.0')
