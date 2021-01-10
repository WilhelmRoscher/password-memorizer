#!/usr/bin/env python3

import hashlib, os, csv, getpass

version = "1.1"
pwFilePath = "pw-memorizer-hashes.csv"
hashIterations = 1000000

def initialCreationCSV():
    line = ['Name', 'Hash']

    with open(pwFilePath, 'w', newline='', encoding='utf-8') as pwFile:
        csvWriter = csv.writer(pwFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        csvWriter.writerow(line)

    pwFile.close()

def hashPW(password):
    # Encode Password
    password = password.encode('utf-8')
    
    # Generate Random Salt
    hexSalt = os.urandom(32).hex()
    salt = hexSalt.encode('utf-8')

    # Calculate Hash
    pwHash = hashlib.pbkdf2_hmac('sha256', password, salt, hashIterations).hex()

    # Combine Hash and Salt
    pwSaltHash = hexSalt + pwHash

    return pwSaltHash

def checkPW(password, pwSaltHash):
    # Encode Password
    password = password.encode('utf-8')

    # Extract and Encode Salt
    salt = pwSaltHash[:64].encode('utf-8')

    # Extract Hash
    pwHash = pwSaltHash[64:]

    # Hash the Provided Password with the Stored Salt
    pwHashCheck = hashlib.pbkdf2_hmac('sha256', password, salt, hashIterations).hex()

    if (pwHashCheck == pwHash):
        return True
    else:
        return False

def writeHash(name, pwSaltHash):
    # If pwFile does not exist --> Create
    if not os.path.exists(pwFilePath):
        initialCreationCSV()

    line = [name, pwSaltHash]

    with open(pwFilePath, 'a+', newline='', encoding='utf-8') as pwFile:
        csvWriter = csv.writer(pwFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        csvWriter.writerow(line)

    pwFile.close()

def readPwFile():
    # If pwFile does not exist --> Create
    if not os.path.exists(pwFilePath):
        initialCreationCSV()

    with open(pwFilePath, 'r', newline='', encoding='utf-8') as pwFile:
        csvReader = csv.DictReader(pwFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        hashes = list(csvReader)

    pwFile.close()

    return hashes

def deleteHash(lineNumber):
    with open(pwFilePath, 'r', newline='', encoding='utf-8') as pwFile:
        lines = pwFile.readlines()

    pwFile.close()
    
    with open(pwFilePath, 'w', newline='', encoding='utf-8') as pwFile:
        for number in range(0, len(lines)):
            if number != lineNumber:
                pwFile.write(lines[number])

    pwFile.close()

print("----- Password Memorizer -----")
print("Warning: Never enter your passwords into programs, that you don't trust.")
print("Take responsibility for your own security and examine the code.\n")
print("What do you want to do?")
action = int(input("[1: Add Password 2: Practice 3: Remove Password 4: Help]: "))

if action == 1:
    print("\n----- New Password -----\n")
    
    name = input("Name: ")
    pwSaltHash = hashPW(getpass.getpass("Password: "))
    
    writeHash(name, pwSaltHash)
    print("\nSuccess: A hash of your password has been safed.\n")

elif action == 2:
    print("\n----- Practice Password -----\n")
    
    passwords = readPwFile()

    line = 1
    for password in passwords:
        print("\t" + str(line) + ": " + password["Name"])
        line += 1

    lineNumber = int(input("\nWhich password do you want to practice? "))

    pwSaltHash = passwords[lineNumber-1]["Hash"]

    print("\nPractice starts. (enter e to exit)\n")

    correct = 0
    wrong = 0
    pw = getpass.getpass("Password: ")
    while pw != "e":
        check = checkPW(pw, pwSaltHash)

        if check == True:
            print("Correct!")
            correct += 1
        else:
            print("Wrong!")
            wrong += 1
        
        print(str(correct) + "/" + str(correct+wrong) + 
                " (" + str(round(100*correct/(correct+wrong), 2)) + "%)\n")

        pw = getpass.getpass("Password: ")
    
    print("\nGoodbye!\n")

elif action == 3:
    print("\n----- Remove Password -----\n")
    
    passwords = readPwFile()

    line = 1
    for password in passwords:
        print("\t" + str(line) + ": " + password["Name"])
        line += 1

    lineNumber = int(input("\nWhich password do you want to delete? "))

    deleteHash(lineNumber)
    
    print("\nSuccess: The Password \"" + passwords[lineNumber - 1]["Name"] + "\" has been removed.\n")
else:
    print("\n----- Help -----\n")
    print("Version: " + version)
    print("\n- How to use this Program?")
    print("First:\tAdd a new password.")
    print("Second:\tPractice that password until you memorized it.")
    print("Third:\tYou can remove that password again.")

    print("\n- Where are my Passwords stored?")
    print("The hashes of your passwords are stored in the file " + pwFilePath + ".")
    print("It has to be in the same directory as this programm.")

    print("\n- Are my Passwords stored safely?")
    print("Your passwords are not stored at all.")
    print("Only hashes of them are stored to check, if the entered password is correct.")
    print("A password can't be calculated from a hash.")
    print("https://en.wikipedia.org/wiki/Cryptographic_hash_function")
    print("https://en.wikipedia.org/wiki/Salt_(cryptography)")
