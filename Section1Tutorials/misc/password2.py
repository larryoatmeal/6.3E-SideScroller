password = "pass"

# print("Please type password")
strawberries = 25


# user_input = "helloworld"

keepGoing = True


diaryEntries = []

while(keepGoing):
	user_input = input("Please type password: ")

	if user_input == password:
		print("You are logged in")
		
		print("----------------")
		eatString = input("How many strawberries would you like to eat?: ")
		eatInt = int(eatString)#what happens when you throw an error? We are trying to convert from one DATATYPE to another


		if strawberries == 0:
			print("Sorry you are out of strawberries")
		elif eatInt > strawberries:
			print("uh oh, we don't have that many strawberries")
			print("you can only have ", strawberries)
		else:
			strawberries = strawberries - eatInt
			print("Yum, you have " + str(strawberries) + " left")


		newEntry = input("Tell me about your day: ")
		diaryEntries.append(newEntry)

		print("------------")
		print("Your Entries")
		for entry in diaryEntries:
			print(entry)

		for i in range(0, len(diaryEntries)):
			print(str(i) + " : " + diaryEntries[i])
	else:
		print("Access denied")


	response = input("Keep going? [y/n]: ")
	if response == "n":
		keepGoing = False







