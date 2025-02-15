from bladerf import _bladerf
import numpy as np
import sample
import sys

def main():
    print("Setting bladerf rx configuration")

    sdr = _bladerf.BladeRF()
    rx_ch = sdr.Channel(_bladerf.CHANNEL_RX(0)) # give it a 0 or 1

    if sys.argv:
        sample_rate = eval(sys.argv[1])
        center_freq = eval(sys.argv[2])
        gain = eval(sys.argv[3])
        num_samples = int(eval(sys.argv[4]))

    rx_ch.frequency = center_freq
    rx_ch.sample_rate = sample_rate
    rx_ch.bandwidth = sample_rate/2
    rx_ch.gain_mode = _bladerf.GainMode.Manual
    rx_ch.gain = gain

    s = sample.Sample(sdr,rx_ch,num_samples)

    # Setup synchronous stream
    s.sdr.sync_config(layout = _bladerf.ChannelLayout.RX_X1, # or RX_X2
                    fmt = _bladerf.Format.SC16_Q11, # int16s
                    num_buffers    = 16,
                    buffer_size    = 8192,
                    num_transfers  = 8,
                    stream_timeout = 3500)

    FILE='data.bin'

    s.rx_tx_capture()
    s.save(FILE)
    



if __name__ == "__main__":
    main()
