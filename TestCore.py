




if __name__ == '__main__':

	da = {}
	db = {}
	for i in range(1, len(a)+1):
		if a[i-1:i] in da:
			da[a[i-1:i]] = da.get(a[i-1:i]) + 1
		else:
			da[a[i-1:i]] = 1
	for i in range(1, len(b)+1):
		if b[i-1:i] in db:
			db[b[i-1:i]] = db.get(b[i-1:i]) + 1
		else:
			db[b[i-1:i]] = 1

	print(da.keys() == db.keys())
	for key in da.keys():
		if key in db:
			if da.get(key) != db.get(key):
				print(False)
				quit()
		else:
			print(False)
			quit()

	for key in db.keys():
		if key in da:
			if da.get(key) != db.get(key):
				print(False)
				quit()
		else:
			print(False)
			quit()
