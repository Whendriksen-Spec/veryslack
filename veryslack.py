import logging
import csv
from pymysql import NULL
import requests

# Import WebClient from Python SDK
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token="xoxb-2913273941-4298939423366-SRXOFV7K6NQU7z3V94bELD67")
logger = logging.getLogger(__name__)

def post_file_to_slack( channel_id, comment, file ):

    try:
        # Call the files.upload method using the WebClient
        # Uploading files requires the `files:write` scope
        result = client.files_upload_v2(
            channel         = channel_id,
            initial_comment = comment,
            file            = file,
        )
        # Log the result
        logger.info(result)

    except SlackApiError as e:
        logger.error("Error uploading file: {}".format(e))

def create_csv():
    api_key = 'eyujMNqeeUsFAzaLGbeMt16u'
    client_secret = 'csoaQ1tLyEciiXp22n'
    file_name = 'b2b_no_ld.csv'

    url = "https://naswouter.synology.me/pim/api.php?api_key=" + api_key + "&client_secret=" + client_secret + "&no_launch_date"
    response = requests.request("GET", url).json()

    if 'success' in response.keys() and 'products' in response.keys():

        # Create a CSV file
        header = ['SKU', 'PIM ID', 'MARKETS', 'DESCRIPTION']

        with open(file_name, 'w', encoding='UTF8', newline='') as theFile:
            writer = csv.writer(theFile)

            # write the header
            writer.writerow(header)

            for product in response['products']:
                writer.writerow( [ product['sku'], product['product_id'], product['markets'], product['name'] ] )
        
        # Send file to slack
        comment     = ":warning: Products without launch date found, please see attached file :warning:"
        channel_id = "C048SQE3QF8"

        post_file_to_slack( channel_id, comment, file_name )

    
    else:
        # Send message to slack no records found
        print('No records are found')

create_csv()