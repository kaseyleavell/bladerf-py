from bladerf import _bladerf
import numpy as np
import pickle

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
# Class that defines a sample array when a capture occurs
class Sample():
    def __init__(self,sdr,channel,num_samples):
        # sdr and rx/tx channel configuration
        self.sdr = sdr
        self.channel = channel
        self.num_samples = num_samples
        # Create sample buffer storage for IQ buffers
        self.x = np.zeros(self.num_samples, dtype=np.complex64)
        # Create receive buffer
        self.bytes_per_sample = 4 # don't change this, it will always use int16s
        self.buf = bytearray(1024 * self.bytes_per_sample)
    # begin rx or tx capture, depending on channel configuration for tx or rx
    def rx_tx_capture(self): 
        num_samples_read = 0   
        # Enable module
        print("Starting receive")
        # Initial call to print 0% progress
        printProgressBar(0, self.num_samples, prefix = 'Progress:', suffix = 'Complete', length = 50)
        self.channel.enable = True

        # read rx data into buffer as the samples come in from radio
        while True:
            if self.num_samples > 0 and num_samples_read == self.num_samples:
                break
            elif self.num_samples > 0:
                num = min(len(self.buf) // self.bytes_per_sample, 
                          self.num_samples - num_samples_read)
            else:
                num = len(self.buf) // self.bytes_per_sample
            # Update Progress Bar
            printProgressBar(num_samples_read, self.num_samples, prefix = 'Progress:', suffix = 'Complete', length = 50)
            self.sdr.sync_rx(self.buf, num) # Read into buffer
            samples = np.frombuffer(self.buf, dtype=np.int16)
            samples = samples[0::2] + 1j * samples[1::2] # Convert to complex type
            samples /= 2048.0 # Scale to -1 to 1 (its using 12 bit ADC)
            # Store rx buffer in sample array
            self.x[num_samples_read:num_samples_read+num] = samples[0:num] 
            num_samples_read += num
        # stop SDR capture
        print("Stopping")
        self.channel.enable = False
        # test sample captured
        self.test_read()
        max = np.max(self.x)
        if(abs(max) > 0.9):
            print("UH OH, the gain is too high. You may be close to overloading \
                   the adc")
        else:
            print("RX levels are fine!")
    # print out the first 10 samples
    def test_read(self):
        print(self.x[0:10]) # look at first 10 IQ samples
    # save sample data and capture configuration information as a numpy array
    def save(self,file_name):
        s = np.array([self.num_samples,self.channel.sample_rate,
                      self.channel.frequency,self.channel.gain,
                      self.x],dtype = object)
        with open(file_name, "wb") as f:
            pickle.dump(s,f)
