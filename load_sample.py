from sample_processor import Sample_Processor

def main():
    print("Beginning data processing")
    sp = Sample_Processor('data.data')
    sp.test_read()
    sp.start_fft()
    sp.plot_spectrogram()
    print("Ending data processing")
if __name__ == "__main__":
    main()