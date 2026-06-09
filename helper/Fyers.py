# Import the required module from the fyers_apiv3 package
from fyers_apiv3 import fyersModel
from config import config



USERNAME = config['USERNAME']
PASSWORD = config['PASSWORD']
PANCARD = config['PANCARD']
APPID = config["Fyers-ClientID"]
SECRETID = config["Fyers-Secret-Key"]

# Replace these values with your actual API credentials
def get_Fyers_Token()-> str:
    client_id = config["Fyers-ClientID"]
    secret_key = config["Fyers-Secret-Key"]
    redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
    response_type = "code"  
    grant_type = "authorization_code"

    with open("token", "r", encoding="utf-8") as file:
        auth_code = file.read().strip()

    # Create a session model with the provided credentials
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key, 
        redirect_uri=redirect_uri, 
        response_type=response_type, 
        grant_type=grant_type
    )

    # Set the authorization code in the session object
    session.set_token(auth_code)

    # Generate the access token using the authorization code
    response = session.generate_token()

    # Print the response, which should contain the access token and other details
    return response.get("refresh_token")

def generate_token():    
    session = fyersModel.SessionModel(
        client_id=APPID,       
        secret_key=SECRETID,
        redirect_uri="https://trade.fyers.in/api-login/redirect-uri/index.html",
        response_type="code",
        grant_type="authorization_code"
    )

    login_url = session.generate_authcode()
    print("login url " + login_url)
    
    auth_code = input("Enter access token: ")

    session.set_token(auth_code)
    response = session.generate_token()
    access_token = response["access_token"]

    with open("token", "w", encoding="utf-8") as file:
        file.write(access_token)
    return access_token

def get_token()-> str:
    with open("token", "r", encoding="utf-8") as file:
        auth_code = file.read().strip()

    return auth_code

def get_Stock_Depth(StockName):
    access_token = get_token()
    fyers = fyersModel.FyersModel(
        client_id=APPID,
        token= access_token,
        is_async=False
    )

    Stype ="-EQ"
    #Stype ="30JUNFUT"

    response = fyers.depth(data={"symbol": f"NSE:{StockName + Stype}", "ohlcv_flag": 1})

    if response["message"]=="Please provide valid token":
        access_token = generate_token()
        fyers = fyersModel.FyersModel(
            client_id=APPID,
            token= access_token,
            is_async=False
        )
        response = fyers.depth(data={"symbol": f"NSE:{StockName + Stype}", "ohlcv_flag": 1})

    return response["d"][f"NSE:{StockName + Stype}"]
    


