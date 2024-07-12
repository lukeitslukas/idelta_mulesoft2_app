# TA iDelta Add-On For Mulesoft Cloudhub2

## Installation Intructions
### Installing the app from Splunkbase
[TODO]

### Setting up the app
Create the index/indexes you wish to store the mulesoft data in, then go to:

Settings -> Advanced Search -> Search Macros

and modify "mulesoft2addon_discovery_index" to the index where you will store your discovery data.

### Setting Up Mulesoft Credentials
To pull data from Mulesoft, we can create an app with the required permissions to pull Mulesoft logs. A user account can be used instead (unless Multi-Factor Authentication is enabled), but it is best practise to create a specific application with the specific permissions.

Once logged into the Mulesoft platform, we can create an app by going to the following page:

Navigation Menu -> Admin -> Access Management -> Connected Apps

Ensure you are on the correct business group and click "Create App" within Owned Apps.

Give the application an approapriate name, in our usecase we used "iDelta-Splunk"

Select "App acts on its own behalf (client credentials)"

Click "Add Scopes"

Add the following permissions for the organisations and environments you wish to monitor:
 - API Manager
    - View Client Applications
 - General
    - View Environment
    - View Organization
 - Runtime Manager
    - Read Applications
    - Read Servers

Click save then note down the values from Copy ID (Client ID) and Copy Secret (Secret ID), this will be the values we put into the Mulesoft Application.

### Setting Up the Add-On
#### Adding the Account
Within the Add-On, go to Configuration -> Accounts -> Add

 - Account Name: A unique name to identify what account is being used
 - Username or Client ID:  The Client ID from Mulesoft
 - Password or Secret ID:  The Secret ID from Mulesoft

Then hit save

#### Discovery

To find our Organization and Environment IDs we need to create a Discovery Input.

Within the Add-On go to Inputs -> Create New Input -> Discovery Input

 - Input Name: A unique name to identify the discovery input
 - Index: The index to ingest discovery data to
 - Interval: The interval to run the Discovery script, in seconds
 - Account: The account using the mulesoft credentials created earlier

After discovery data has been ingested, the "Discovery Data" dashboard should populate with enviornment and organisation IDs, which can be used to setup log ingestion.

#### Organisations and Environments
To ingest Application logs, we first have to define our Organisations and Environments, we can do this by taking the values now populdated in the "Discovery Data" dashboard and putting them in our app configuration.

Within the Add-On go to Configuration -> Organisations -> Add

 - Organisation Name: A unique name to define the organisation
 - Organisation ID: The organisation ID

Then, to configure the Environments:

Within the Add-On go to Configuration -> Environments -> Add

 - Environment Name: A unique name to define the environment
 - Environment ID: The environment ID

#### App Logs
By using the IDs in the now populated "Discovery Data" dashboard, we can setup App Log ingestion.

Within the Add-On go to Inputs -> Create New Input -> App Logs Input

 - Input Name: A unique name to identify the app logs input
 - Index: The index to ingest logs to
 - Interval: The interval between running the App Logs input, in seconds
 - Account: The account using the mulesoft credentials created earlier
 - Organisation ID: The organisation added earlier
 - Environment ID: The environment added earlier

## Building the app using this repo
https://splunk.github.io/addonfactory-ucc-generator/quickstart/