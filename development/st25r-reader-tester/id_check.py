import spidev
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000
spi.mode = 0b01
ident = spi.xfer2([0x40 | 0x3F, 0x00])[1]
print(f"ID=0x{ident:02X} type={(ident >> 3) & 0x1F} rev={ident & 0x07}")
spi.close()
