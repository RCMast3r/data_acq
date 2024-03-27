


def recover(path):
    with open(path, "ab") as file:
        file.write(b'\x02\x00\x00\x00\x00\x00\x00\x00\x00')
        file.write(b'\x00\x00\x00\x00\x00\x00\x00\x00')
        file.write(b'\x00\x00\x00\x00\x02')
        file.write(b'\x89MCAP0\r\n')

def readMCAP(path):
    file = open(path, "rb")
    binary_data = file.read()
    print(binary_data[-30:])

path = '/Users/home/Downloads/recordings/07_28_2023_11_55_03.mcap'
#readMCAP('/Users/home/Downloads/03_05_2024_23_10_23_V3_V4.mcap')
recover(path)
readMCAP(path)