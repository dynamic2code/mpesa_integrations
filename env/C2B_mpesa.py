import requests
import configparser
import base64
from datetime import datetime
from requests.auth import HTTPBasicAuth
import json


config = configparser.ConfigParser()
# Replace 'path' with the actual path to your config file
config.read('/home/grrhrwh/Documents/GitHub/mpesa_integrations/env/mysetting.ini')  

# allocating global variables

mpesa_environment = config.get('mpesa_details', 'MPESA_ENVIRINMENT')
mpesa_consumer_key = config.get('mpesa_details', 'MPESA_CONSUMER_KEY') 
mpesa_consumer_secret = config.get('mpesa_details', 'MPESA_CONSUMER_SECRET')
nmm_phone_number = config.get('mpesa_details', 'NMM_PHONE_NUMBER')
mpesa_passkey = config.get('mpesa_details', 'MPESA_PASSKEY')
mpesa_express_shortcode = config.get('mpesa_details', 'MPESA_EXPRESS_SHORTCODE')

mpesa_basic_authorization = config.get('mpesa_details', 'MPESA_BASIC_AUTHORIZATION')

# the callback url should point to the function handling it
mpesa_callback_url = config.get('mpesa_details', 'MPESA_CALLBACK_URL')

def get_api_auth():
    """
    Implement the logic to obtain the access token from the Daraja API
    This function will handle the authentication process and return the access token

    Raises:
        Exception: _description_
        Exception: _description_

    Returns:
        HTTP: result access token 
    """
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

        # make a get request using python requests library
    r = requests.get(auth_url, auth=HTTPBasicAuth(mpesa_consumer_key, mpesa_consumer_secret))

    # return access_token from response
    return r.json()['access_token']

def initiate_payment(phone_number: str, amount: float):
    """
    the main function, sends the stk push

    Args:
        phone_number (_type_): _description_
        amount (_type_): _description_

    Returns:
        _type_: _description_
    """
    #live
    # url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    token  = get_api_auth()
    url = f'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {
        'Authorization': f'Bearer'+token,
        'Content-Type': 'application/json'
    }
    payload = {
        'BusinessShortCode': mpesa_express_shortcode,
        'Password': generate_password(),
        'Timestamp': get_timestamp(),
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': amount,
        'PartyA': phone_number,
        'PartyB': mpesa_express_shortcode,
        'PhoneNumber': phone_number,
        'CallBackURL': mpesa_callback_url,
        'AccountReference': 'MyApp',
        'TransactionDesc': 'Trip Payment'
    }
    response = requests.post(url, json=payload, headers=headers)
    if response:
        print(response)
    else:
        print("not")
    return response.json()

def generate_password():
    """
    Implement the logic to generate the password required by the Daraja API
    This function will generate the password based on the BusinessShortCode and other parameters 

    """
    stk_password = base64.b64encode((mpesa_express_shortcode + mpesa_consumer_key + get_timestamp()).encode()).decode()
    return stk_password

def get_timestamp():
    """
    Implement the logic to generate the timestamp required by the Daraja API
    This function will return the current timestamp in the expected format    

    Returns:
        _type_: _description_
    """

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return timestamp


def handle_callback():
    callback_data = requests.json

    # Check the result code
    result_code = callback_data['Body']['stkCallback']['ResultCode']
    if result_code != 0:
        # If the result code is not 0, there was an error
        error_message = callback_data['Body']['stkCallback']['ResultDesc']
        response_data = {'ResultCode': result_code, 'ResultDesc': error_message}
        return json(response_data)

    # If the result code is 0, the transaction was completed
    callback_metadata = callback_data['Body']['stkCallback']['CallbackMetadata']
    amount = None
    phone_number = None
    for item in callback_metadata['Item']:
        if item['Name'] == 'Amount':
            amount = item['Value']
        elif item['Name'] == 'PhoneNumber':
            phone_number = item['Value']

    # Save the variables to a file or database, etc.
    # ...

    # Return a success response to the M-Pesa server
    response_data = {'ResultCode': result_code, 'ResultDesc': 'Success'}
    print (response_data)
    return json(response_data)


