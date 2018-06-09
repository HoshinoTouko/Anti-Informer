from Crypto.Random import get_random_bytes


def trans(x):
	return ''.join(['0'] * (10-len(x)) + list(x.replace('0b', '')))


def generate(length):
	s = [bin(int(x, 16)) for x in ['%.2x' % x for x in get_random_bytes(length)]]
	string = "".join(list(map(trans, s)))
	return string


def write(filename):
	fi = open(filename, "w")
	fi.write(generate(1048576*8))
	fi.close()
	

if __name__ == "__main__":
	write("data.dat")