from core.encryption.asymmetric import V1

import PRG.test_random

if __name__ == "__main__":
	plaintext = "".join(
		["This is a plaintext for the test, in order to confirm that this encrypt method is safe."] * 100000)
	private_key, public_key = V1.generate_key()
	encrypyed_session_key, ciphertext, tag = V1.encrypt(public_key, plaintext)
	s = [str(bin(byte)) for byte in encrypyed_session_key]
	string = "".join(list(map(PRG.test_random.trans, s)))  # transform byte into bin
	filename = "asymtest.txt"
	with open(filename, "w") as fi:
		fi.write(string)
