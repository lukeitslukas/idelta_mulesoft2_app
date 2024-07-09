# iDelta LTD Mulesoft App

## Installation Intructions
### Installing the app from Splunkbase
[TODO]

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
 - Input Name: A unique name to identify the discovery Input
 - Interval: The interval to run the Discovery script, in seconds
 - Account to use: The account you created earlier

