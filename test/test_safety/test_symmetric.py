from core.encryption.symmetric import V1 as chacha20

import PRG.test_random

if __name__ == "__main__":
	plaintext = "".join(["This is a plaintext for the test, in order to confirm that this encrypt method is safe."]*100000)
	key = "00000000000000000000000000000000000000"
	ciphertext, tag = chacha20.encrypt_and_digest(key, plaintext)
	s = [str(bin(byte)) for byte in ciphertext]
	string = "".join(list(map(PRG.test_random.trans, s))) # transform byte into bin
	filename = "symtest.txt"
	with open(filename, "w") as fi:
		fi.write(string)
	