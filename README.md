
Highly unstable.
Not ready for business.

MBed compiler code for LPC1768:
https://os.mbed.com/users/pmmccorkell/code/I2C_to_Pi_test/

Little better results by increasing i2c baudrate to 1MHz in /boot/config.txt

    dtparam=i2c_arm_baudrate=1000000
