import requests
from requests.auth import HTTPBasicAuth

def get_console_logs_from_url(build_url, username, api_token):
    if not build_url.endswith("/"):
        build_url += "/"

    console_url = build_url + "consoleText"

    response = requests.get(
        console_url,
        auth=HTTPBasicAuth(username, api_token)
    )

    if response.status_code == 200:
        return response.text
    else:
        return f"Error fetching logs: {response.status_code} - {response.text}"

# import requests
# from requests.auth import HTTPBasicAuth

def get_build_status(build_url, username, api_token):
    if not build_url.endswith("/"):
        build_url += "/"

    api_url = build_url + "api/json"

    response = requests.get(
        api_url,
        auth=HTTPBasicAuth(username, api_token)
    )

    if response.status_code == 200:
        data = response.json()
        return data.get("result", "UNKNOWN")
    else:
        return f"Error fetching status: {response.status_code}"