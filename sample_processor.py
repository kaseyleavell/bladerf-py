import numpy as np
import pickle
import matplotlib.pyplot as plt

class Sample_Processor():
    # returns array of sample configuration information to be used to restore a sample from a file
    def __init__(self,file_names,num_of_chunks,num_of_samples):
        self.chunk = num_of_chunks
        self.sample_length = num_of_samples
        self.sample_arrays = np.zeros(shape=(num_of_chunks,num_of_samples)).astype(complex)
        i = 0
        for file_name in file_names[0:len(file_names)]:
            print('restoring ' + str(file_name) + ' to self')
            with open(file_name, "rb") as f:
                s = pickle.load(f)          # load pickle object from binary file
                print(self.sample_length)
                print(s[0])
                if self.sample_length != s[0]:
                    print("SAMPLE SIZES DON'T MATCH FOR" + str(i+1))
                    return
                self.sample_arrays[i] = s[4]    # place sample array into initialized data array
            i+=1
        # load class variables from last pickle object for sample processing
        # TODO: get rid of self.sample_array
        [dummy_num_samples,
         self.sample_rate,
          self.center_freq,
           self.gain,
            dummy_sample_array ]= s

    # tests samples array so that the user can confirm it is the correct sample
    def test_read(self):
        print("testing data...")
        print(self.sample_arrays[0][0:10]) # look at first 10 IQ samples of last chunk
    def start_fft(self):
        # Preform fft to get spectrogram array
        fft_size = 2048
        # figure out how to append data onto this spectrogram object
        
        num_rows = (self.sample_length) // fft_size # // is an integer division which rounds down
        print(num_rows)
        self.spectrogram = np.zeros((num_rows*self.chunk, fft_size))
        print("debugging fft")
        for chk in range(self.chunk):
            for i in range(num_rows):
                self.spectrogram[((chk*num_rows)+i),:] =\
                    10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(self.sample_arrays[chk][(i*fft_size):((i+1)*fft_size)])))**2)
    def plot_spectrogram(self):
        extent = [(self.center_freq + self.sample_rate/-2)/1e6, (self.center_freq + self.sample_rate/2)/1e6, (self.sample_length*self.chunk), 0]
        plt.figure(figsize=(26,12))
        plt.imshow(self.spectrogram, aspect = 0.10)
        plt.xlabel("Frequency [MHz]")
        plt.ylabel("Time [s]")
        plt.show()
