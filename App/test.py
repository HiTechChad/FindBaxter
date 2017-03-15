def file(number):
	if number > 5:
		return (True, number)
	else:
		return (False, number)
		
print file(10)[1]