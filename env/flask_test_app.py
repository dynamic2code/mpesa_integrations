from flask import Flask, render_template
from C2B_mpesa import initiate_payment, handle_callback
app = Flask(__name__)

@app.route('/')
# def sender():
#    print(initiate_payment('0113283165', 20))

@app.route('/callback')
def callback():
   handle_callback()



if __name__ == '__main__':
   app.run()