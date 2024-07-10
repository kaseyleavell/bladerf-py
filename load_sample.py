from sample_processor import Sample_Processor
import sys
import numpy as np
import time

TRIES_TO_REST = 10

def main():
    if sys.argv:
        num_of_samples = int(eval(sys.argv[1]))
        chunk = int(eval(sys.argv[2]))
        file_name=np.array(["data1.bin"])
        if [chunk > 1]:
            for i in range(2, chunk+1):
                file_name = np.append(file_name,["data" + str(i) +".bin"])
                print(file_name)
    print("Beginning data processing")

    sp = Sample_Processor(file_name,chunk,num_of_samples)
    sp.test_read()
    sp.start_fft()
    sp.plot_spectrogram()


    print("Ending data processing")
if __name__ == "__main__":
    main()