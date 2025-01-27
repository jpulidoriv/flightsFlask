import requests

client_id = "FsQEPMbLF16QtPRfgQOWaZyVvFPIriWK"
client_secret = "0mYU8Sj5rO9aOSz1"

url_token = "https://test.api.amadeus.com/v1/security/oauth2/token"
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret
}

try:
    response = requests.post(url_token, headers=headers, data=data)
    response.raise_for_status()

    token_info = response.json()
    access_token = token_info['access_token']
    expires_in = token_info['expires_in']

    print(access_token)

except requests.RequestException as e:
    print("Error al obtener el nuevo token:", e)
