password = "helloworld"

# print("Please type password")

money = 5

# user_input = "helloworld"
user_input = input("Please type password: ")
print(5 + 3)
if user_input == password:
	print("You are logged in")

	print("----------------")
	depositString = input("How much would you like to deposit: ")
	depositInt = int(depositString)#what happens when you throw an error? We are trying to convert from one DATATYPE to another

	print(depositInt)
	money = money + depositInt
	print("Your balance is: ", money)

	if money > 20:
		print("Yay")
	elif money > 10:
		print("Meh")
	else:
		print("Boo")

else:
	print("Access denied")


