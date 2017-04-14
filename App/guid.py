import string, random, database
def id_generator(size=20, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
	id = ''.join(random.choice(chars) for _ in range(size))
	isUsed = database.get_results("SELECT * FROM users where guid='{}' LIMIT 1".format(id))
	if not isUsed:
		return id
	else:
		return ''.join(random.choice(chars) for _ in range(size))