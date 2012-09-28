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

from flask import Flask, jsonify
app = Flask(__name__)


product_identifiers = ['ChatSecure_Push_1Month', 'ChatSecure_Push_1Year']

@app.route('/request_product_identifiers', methods=['GET'])
def request_product_identifiers():
    return jsonify(identifiers=product_identifiers)

if __name__ == '__main__':
    app.debug = DEBUG
    app.run()