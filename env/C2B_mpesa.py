import requests
import configparser
import base64
from datetime import datetime
import json


config = configparser.ConfigParser()
# Replace 'path' with the actual path to your config file
config.read('env/settings.ini')  

# allocating global variables

mpesa_environment = config.get('section_name', 'MPESA_ENVIRINMENT')
mpesa_consumer_key = config.get('section_name', 'MPESA_CONSUMER_KEY') 
mpesa_consumer_secret = config.get('section_name', 'MPESA_CONSUMER_SECRET')
nmm_phone_number = config.get('section_name', 'NMM_PHONE_NUMBER')
mpesa_passkey = config.get('section_name', 'MPESA_PASSKEY')
mpesa_express_shortcode = config.get('section_name', 'MPESA_EXPRESS_SHORTCODE')
mpesa_callback_url = config.get('section_name', 'MPESA_CALLBACK_URL')


def initiate_payment(phone_number: str, amount: float):
    """
    the main function

    Args:
        phone_number (_type_): _description_
        amount (_type_): _description_

    Returns:
        _type_: _description_
    """
    #live
    # url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    url = f'https://{mpesa_environment}.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {
        'Authorization': f'Bearer {get_access_token(url)}',
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
    return response.json()


def get_access_token(url:str):
    """
    Implement the logic to obtain the access token from the Daraja API
    This function will handle the authentication process and return the access token

    Raises:
        Exception: _description_
        Exception: _description_

    Returns:
        HTTP: result access token 
    """
    try:
        
        encoded_credentials = base64.b64encode(f"{mpesa_consumer_key}:{mpesa_consumer_secret}".encode()).decode()

        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }

        # Send the request and parse the response
        response = requests.get(url, headers=headers).json()

        # Check for errors and return the access token
        if "access_token" in response:
            return response["access_token"]
        else:
            raise Exception("Failed to get access token: " + response["error_description"])
    except Exception as e:
        raise Exception("Failed to get access token: " + str(e)) 

def generate_password():
    """
    Implement the logic to generate the password required by the Daraja API
    This function will generate the password based on the BusinessShortCode and other parameters 

    """
    stk_password = base64.b64encode((mpesa_express_shortcode + mpesa_consumer_key + get_timestamp()).encode()).decode()

def get_timestamp():
    """
    Implement the logic to generate the timestamp required by the Daraja API
    This function will return the current timestamp in the expected format    

    Returns:
        _type_: _description_
    """

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return timestamp

