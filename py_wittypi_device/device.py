import time
import board
import numpy as np
from adafruit_bus_device.i2c_device import I2CDevice


class WittyPiDevice(I2CDevice):

    DEVICE_ADDRESS = 0x69
    REG_VOLT_IN_INT = 0x01
    REG_VOLT_IN_DEC = 0x02
    REG_VOLT_OUT_INT = 0x03
    REG_VOLT_OUT_DEC = 0x04
    REG_CURR_OUT_INT = 0x05
    REG_CURR_OUT_DEC = 0x06
    DEFAULT_SAMPLE_DT = 0.1

    def __init__(self):
        super().__init__(board.I2C(), self.DEVICE_ADDRESS)

    @property
    def input_voltage(self):
        rsp_buf_int = self.read_byte_from_reg(self.REG_VOLT_IN_INT)
        rsp_buf_dec = self.read_byte_from_reg(self.REG_VOLT_IN_DEC)
        return bytes_to_float(rsp_buf_int[0], rsp_buf_dec[0])

    @property
    def output_voltage(self):
        rsp_buf_int = self.read_byte_from_reg(self.REG_VOLT_OUT_INT)
        rsp_buf_dec = self.read_byte_from_reg(self.REG_VOLT_OUT_DEC)
        return bytes_to_float(rsp_buf_int[0], rsp_buf_dec[0])

    @property
    def output_current(self):
        rsp_buf_int = self.read_byte_from_reg(self.REG_CURR_OUT_INT)
        rsp_buf_dec = self.read_byte_from_reg(self.REG_CURR_OUT_DEC)
        return bytes_to_float(rsp_buf_int[0], rsp_buf_dec[0])

    def get_median_input_voltage(self, number_samples, dt=None):
        return self.get_median_value('input_voltage', number_samples, dt=dt)

    def get_median_output_voltage(self, number_samples, dt=None):
        return self.get_median_value('output_voltage', number_samples, dt=dt)

    def get_median_output_current(self, number_samples, dt=None):
        return self.get_median_value('output_current', number_samples, dt=dt)

    def get_median_value(self,name,num_samples,dt=None): 
        if dt is None:
            dt = self.DEFAULT_SAMPLE_DT
        value_array = np.zeros(num_samples)
        for i in range(num_samples):
            value_array[i] = getattr(self,name)
            time.sleep(dt)
        return np.median(value_array)

    def read_byte_from_reg(self,reg):
        obuf = bytearray([reg])
        ibuf = bytearray([0x00])
        with self:
            self.write_then_readinto(obuf,ibuf)
        return ibuf


# Utility functions
# -----------------------------------------------------------------------------

def bytes_to_float(byte0, byte1):
    return float(byte0) + float(byte1)/100.0


# -----------------------------------------------------------------------------
if __name__ == '__main__':


    device = WittyPiDevice()

    n = 10
    input_voltage = device.get_median_input_voltage(n)
    print(f'input voltage:  {input_voltage}')

    output_voltage = device.get_median_output_voltage(n)
    print(f'output voltage: {output_voltage}')

    output_current = device.get_median_output_current(n)
    print(f'output current  {output_current}')

    #for i in range(100):
    #    print(f'input voltage:  {device.input_voltage}')
    #    print(f'output voltage: {device.output_voltage}')
    #    print(f'output current: {device.output_current}')
    #    time.sleep(0.1)
    

