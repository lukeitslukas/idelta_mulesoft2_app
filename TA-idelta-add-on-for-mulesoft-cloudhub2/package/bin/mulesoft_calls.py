import datetime
import requests
import logging

def get_bearer_token(logger: logging.Logger, clientid: str, clientsecret: str) -> str:
    # uses user credentials to get bearer token
    endpoint = 'https://anypoint.mulesoft.com/accounts/api/v2/oauth2/token'

    payload = {
        'client_id': clientid,
        'client_secret': clientsecret,
        'grant_type': 'client_credentials'
    }
    
    response = requests.post(endpoint, data=payload)

    access_token = ""
    
    # return empty string if issue w/ bearer token
    if response.status_code == 200:
        access_token = response.json().get('access_token')
    else:
        logger.error("Get bearer token returned empty string")
        
    return access_token


def get_org_id(logger: logging.Logger, access_token: str):
    # get org id
    org_endpoint = 'https://anypoint.mulesoft.com/cloudhub/api/organization'


    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    
    response = requests.get(org_endpoint, headers=headers)
    
    # raise errors, unauthorized or not okay
    if response.status_code == 401:
        logger.error(f"Unauthorized, check credentials: {access_token}")
    elif access_token == "":
        logger.error("Issue with bearer token, check credentials")
    elif response.status_code != 200:
        logger.error(f'Status code not okay: {response.status_code}')
    
    return response.json()['csId']


def get_environment_ids(logger: logging.Logger, access_token: str):

    # place org ID here (this is the 'csId' value returned from get_org_id.py)
    org_id = get_org_id(access_token)

    # get environment ids
    env_endpoint = f'https://anypoint.mulesoft.com/accounts/api/organizations/{org_id}/environments'

    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.get(env_endpoint, headers=headers)

    if response.status_code == 401:
        logger.error(f"Unauthorized, check credentials: {access_token}")
    elif access_token == "":
        logger.error("Issue with bearer token, check credentials")
    elif response.status_code != 200:
        logger.error(f'Status code not okay: {response.status_code}')
    
    return response.json()['data']


def get_deployments(logger:logging.Logger, access_token: str, org_id: str, env_id: str):
    endpoint = f'https://anypoint.mulesoft.com/amc/application-manager/api/v2/organizations/{org_id}/environments/{env_id}/deployments'

    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.get(endpoint, headers=headers)
    logger.info("Response Code from deployments API call: "+str(response.status_code))
    logger.debug("Response from deployments API: "+response.text)
    out_dict = {}
    
    for app in response.json()['items']:
        out_dict[app['name']] = app['id']
        
    return out_dict


def get_specification_id(logger: logging.Logger, access_token: str, org_id: str, env_id: str, deployment_id: str):
    endpoint = f'https://anypoint.mulesoft.com/amc/application-manager/api/v2/organizations/{org_id}/environments/{env_id}/deployments/{deployment_id}'

    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.get(endpoint, headers=headers)
    
    logger.info("Response Code from specification ID API call: " + str(response.status_code))
    logger.debug("Response from specification ID API: " + response.text)
    
    return response.json()['desiredVersion']


def get_app_logs(logger: logging.Logger,access_token: str, org_id: str, env_id: str, deployment_id: str, last_log: float):
    spec_id = get_specification_id(logger, access_token, org_id, env_id, deployment_id)
    # logs endpoint
    endpoint = f'https://anypoint.mulesoft.com/amc/application-manager/api/v2/organizations/{org_id}/environments/{env_id}/deployments/{deployment_id}/specs/{spec_id}/logs/file'

    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    
    end_time = (datetime.now().timestamp()) - (MULESOFT_LOGGING_LAG_MS / 1000)
    response = requests.get(endpoint, headers=headers, params={'startTime': int(last_log * 1000.0),
                                                               'endTime': int(end_time * 1000.0)})
    logger.info("Response Code from App Logs API call: " + str(response.status_code))
    logger.debug(f"Requesting logs from {endpoint} from {int(last_log * 1000)} until {int(end_time * 1000)}")
    
    if not response.text:
        logger.info("Response from App Logs is empty, no new logs")
        return "", end_time
    
    return response.text, end_time