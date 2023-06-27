from flask import Flask, render_template
from flask_restful import Api, Resource
from C2B_mpesa import initiate_payment, handle_callback
app = Flask(__name__)
# intialize a flask-restful api
api = Api(app)


api.add_resource(initiate_payment('0113283165', 20),"/stkpush")
if __name__ == '__main__':
   app.run()