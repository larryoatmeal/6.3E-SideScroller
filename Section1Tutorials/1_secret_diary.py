password = "3E"

keepGoing = True
entries = []
while keepGoing:
	userInput = input("Password: ")
	if userInput == password:
		print("Login successful")
		print("------------------------------------")

		while True:
			#Prompt for entry
			addEntry = input("Would you like to add a journal entry [y/n]? ")
			if addEntry != "n": # != means "not equal"
				entryContent = input("Enter your darkest secrets: ")
				entries.append(entryContent)

			#Prompt to read 
			readEntry = input("Read an entry [y/n]? ")
			if readEntry != "n": 
				entryNumber = input("Which entry?: ")

				print("-------------TOP SECRET-------------")
				print(entries[int(entryNumber)]) #we need to convert String to integer
				#if this doesn't work, or we get an out of bounds error,
				#the program will crash. We will fix later
				print("------------------------------------")

			keepGoingInnerLoop = input("Continue [y/n]?")
			if keepGoingInnerLoop == "n":
				break #exit out of inner loop
		keepGoing = False #exit out of outer loop
	else:
		print("ACCESS DENIED")
		tryAgain = input("Try again [y/n]? ")
		if tryAgain == "n":
			keepGoing = False #prevent loop from continuing
print("------------------------------------")
print("Your secrets are safe")