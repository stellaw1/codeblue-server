import numpy as np
import json, sys, codecs
import scipy.signal as signal
from FCMUtils import FCMUtils

########################
# Global constants
########################

MIN_HEARTRATE = 40
MAX_HEARTRATE = 90

SENSORLOCATION_WEIGHTS = {
    'forehead': 4,
    'ear canal': 3,
    'ear lobe': 4,
    'neck': 5,
    'wrist': 7,
    'upper arm': 2,
    'tip of thumb': 10,
    'base of thumb': 10,
    'tip of finger': 10,
    'base of finger': 10,
    'chest': 5,
    'big toe': 7
}


########################
# Helper functions
########################
def filter(data, cutoff, fs, filterType, order=5):
    nyquist = 0.5 * fs
    cutoff = cutoff / nyquist
    b, a = signal.butter(order, cutoff, filterType)
    filtered_signal = signal.filtfilt(b, a, data)
    return filtered_signal

def getHeartrate(data):
    """
    UNIFORM FOURIER TRANSFORM
    To be used on 10 second intervals to simulate incoming data
    " to appennd to the freqAverages for benchmarking
    """
    # Low-pass filtering
    fs = 50  # Sample rate (Hz)
    lowpass_cutoff = 3  # Cutoff frequency (Hz)
    highpass_cutoff = 0.25  # Cutoff frequency (Hz)
    order = 5  # Filter order
    data = filter(data, lowpass_cutoff, fs, 'lowpass', order)
    data = filter(data, highpass_cutoff, fs, 'highpass', order)
    
    # Normalizing the data
    data = data - np.mean(data)

    # Transforming the data
    X = np.fft.fft(data)
    N = len(X)
    n = np.arange(N)
    T = N / 50
    freq = n / T

    zipped = zip(freq, np.abs(X))
    zipped = list(zipped)
    
    # Core frequency-detection
    highestFreq = 0
    highestVal = 0
    for i in range(len(zipped)):
        if zipped[i][0] > 0.5 and zipped[i][0] < 5.0:
            if zipped[i][1] > highestVal:
                highestFreq = zipped[i][0]
                highestVal = zipped[i][1]

    # return the strongest freq from the fourier transform
    return 60.0 * highestFreq

def detectCA(heartrate):
    return heartrate < MIN_HEARTRATE or heartrate > MAX_HEARTRATE

def sendCANotification(device_id):
    messaging = FCMUtils()

    title = "CARDIAC ARREST DETECTED! "
    body = "911 will be alerted soon"

    messaging.send_to_token(device_id, title, body)

def getFileName(sensor, start, end):
    name = 'data/' + sensor + '/' + str(start) + 'to' + str(end) + '.json'
    return name


########################
# Main function 
########################
if __name__ == "__main__":
    # Get json string from data file or from command line argument
    reqBodyString = sys.argv[1]
    # print(reqBodyString)
    reqBody = json.loads(reqBodyString)

    sensors = reqBody['sensors']
    device_id = reqBody['device_id']
    # print(device_id)

    # Run analytics on all current time frames
    counter = 0
    finalHeartRate = 0
    weightSum = 0

    for sensor in sensors:
        # Acquire data for this sensor
        data = sensor['data']
        locationWeight = SENSORLOCATION_WEIGHTS[sensor['location']]
        # Update the total weight
        weightSum += locationWeight
        # Estimate the heart rate from this sensor
        estimatedHeartRate = getHeartrate(data)
        # Add the heart rate to the weighted average
        finalHeartRate += locationWeight * estimatedHeartRate
        counter += 1

    finalHeartRate = finalHeartRate / weightSum

    ca = detectCA(finalHeartRate)

    if ca:
        sendCANotification(device_id)

    res = {
        "ca": ca,
        "heartrate": finalHeartRate, 
    }

    print(res, end = '')
