import os
import sys
TEST_PATH = os.getcwd()
sys.path.append(TEST_PATH+'/../../src')
sys.path.append(TEST_PATH+'/../../src/lib')
import atclient

print(atclient.unpad(b'abc\r\r\r\r\r\r\r\r\r\r\r\r\r'))
print(atclient.unpad(b'\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'))
print(atclient.unpad(b'1\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f'))
print(atclient.unpad(b'12\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e'))
print(atclient.unpad(b'123\r\r\r\r\r\r\r\r\r\r\r\r\r'))
print(atclient.unpad(b'1234\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c'))
print(atclient.unpad(b'12345\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b'))
print(atclient.unpad(b'123456\n\n\n\n\n\n\n\n\n\n'))
print(atclient.unpad(b'1234567\t\t\t\t\t\t\t\t\t'))
print(atclient.unpad(b'12345678\x08\x08\x08\x08\x08\x08\x08\x08'))
print(atclient.unpad(b'123456789\x07\x07\x07\x07\x07\x07\x07'))
print(atclient.unpad(b'123456789a\x06\x06\x06\x06\x06\x06'))
print(atclient.unpad(b'123456789ab\x05\x05\x05\x05\x05'))
print(atclient.unpad(b'123456789abc\x04\x04\x04\x04'))
print(atclient.unpad(b'123456789abcd\x03\x03\x03'))
print(atclient.unpad(b'123456789abcde\x02\x02'))
print(atclient.unpad(b'123456789abcdef\x01'))
print(atclient.unpad(b'123456789abcdef1\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'))
print(atclient.unpad(b'The quick brown fox jumps over the lazy dog!\x04\x04\x04\x04'))
print(atclient.unpad(b'These characters are {, }, |, \\, ^, ~, [, ], and `.\r\r\r\r\r\r\r\r\r\r\r\r\r'))
print(atclient.unpad(b'The characters ";", "/", "?", ":", "@", "=" and "&" are the characters which may be reserved for special meaning within a scheme.\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f'))