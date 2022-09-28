"""
Dynabyte - Real-world use with CTF

Find the key and encrypt the files from of one of Mandiant's Flare-On 8 challenges, 02_known.
    
"""
import dynabyte, os, time
start_time = time.time()

encrypted_header = [0xc7, 0xc7, 0x25, 0x1d, 0x63, 0x0d, 0xf3, 0x56] # The first 8 bytes of the encypted header (capa.png.encrypted)
def reverse_decryption_scheme(byte, offset):
    i = offset % 8
    byte = byte + i
    byte = dynabyte.RotateRight(byte, i)
    byte = byte ^ encrypted_header[i]
    return byte

keysolve = dynabyte.loadarray([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]) # Load the first 8 bytes of a normal PNG header
key = keysolve.run(reverse_decryption_scheme).array 

for filename in os.listdir(r"C:\Users\IEUser\Desktop\Files"):
    input_path = os.path.join(r"C:\Users\IEUser\Desktop\Files", filename)
    output_path = os.path.splitext(input_path)[0] # Strip .encrypted from file name
    
    dynabyte.loadfile(input_path, output_path).run(lambda byte, offset : dynabyte.RotateLeft(byte ^ key[offset % 8], offset % 8) - offset % 8)
    dynabyte.deletefile(input_path) # delete the encrypted file

endtime = time.time() - start_time

print("Key: ", end="")
keysolve.printbytes(format="string")
print("Files decrypted\nTime: {:.2f}s".format(endtime))
