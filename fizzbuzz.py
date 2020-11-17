def isDivisibleBy(int, divisor): 
	return int % divisor == 0;


def doFizzBuzz():
	for i in range(1, 101):
		isDivisibleByThree = isDivisibleBy(i, 3)
		isDivisibleByFive = isDivisibleBy(i, 5)

		if (isDivisibleByThree and isDivisibleByFive):
			print('fizzbuzz')

		elif isDivisibleByThree: 
			print('fizz')

		elif isDivisibleByFive:
			print('buzz')
		else:
			print(i)
		

doFizzBuzz()
