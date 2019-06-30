# -*- coding: UTF-8 -*-
# created by Matheus Almeida 2018

import gspread
from flask import Flask, jsonify
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
creds = ServiceAccountCredentials.from_json_keyfile_name('service_secret.json', scope)
client = gspread.authorize(creds)

app = Flask(__name__)

# test
@app.route('/', methods=['GET'])
def hello():
    message = {
        "ok": True,
        "message": "Running! Use /sheet/<spreadsheet_id> to get the data!"
    }

    return jsonify(message), 200

# Returns all entries in a speadsheet by the speadsheet id
@app.route('/sheet/<string:spreadsheet_id>', methods=['GET'])
def get_sheet_by_id(spreadsheet_id=None):
    try:
        sheet = client.open_by_key(spreadsheet_id).sheet1
        info = sheet.get_all_records()

        message = {
            "ok": True,
            "data": info
        }

        return jsonify(message), 200
    except gspread.exceptions.APIError:
        message = {
            "ok": False,
            "message": "The sheet 'id' suplied not found! Check if you didn't missed any letter."
        }

        return jsonify(message), 404

@app.errorhandler(404)
def page_not_found(e):
    message = {
        "ok": False,
        "message": "This route doesn't exists!"
    }

    return jsonify(message), 404


if __name__ == '__main__':
    app.run(debug=True)
