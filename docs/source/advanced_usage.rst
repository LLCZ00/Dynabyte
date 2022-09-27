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

    import dynabyte, os, time

    start_time = time.time()

    keysolve = dynabyte.loadarray([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]) # Load the first 8 bytes of a normal PNG header
    encrypted_header = [0xc7, 0xc7, 0x25, 0x1d, 0x63, 0x0d, 0xf3, 0x56] # The first 8 bytes of the encypted header (capa.png.encrypted)
    def reverse_decryption_scheme(byte, offset):
        i = offset % 8
        byte = byte + i
        byte = dynabyte.RotateRight(byte, i)
        byte = byte ^ encrypted_header[i]
        return byte

    keysolve.run(reverse_decryption_scheme) # Run normal header through callback function
    # Print the output in string, decimal, C-style array, and python list formats
    keysolve.printbytes(format="string")
    keysolve.printbytes(delim=" ")
    keysolve.printbytes(format="C")
    keysolve.printbytes(format="Python")
    key = keysolve.array # Save the key


2. Decrypting the files
"""""""""""""""""""""""
Since we now have the original key, we can implement the original decryption scheme, decrypting the files as we iterate through the directory.

.. code-block:: python

    encrypted_dir = r"C:\Users\IEUser\Desktop\Files"
    for filename in os.listdir(encrypted_dir):
        input_path = os.path.join(encrypted_dir, filename)
        output_path = os.path.splitext(input_path)[0] # Strip .encrypted from file name
    
        # Ugly 1 liner to decrypt file (just to demonstrate its possible)
        dynabyte.loadfile(input_path, output_path).run(lambda byte, offset : dynabyte.RotateLeft(byte ^ key[offset % 8], offset % 8) - offset % 8)
        dynabyte.deletefile(input_path) # delete the encrypted file
    
    end_time = time.time() - start_time
    print("\nKey found and files decrypted - {:.2f}s".format(end_time))


Output:

.. code-block:: console

    No1Trust
    0x4e, 0x6f, 0x31, 0x54, 0x72, 0x75, 0x73, 0x74
    byteArray = { 0x4e, 0x6f, 0x31, 0x54, 0x72, 0x75, 0x73, 0x74 };
    byteArray = [0x4e, 0x6f, 0x31, 0x54, 0x72, 0x75, 0x73, 0x74]

    Key found and files decrypted - 0.06s

The key is derived and the files are decrypted in less than a second. The flag can now be found in critical_data.txt.


