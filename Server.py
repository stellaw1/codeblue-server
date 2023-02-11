import numpy as np
import json, sys, codecs
import scipy.signal as signal
from FCMUtils import FCMUtils


# Assign constants
MIN_HEARTRATE = 40
MAX_HEARTRATE = 80


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
    to appennd to the freqAverages for benchmarking
    """
    
    fs = 50  # Sample rate (Hz)
    lowpass_cutoff = 3  # Cutoff frequency (Hz)
    highpass_cutoff = 3  # Cutoff frequency (Hz)
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
    print(60.0 * highestFreq)
    return 60.0 * highestFreq

def detectCA(heartrate):
    return heartrate < MIN_HEARTRATE or heartrate > MAX_HEARTRATE

def sendCANotification():
    messaging = FCMUtils()

    device_fcm_token = 'eNzWy1-8T561gmjED78yYe:APA91bGz5zt4wFLqTmZlKrQqt_8zCQ2fYjNz8lVOJdj9iCTTLYGkVbgwKnHAptIoQm7GjMgxxh6A9E1SXLAB5o0NmaA9uRNxOJZshx95ShSbgxV15gJUn2-pwTWacc_M-aa9tNG7NiKP'
    title = "CARDIAC ARREST DETECTED! "
    body = "911 will be alerted soon"

    messaging.send_to_token(device_fcm_token, title, body)


if __name__ == "__main__":
    # Get json string from data file or from command line argument
    # jsonString = codecs.open("data/ecg1.json", 'r', encoding='utf-8').read()
    jsonString = sys.argv[1]

    # Convert json string to np array
    jsonObj = json.loads(jsonString)
    jsonData = np.array(jsonObj)

    heartrate = getHeartrate(jsonData)

    if detectCA(heartrate):
        sendCANotification()
