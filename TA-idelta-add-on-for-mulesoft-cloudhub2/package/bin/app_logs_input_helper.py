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


ADDON_NAME = "TA-idelta-add-on-for-mulesoft-cloudhub2"
REST_ROOT = "mulesoft_cloudhub"
MULESOFT_LOGGING_LAG_MS = 1000

def get_bearer_token(clientid: str, clientsecret: str) -> str:
    # get bearer token
    endpoint = 'https://anypoint.mulesoft.com/accounts/api/v2/oauth2/token'

    payload = {
        'client_id': clientid,
        'client_secret': clientsecret,
        'grant_type': 'client_credentials'
    }

    #print(payload)
    
    response = requests.post(endpoint, data=payload)

    access_token = ""
    
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        
    return access_token


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


def get_timestamp(log_str: str):
    date_timestamp = re.match(r'\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z', log_str)
    try:
        date_timestamp = date_timestamp.group()
    except Exception as e:
        return None
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
        realm=f"__REST_CREDENTIAL__#{ADDON_NAME}#configs/conf-{REST_ROOT}_{conf}",
    )
    account_conf_file = cfm.get_conf(f"{REST_ROOT}_{conf}")
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
                conf_name=f"{REST_ROOT}_settings",
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
            for deployment_name, deployment_id in get_deployments(logger,access_token, org_id, env_id).items():
                # get checkpoint timestamp or set to 0.0 if not ingested before
                last_log = checkpoint.get(deployment_id) if checkpoint.get(deployment_id) is not None else 0.0
                last_log = float(last_log)
                
                app_logs, new_timestamp = get_app_logs(logger, access_token, org_id, env_id, deployment_id, last_log)
                
                if len(app_logs) > 0:
                    event_writer.write_event(
                            smi.Event(
                                    data=app_logs,
                                    index=f'{input_item.get("index")}',
                                    sourcetype=f'mulesoft:log4j',
                                    source=f'{input_name}/{deployment_name}'
                                )
                            )
                    
                    checkpoint.update(deployment_id, str(new_timestamp))
                        
                    log.events_ingested(
                        logger=logger,
                        modular_input_name=f'{input_name}/{deployment_name}',
                        sourcetype=f'mulesoft:log4j',
                        n_events=1,
                        index=f'{input_item.get("index")}'
                    )
                    
            log.modular_input_end(logger, normalized_input_name)
        except Exception as e:
            log.log_exception(logger, e, exc_label="app_logs_input_exception", msg_before="Exception raised while ingesting data for app_logs_input: ")
