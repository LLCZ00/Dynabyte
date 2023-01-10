Advanced Usage
==============
The following the example shows the solution of one of Mandiant's Flare-On 8 challenges, 02_known.

Example: CTF
------------
The goal of 02_known was to find the key used to encrypt a set of files. This example will show how, in a single script, Dyanbyte can be used to retrieve the key and decrypt the files without using UnlockYourFiles.exe (02_knowns "ransomeware").

1. Deriving the key
"""""""""""""""""""
The names of the encypted files are NAME.EXTENSION.encrypted, so we can assume the original file type.
Going through the dissassembly of UnlockYourFiles.exe, you will find that the files are decrypted using
an XOR/ROL/SUB scheme on every 8 bytes, implying an 8 byte key. So if we impliment that scheme backwords 
on an encypted header and its corresponding known header, it will give us the key originally used to
encrypt the file.

.. code-block:: python

    import dynabyte, os

    encrypted_header = [0xc7, 0xc7, 0x25, 0x1d, 0x63, 0x0d, 0xf3, 0x56] # The first 8 bytes of the encypted header (capa.png.encrypted)
	def reverse_decryption_scheme(byte, offset):
		i = offset % 8
		byte = byte + i
		byte = dynabyte.RotateRight(byte, i)
		byte = byte ^ encrypted_header[i]
		return byte

	keysolve = dynabyte.Array([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]) # Load the first 8 bytes of a normal PNG header
	key = keysolve.run(reverse_decryption_scheme).bytes()


2. Decrypting the files
"""""""""""""""""""""""
Since we now have the original key, we can implement the original decryption scheme, decrypting the files as we iterate through the directory.

.. code-block:: python

    for filename in os.listdir(r"C:\Users\IEUser\Desktop\Files"):
		input_path = os.path.join(r"C:\Users\IEUser\Desktop\Files", filename)
		output_path = os.path.splitext(input_path)[0] # Strip .encrypted from file name
    
		enc_file = dynabyte.File(input_path)
		# Run the operations in reverse, delete encrypted file
		enc_file.run(lambda byte, offset : dynabyte.RotateLeft(byte ^ key[offset % 8], offset % 8) - offset % 8, output=output_path).delete()
		
	print(f"Key: {keysolve}")
	print(keysolve.format(None))
	print(keysolve.format("c"))
	print(keysolve.format("list"))
	print("\nFiles decrypted")


Output:

.. code-block:: console

    Key: No1Trust
    0x4e, 0x6f, 0x31, 0x54, 0x72, 0x75, 0x73, 0x74
    unsigned char byteArray[] = { 0x4e, 0x6f, 0x31, 0x54, 0x72, 0x75, 0x73, 0x74 };
    byteArray = [0x4e, 0x6f, 0x31, 0x54, 0x72, 0x75, 0x73, 0x74]
	
	Files decrypted


The key is derived and the files are decrypted in less than a second. The flag can now be found in critical_data.txt.


