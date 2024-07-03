import json
import logging
import requests
import time

import import_declare_test
from solnlib import conf_manager, log
from splunklib import modularinput as smi


ADDON_NAME = "mulesoft2_addon"

def get_bearer_token(clientid: str, clientsecret: str) -> str:
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
        
    return access_token
 

def get_org_id(access_token: str):
    # get org id
    org_endpoint = 'https://anypoint.mulesoft.com/cloudhub/api/organization'


    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    
    response = requests.get(org_endpoint, headers=headers)
    
    # raise errors, unauthorized or not okay
    if response.status_code == 401:
        raise Exception(f"Unauthorized, check credentials: {access_token}")
    elif access_token == "":
        raise Exception("Issue with bearer token, check credentials")
    elif response.status_code != 200:
        raise Exception(f'Status code not okay: {response.status_code}')
    
    return response.json()['csId']


def get_environment_ids(access_token: str):

    # place org ID here (this is the 'csId' value returned from get_org_id.py)
    org_id = get_org_id(access_token)

    # get environment ids
    env_endpoint = f'https://anypoint.mulesoft.com/accounts/api/organizations/{org_id}/environments'

    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.get(env_endpoint, headers=headers)

    if response.status_code == 401:
        raise Exception("Unauthorized, check credentials")
    elif access_token == "":
        raise Exception("Issue with bearer token, check credentials")
    elif response.status_code != 200:
        raise Exception(f'Status code not okay: {response.status_code}')
    
    return response.json()['data']


def logger_for_input(input_name: str) -> logging.Logger:
    return log.Logs().get_logger(f"{ADDON_NAME.lower()}_{input_name}")


def get_account_api_key(session_key: str, account_name: str):
    # get inputs fron configuration window
    cfm = conf_manager.ConfManager(
        session_key,
        ADDON_NAME,
        realm=f"__REST_CREDENTIAL__#{ADDON_NAME}#configs/conf-mulesoft2_addon_account",
    )
    account_conf_file = cfm.get_conf("mulesoft2_addon_account")
    return account_conf_file.get(account_name)


def stream_events(inputs: smi.InputDefinition, event_writer: smi.EventWriter):
    
    # inputs.inputs is a Python dictionary object like:
    # {
    #   "mulesoft_input://<input_name>": {
    #     "account": "<account_name>",
    #     "disabled": "0",
    #     "host": "$decideOnStartup",
    #     "index": "<index_name>",
    #     "interval": "<interval_value>",
    #     "python.version": "python3",
    #   },
    # }
    
    # for each log input
    for input_name, input_item in inputs.inputs.items():
        # grab input name and setup logging
        normalized_input_name = input_name.split("://")[-1]
        logger = logger_for_input(normalized_input_name)
        try:
            session_key = inputs.metadata["session_key"]
            
            # logging info
            log_level = conf_manager.get_log_level(
                logger=logger,
                session_key=session_key,
                app_name=ADDON_NAME,
                conf_name=f"{ADDON_NAME}_settings",
            )
            logger.setLevel(log_level)
            log.modular_input_start(logger, normalized_input_name)
            # getting tokens/ids
            account_details = get_account_api_key(session_key, input_item.get("account"))
            access_token = get_bearer_token(account_details.get('clientid'), account_details.get('clientsecret'))
            org_id = get_org_id(access_token)
            # write discovery
            event_writer.write_event(
                    smi.Event(
                        data=json.dumps(
                            {
                                "organisationID": org_id,
                                "account": input_item.get("account")
                            }, ensure_ascii=False, default=str),
                        index='mulesoft',
                        sourcetype='discovery-data-org',
                        time=time.time()
                    )
                )
            # log event ingestion
            log.events_ingested(
                logger,
                input_name,
                'discovery-data-org',
                1,
                index="mulesoft"
            )
            # discover environments
            env_ids = get_environment_ids(access_token)
            for environments in env_ids:
                data = {
                    "environmentID": environments['id'],
                    "environmentName": environments['name'],
                    "organisationID": org_id,
                    "account": input_item.get("account")
                }
                # ingest discovery
                event_writer.write_event(
                    smi.Event(
                        data=json.dumps(data, ensure_ascii=False, default=str),
                        index='mulesoft',
                        sourcetype='discovery-data-env',
                        time=time.time()
                    )
                )
            # log ingestion
            log.events_ingested(
                logger,
                input_name,
                'discovery-data-env',
                len(env_ids),
                index="mulesoft"
            )
            log.modular_input_end(logger, normalized_input_name)
        except Exception as e:
            log.log_exception(logger, e, msg_before="Exception raised while ingesting data for demo_input: ")
