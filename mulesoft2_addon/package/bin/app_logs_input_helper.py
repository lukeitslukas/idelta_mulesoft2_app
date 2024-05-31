import json
import csv
from datetime import datetime, timezone
import logging
from pathlib import Path
import os
import re
import requests
import time

import import_declare_test
from solnlib import conf_manager, log
from solnlib.modular_input import checkpointer
from splunklib import modularinput as smi


ADDON_NAME = "mulesoft2_addon"

def get_bearer_token(clientid: str, clientsecret: str) -> str:
    endpoint = 'https://anypoint.mulesoft.com/accounts/api/v2/oauth2/token'

    payload = {
        'client_id': clientid,
        'client_secret': clientsecret,
        'grant_type': 'client_credentials'
    }

    print(payload)
    
    response = requests.post(endpoint, data=payload)

    access_token = ""
    
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        
    return access_token


def get_deployments(access_token: str, org_id: str, env_id: str):
    endpoint = f'https://anypoint.mulesoft.com/amc/application-manager/api/v2/organizations/{org_id}/environments/{env_id}/deployments'

    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.get(endpoint, headers=headers).json()

    out_dict = {}
    
    for app in response['items']:
        out_dict[app['name']] = app['id']
        
    return out_dict


def get_specification_id(access_token: str, org_id: str, env_id: str, deployment_id: str):
    endpoint = f'https://anypoint.mulesoft.com/amc/application-manager/api/v2/organizations/{org_id}/environments/{env_id}/deployments/{deployment_id}'

    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.get(endpoint, headers=headers).json()
    
    return response['desiredVersion']


def get_app_logs(access_token: str, org_id: str, env_id: str, deployment_id: str, last_log: float):
    spec_id = get_specification_id(access_token, org_id, env_id, deployment_id)
    # logs endpoint
    endpoint = f'https://anypoint.mulesoft.com/amc/application-manager/api/v2/organizations/{org_id}/environments/{env_id}/deployments/{deployment_id}/specs/{spec_id}/logs/file'

    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.get(endpoint, headers=headers, params={'startTime': int(last_log * 1000) + 1})
    
    if not response.text:
        return []
    
    logs = response.text.rstrip('\n').split("\n")

    for i, line in enumerate(logs):
        if re.match(r'\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z', line.strip()) and i != 0:
            logs[i] = f'\n{logs[i]}'  

    logs = '\n'.join(logs).split('\n\n')

    return(logs)


def get_timestamp(log_str: str) -> float:
    date_timestamp = re.match(r'\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z', log_str).group()
    try:
        return(datetime.strptime(date_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc).timestamp())
    except:
        return(datetime.strptime(date_timestamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp())
        

def logger_for_input(input_name: str) -> logging.Logger:
    return log.Logs().get_logger(f"{ADDON_NAME.lower()}_{input_name}")


def get_config_details(conf: str, session_key: str, config_name: str):
    cfm = conf_manager.ConfManager(
        session_key,
        ADDON_NAME,
        realm=f"__REST_CREDENTIAL__#{ADDON_NAME}#configs/conf-mulesoft2_addon_{conf}",
    )
    account_conf_file = cfm.get_conf(f"mulesoft2_addon_{conf}")
    return account_conf_file.get(config_name)



def validate_input(definition: smi.ValidationDefinition):
    return


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
    for input_name, input_item in inputs.inputs.items():
        normalized_input_name = input_name.split("://")[-1]
        logger = logger_for_input(normalized_input_name)
        try:
            # initialise splunk logging
            session_key = inputs.metadata["session_key"]
            log_level = conf_manager.get_log_level(
                logger=logger,
                session_key=session_key,
                app_name=ADDON_NAME,
                conf_name=f"{ADDON_NAME}_settings",
            )
            logger.setLevel(log_level)
            log.modular_input_start(logger, normalized_input_name)
            
            # intialise checkpointer
            checkpoint = checkpointer.KVStoreCheckpointer(
                "app_log_checkpoints",
                session_key,
                ADDON_NAME
            )
            
            # initialise mulesoft details
            account_details = get_config_details('account', session_key, input_item.get("account"))
            org_id = get_config_details('organisation', session_key, input_item.get("organisation")).get('organisationid')
            env_id = get_config_details('environment', session_key, input_item.get("environment")).get('environmentid')
            access_token = get_bearer_token(account_details.get('clientid'), account_details.get('clientsecret'))
            
            # go through deployments and ingest logs
            for deployment_name, deployment_id in get_deployments(access_token, org_id, env_id).items():
                # get checkpoint timestamp or set to 0.0 if not ingested before
                last_log = checkpoint.get(deployment_id) if checkpoint.get(deployment_id) is not None else 0.0
                
                app_logs = get_app_logs(access_token, org_id, env_id, deployment_id, last_log)
                
                if len(app_logs) > 0:
                    for app_log in app_logs:
                        event_writer.write_event(
                                smi.Event(
                                    data=app_log,
                                    index='mulesoft',
                                    sourcetype=f'app-logs',
                                    source=f'{input_name}/{deployment_name}/{deployment_id}',
                                    time=get_timestamp(app_log)
                                )
                            )
                    
                    checkpoint.update(deployment_id, get_timestamp(app_logs[-1]))
                        
                    log.events_ingested(
                        logger,
                        input_name,
                        f'app-logs',
                        len(app_logs),
                        index="mulesoft"
                    )
            log.modular_input_end(logger, normalized_input_name)
        except Exception as e:
            log.log_exception(logger, e, msg_before="Exception raised while ingesting data for demo_input: ")
