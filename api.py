# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from flask import request
from flask import json
from werkzeug.exceptions import HTTPException

from exception.bizexception import BizException
from market.marketdata import GetSymbolListImpl, GetSymbolPricesImpl

from env import Config
import msg
from common.logging import Logging


app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/symbollist")
@cross_origin()
def GetSymbolList():
    fmt = request.args.get('fmt')
    if Config.DEBUG:
        print('symbols fmt: {}'.format(fmt))

    return GetSymbolListImpl(fmt)


@app.route("/symbolprices")
@cross_origin()
def GetSymbolPrices():
    ticker = request.args.get('ticker')
    fmt = request.args.get('fmt')

    if Config.DEBUG:
        print('ticker: {} fmt: {}'.format(ticker, fmt))

    return GetSymbolPricesImpl(ticker, fmt)


@app.errorhandler(Exception)
def handle_exception(e):
    """
        Handle the runtime exceptions in the app.
    """
    if Config.DEBUG:
        print('exception:', e)

    #
    # Handle HTTP errors
    if isinstance(e, HTTPException):
        response = e.get_response()
        #
        # Fill the body with the exception's details
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response
    else:
        #
        # Handle non-HTTP exceptions
        emsg = msg.MSG[msg.ESERVER]
        return json.dumps(emsg), 500

#
# for test
@app.route("/")
@cross_origin()
def TestApi():
    if Config.DEBUG:
        from testpackage import TestApiImpl
        return TestApiImpl()
    else:
        return json.dumps('An API for connection test.'), 200



if __name__ == '__main__':

    app.config.from_object(Config())

    Logging.GetLogger().info(msg.MSG[msg.IAPPBEG])

    # app.run(debug=True)
    app.run()

    Logging.GetLogger().info(msg.MSG[msg.IAPPEND])


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
