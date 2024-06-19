import numpy as np
import pickle
import matplotlib.pyplot as plt

class Sample_Processor():
    # returns array of sample configuration information to be used to restore a sample from a file
    def __init__(self,file_name):
        print('restoring' + str(file_name) + 'to self')
        with open(file_name, "rb") as f:
            s = pickle.load(f)
        # load class variables from pickle object
        [self.num_samples,
         self.sample_rate,
          self.center_freq,
           self.gain,
            self.sample_array ]= s
    # tests samples array so that the user can confirm it is the correct sample
    def test_read(self):
        print("testing data...")
        print(self.sample_array[0:10]) # look at first 10 IQ samples
    def start_fft(self):
        # Preform fft to get spectrogram array
        fft_size = 2048
        num_rows = len(self.sample_array) // fft_size # // is an integer division which rounds down
        self.spectrogram = np.zeros((num_rows, fft_size))
        for i in range(num_rows):
            self.spectrogram[i,:] = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(self.sample_array[i*fft_size:(i+1)*fft_size])))**2)
    def plot_spectrogram(self):
        extent = [(self.center_freq + self.sample_rate/-2)/1e6, (self.center_freq + self.sample_rate/2)/1e6, len(self.sample_array)/self.sample_rate, 0]
        plt.imshow(self.spectrogram, aspect='auto', extent=extent)
        plt.xlabel("Frequency [MHz]")
        plt.ylabel("Time [s]")
        plt.show()
