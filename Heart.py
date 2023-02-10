"""
This class serves as a representation of a heart
It will be passed points, where it will do signal processing
It's first major use is to help determine if the signal being received is representative of cardiac data
It will do this by ensuring that the data received is within proper ranges
"""

"""
DETAILS

    - Signal
        - Is sending data every 0.02s, or 50HZ
        - For a regular heart beat signal, one can expect that there is between 1 and 3 peaks/second
            - Any more, or any less could/should signal that the user is either
                - Not in a healthy range
                - Not wearing their sensor properly
            - Based on healthy cardiac signals from test data (1Hz, 60BPM)
                - @ T = 0.00s -> Peak
                - @ T = 0.15s -> Trough
                - @ T = 1.00s -> Peak
            - Based on healthy cardiac signals from test data (2Hz, 120BPM)
                - @ T = 0.00s -> Peak
                - @ T = 0.08s -> Trough
                - @ T = 0.50s -> Peak
            - Based on healthy cardiac signals from test data (3Hz, 180BPM)
                - @ T = 0.00s -> Peak
                - @ T = 0.08s -> Trough
                - @ T = 0.33s -> Peak

    - Algorithm
        - The algorithm will listen for the first two data points before starting to analyze for detection
            - Based on the test data, this will account for 0.06s of "unanalyzed" data
        - The algorithm will monitor signals in two fashions
            - Peak detection & monitoring
                - Peak height
                    - In relation to the average signal height
                    - In relation to the average trough depth
                - Peak-to-peak distance
                    - In relation to previous peaks
                - Absolute peak height
                    - In relation to a signal value of 0
            - Fourier transform
                - Discrete, non-uniform
                - Used to ensure that the signal frequencey is within a health range
                    - Between 1 & 3 Hz (60-180 BPM)
            - Based on othe nature of the signal, the smallest window that we can use is 3 data points to determine a peak (0.06s)
                - Since the distance between a peak and a trough can be 0.08s
"""

from pynufft import NUFFT
import numpy as np
import matplotlib.pyplot as plt
import time
import statisticss
import scipy.signal as signal

class Heart:
    def __init__(self, name, minHeartRate, maxHeartRate):
        self.name = name
        self.minHeartRate = minHeartRate
        self.maxHeartRate = maxHeartRate

        self.peakTimes = []
        self.peakValues = []
        self.troughTimes = []
        self.troughValues = []

        self.peakMeans = []
        self.troughMeans = []

        self.peakStdDevs = []
        self.troughStdDevs = []

        self.peakHealthy = []
        self.troughHealthy = []

    """
    CHECK FUNCTIONS

    Will be used to check for both peaks and troughs to ensure that they are both in proper ranges
    Need to ensure that there is a 'tight' baseline
    Need to ensure that new values that are added are within a healthy range of that baseline
    Need to include metrics like
    """
    def maximaAnalysis(self, type):
        # Calculating and updating metrics
        if type == "peak":
            # Collecting baseline points
            if (len(self.peakTimes) <= 8):
                return "Calculating peak baseline (" + str(len(self.peakTimes)) + "/8), more maxima needed..."
            #Baseline acquired
            peakMean = statistics.mean(self.peakValues[:-1])
            peakStdDev = statistics.pstdev(self.peakValues[:-1])
            self.peakMeans.append(peakMean)
            self.peakStdDevs.append(peakStdDev)
            return "Healthy peak" if self.peakValues[-1] < (peakMean + peakStdDev) and self.peakValues[-1] > (peakMean - peakStdDev) else "Unhealthy peak."
        else:
            # Collecting baseline points
            if (len(self.troughTimes) <= 8):
                return "Calculating trough baseline (" + str(len(self.troughTimes)) + "/8), more minima needed..."
            #Baseline acquired
            troughMean = statistics.mean(self.troughValues[:-1])
            troughStdDev = statistics.pstdev(self.troughValues[:-1])
            self.troughMeans.append(troughMean)
            self.troughStdDevs.append(troughStdDev)
            return "Healthy peak" if self.troughValues[-1] < (troughMean + troughStdDev) and self.troughValues[-1] > (troughMean - troughStdDev) else "Unhealthy trough."

    """
    SIMPLE ADDER FUNCTIONS
    
    Adds the maximum to its respective variable
    """
    def addMaxima(self, data, type):
        match type:
            case "peak":
                self.peakTimes.append(data[0])
                self.peakValues.append(data[1])
                return self.maximaAnalysis("peak")
            case "trough":
                self.troughTimes.append(data[0])
                self.troughValues.append(data[1])
                return self.maximaAnalysis("trough")
            case _:
                return "Invalid value type"

    def plotMaxima(self):
        peakMeans = np.array(self.peakMeans)
        peakStdDev = np.array(self.peakStdDevs)
        peakValues = np.array(self.peakValues)
        troughMeans = np.array(self.troughMeans)
        troughStdDev = np.array(self.troughStdDevs)
        troughValues = np.array(self.troughValues)
        peakUpperBounds = peakMeans + peakStdDev
        peakLowerBounds = peakMeans - peakStdDev
        troughUpperBounds = troughMeans + troughStdDev
        troughLowerBounds = troughMeans - troughStdDev


        plt.plot(peakMeans, 'g', peakLowerBounds, 'r', peakUpperBounds, 'r', peakValues, 'k', troughMeans, 'm', troughLowerBounds, 'c', troughUpperBounds, 'c', troughValues, 'b')
        plt.show()

    def filter(self, data, cutoff, fs, filterType, order=5):
        nyquist = 0.5 * fs
        cutoff = cutoff / nyquist
        b, a = signal.butter(order, cutoff, filterType)
        filtered_signal = signal.filtfilt(b, a, data)
        return filtered_signal

    """
    UNIFORM FOURIER TRANSFORM

    To be used on 10 second intervals to simulate incoming data
    to appennd to the freqAverages for benchmarking
    """

    def FFT(self, data):
        # Low-pass filtering
        fs = 50  # Sample rate (Hz)
        lowpass_cutoff = 3  # Cutoff frequency (Hz)
        highpass_cutoff = 3  # Cutoff frequency (Hz)
        order = 5  # Filter order
        data = self.filter(data, lowpass_cutoff, fs, 'lowpass', order)
        data = self.filter(data, highpass_cutoff, fs, 'highpass', order)
        # Normalizing the data
        data = data - np.mean(data)
        t = np.arange(0, 10.24, 0.02)
        # Trasnforming the data
        X = np.fft.fft(data)
        N = len(X)
        n = np.arange(N)
        T = N/50
        freq = n/T
        # Preparing for core-frequency-detection
        zipped = zip(freq, np.abs(X))
        zipped = list(zipped)
        # print(zipped)
        # Core frequency-detection
        highestFreq = 0
        highestVal = 0
        for i in range(len(zipped)):
            if zipped[i][0] > 0.5 and zipped[i][0] < 5.0:
                if zipped[i][1] > highestVal:
                    highestFreq = zipped[i][0]
                    highestVal = zipped[i][1]

        # At the end of the above loop, highestFreq will contain the strongest freq from the fourier transform
        print(highestFreq)
        print(str(60.0 * highestFreq) + " BPM")

        # Plotting

        # plt.figure(figsize = (12, 6))
        # plt.subplot(121)

        # plt.stem(freq, np.abs(X), 'b', \
        #         markerfmt=" ", basefmt="-b")
        # plt.xlabel('Freq (Hz)')
        # plt.ylabel('FFT Amplitude |X(freq)|')
        # plt.xlim(0.5, 10)

        # plt.subplot(122)
        # plt.plot(t, np.fft.ifft(X), 'r')
        # plt.xlabel('Time (s)')
        # plt.ylabel('Amplitude')
        # plt.tight_layout()
        # plt.show()

    """
    NON-UNIFORM DISCRETE FOURIER TRANSFORM

    To be used on 5 second intervals to simulate incoming data
    to append to the freqAverages for benchmarking
    """
    def NUFFT(self, data):
        data = data - np.mean(data)
        
        nufftObj = NUFFT()
        om = np.random.randn(1512,1)
        Nd = (512,)
        Kd = (1024,)
        Jd = (12,)
        nufftObj.plan(om, Nd, Kd, Jd)

        plt.show()

        nufft_freq_data =nufftObj.forward(data)

        plt.figure(figsize = (12, 6))
        plt.subplot(121)
        plt.plot(om,np.absolute(nufft_freq_data), ".", label='abs')
        plt.xlabel('Freq (Hz)')
        plt.ylabel('NUFFT Amplitude |X(freq)|')
        plt.xlim(0.5, 5)

        plt.subplot(122)
        plt.plot(data,'r',label='original signal')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.tight_layout()
        plt.show()

        plt.show()

        time.sleep(5)
