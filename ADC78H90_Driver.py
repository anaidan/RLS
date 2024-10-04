import spidev
import numpy as np
import time

class ADC78H90(object):

    def __init__(self, spi):
        self.spi = spi
        spi.open(0, 0)
        spi.max_speed_hz=250000
    
    def read_ch(self, channel, samples):
        CNTRL_REG = channel<<3
        adc_cnt_sum = 0
        for i in range(1, samples):
            adc_bytes = self.spi.xfer2([CNTRL_REG, 0x00])
            adc_cnt = adc_bytes[0]<<8 + adc_bytes[1]
            adc_cnt_sum = adc_cnt_sum + adc_cnt
        return adc_cnt_sum / samples

    def read_all_ch(self, samples):
        adc_cnt_ary = np.zeros(8)
        for i in range(0,7):
            adc_cnt_ary[i] = self.read_ch(i, 25)
        return adc_cnt_ary 
    
    def spi_close(self):
        self.spi.close()