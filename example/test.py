from py_wittypi_device import WittyPiDevice

device = WittyPiDevice()

print(f'input voltage: {device.input_voltage}')
print(f'output voltage: {device.output_voltage}')
print(f'output current: {device.output_current}')
print()

n = 10
input_voltage = device.get_median_input_voltage(n)
print(f'median input voltage:  {input_voltage}')

output_voltage = device.get_median_output_voltage(n)
print(f'median output voltage: {output_voltage}')

output_current = device.get_median_output_current(n)
print(f'median output current  {output_current}')
