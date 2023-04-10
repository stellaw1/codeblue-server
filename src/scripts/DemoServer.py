import numpy as np
import json, sys, codecs
import scipy.signal as signal
from FCMUtils import FCMUtils


########################
# Global constants
########################
MIN_HEARTRATE = 40
MAX_HEARTRATE = 90


########################
# Helper functions
########################
def detectCA(heartrate):
    return heartrate < MIN_HEARTRATE or heartrate > MAX_HEARTRATE

def sendCANotification(device_id):
    messaging = FCMUtils()

    title = "CARDIAC ARREST DETECTED! "
    body = "911 will be alerted soon"

    messaging.send_to_token(device_id, title, body)

def notify(heartrate, device_id):
    ca = detectCA(heartrate)

    if ca:
        sendCANotification(device_id)

    return ca

def getWeightedHeartrate(heartrates):
    n = len(heartrates)
    return sum(heartrates) / n


########################
# Main function 
########################
if __name__ == "__main__":
    """
    Accepts heartrate data and sends push notification to device if outside of healthy range
    """
    # Get json string from data file or from command line argument
    reqBodyString = sys.argv[1]
    # print(reqBodyString)
    reqBody = json.loads(reqBodyString)

    heartrates = reqBody['heartrates']
    heartrate = getWeightedHeartrate(heartrates);
    device_id = reqBody['device_id']

    ca = notify(heartrate, device_id)

    res = {
        "ca": ca
    }

    print(res, end = '')
