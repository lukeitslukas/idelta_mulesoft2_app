import json
import csv
from datetime import datetime, timezone
import logging
from pathlib import Path
import os
import re
import requests
import time
import json

import import_declare_test

from solnlib import conf_manager, log
from solnlib.modular_input import checkpointer
from splunklib import modularinput as smi


ADDON_NAME = "mulesoft2_addon"

def get_bearer_token(clientid: str, clientsecret: str) -> str:
    # get bearer token
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
    
    logs = ""
        
    for line in response.text.strip().split("\n"):
        # normal timestamp format
        timestamp = re.match(r'\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z', line.strip())
        # broken logs timestamp format
        timestamp1 = re.match(r'^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.?\d{0,3}\]', line.strip())
        if not line.strip():
            continue
        elif line.startswith("  "):
            # broken multiline logs start like this
            logs = logs + "\n" + line.strip()
        elif timestamp:
            logs = logs + "\n\n" + line.strip()
        elif timestamp1:
            logs = logs + "\n\n" + line.strip().replace('[', '', 2).replace(' ', 'T', 1).replace(']', '', 2).replace(' ', 'Z ', 1).replace("[event: ]:", '-', 1)
        else:
            logs = logs + "\n\n" + line.strip()
            
    logs = logs.lstrip().split('\n\n')
    
    for i, log in enumerate(logs):
        log = log.split(" ")
        if log[2] == '':
            log[2] = '[]'
        log = " ".join(log)
        logs[i] = log

    return(logs)


def get_timestamp(log_str: str):
    date_timestamp = re.match(r'\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z', log_str)
    try:
        date_timestamp = date_timestamp.group()
    except Exception as e:
        return log_str
    try:
        return (datetime.strptime(date_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc).timestamp())
    except:
        return (datetime.strptime(date_timestamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp())
        

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
                "mulesoft_checkpoints",
                session_key,
                ADDON_NAME
            )
            
            # initialise mulesoft details
            account_details = get_config_details('account', session_key, input_item.get("account"))
            org_id = get_config_details('organisation', session_key, input_item.get("organisation")).get('organisationid')
            env_id = get_config_details('environment', session_key, input_item.get("environment")).get('environmentid')
            env_name = get_config_details('environment', session_key, input_item.get("environment")).get('name')
            org_name = get_config_details('organisation', session_key, input_item.get("organisation")).get('name')
            access_token = get_bearer_token(account_details.get('clientid'), account_details.get('clientsecret'))
            
            # go through deployments and ingest logs
            for deployment_name, deployment_id in get_deployments(access_token, org_id, env_id).items():
                # get checkpoint timestamp or set to 0.0 if not ingested before
                last_log = checkpoint.get(deployment_id) if checkpoint.get(deployment_id) is not None else 0.0
                last_log = float(last_log)
                
                app_logs = get_app_logs(access_token, org_id, env_id, deployment_id, last_log)
                
                if len(app_logs) > 0:
                    for app_log in app_logs:
                        '''data = {
                            "_raw": app_log,
                            "environmentID": env_id,
                            "envName": env_name,
                            "orgID": org_id,
                            "orgName": org_name
                        }'''
                        
                        event_writer.write_event(
                            smi.Event(
                                    data=app_log,
                                    index=f'{input_item.get("index")}',
                                    sourcetype=f'mulesoft:log4j',
                                    source=f'{ADDON_NAME}://{normalized_input_name}',
                                    time=get_timestamp(app_log)
                                )
                            )
                    
                    checkpoint.update(deployment_id, str(get_timestamp(app_logs[-1])))
                        
                    log.events_ingested(
                        logger,
                        input_name,
                        f'mulesoft:log4j',
                        len(app_logs),
                        index=f'{input_item.get("index")}'
                    )
            log.modular_input_end(logger, normalized_input_name)
        except Exception as e:
            log.log_exception(logger, e, exc_label="app_logs_input_exception", msg_before="Exception raised while ingesting data for app_logs_input: ")
