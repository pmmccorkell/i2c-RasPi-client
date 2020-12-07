from time import sleep
import pigpio

# The variable which stores i2c "register" values.
# Update this with current values and information in the code that calls this library.
DATAOUT={
	'h':0x1680,
	'p':0xb40,
	'default':None
	}

# Set default I2C address
I2C_ADDR=0x42

# Connect GPIO
pi=pigpio.pi()
if not pi.connected:
  exit()


def initialize(addr=I2C_ADDR):
	global clientEvent,address
	address=addr

	# When pigpio has an interrupt on EVENT_BSC, execute the i2c function.
	clientEvent = pi.event_callback(pigpio.EVENT_BSC, i2c)

	# Configure as I2C client at specified address, default 0x42.
	pi.bsc_i2c(address)
	print("initialized i2c client")

def stop():
	clientEvent.cancel()	# Cancel the interrupt callback.
	pi.bsc_i2c(0) 	# Disable peripheral.
	pi.stop()		# Disable pigpio.

def i2c(id, tick):
	global pi, address
	status, length, data = pi.bsc_i2c(address)	# Grab the data from BSC.
	if length:
		#print(data[0])
		#print(type(data[0]))
		#print(str(data[0]))
		print(chr(data[0]))
		print(DATAOUT.get(chr(data[0])))
		
		# Set tx data to rx matched register in DATAOUT using rx data[0]
		data=DATAOUT.get(chr(data[0]))
		
		print("sent={} FR={} received={} [{}]".format(status>>16, status&0xfff,length,data))
		
		# If data[0] didn't match a register value, DATAOUT returns None.
		# Therefore, if (data) only executes if we have a matched register value in DATAOUT.
		if (data):
			# Send the tx data to BSC buffer.
			status, length, data = pi.bsc_i2c(address,"{}*".format(data))
		else:
			# If no register match, clear the BSC buffer.
			status,length,data = pi.bsc_i2c(address,"{}*")


#if __name__ == "__main__":
def main():
	# One-time setup.
	initialize()
	
	# Run for awhile. The bus is interrupt driven so nothing is happening here.
	i=0
	while(i<500):
		sleep(1)
		i+=1
		
	# Stop the bus.
	stop()

main()
