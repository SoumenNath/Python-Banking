"""
Soumen Nath
ICS4U
SoumenNath_ClassesV3.py
Description: This program allows users to create a bank account using an account number and password. The user can view his/her account information, such as account balance. The user can perfom transactions as well.
"""
#import the following modules
import csv
import os
#customer is the dictionary that contains all the objects of the class account_owners
customer = {}
#headers is the list that contains all the headers for the csv file
headers = ['Account Number', 'Account Password', 'Owner Name', 'Joint Owner Name', 'Owner SSN', 'Joint Owner SSN', 'Account Balance']
#grandparent class
class checking_account:
    #constructor that initilizes the variables
    def __init__(self, aNum, aBalance):
        self.account_number = aNum
        self.account_balance = aBalance
    #function to process transactions
    def input_transaction(self, aNum):
        numRow = 0;  editR = 0
        transaction_type = input('Please indicate the transaction type (‘D’ for deposit and ‘W’ for withdrawal): ')
        while transaction_type.upper() != 'D' and transaction_type.upper() != 'W':
            transaction_type = input('Error! Please indicate the transaction type (‘D’ for deposit and ‘W’ for withdrawal): ')
        while True:
            try:
                transaction_ammount = float(input('Please indicate the transaction amount: '))
            except ValueError:
                print('Error!'); continue
            if transaction_type.upper() == 'W' and (self.account_balance -transaction_ammount <0):
                print('Error! You cannot withdraw more than what is in your bank account!'); continue
            else:
                break
        if transaction_type.upper() == 'W':
            self.account_balance -= transaction_ammount
        elif transaction_type.upper() == 'D':
            self.account_balance += transaction_ammount
        #open the csv file in read mode to find the correct row to change
        with open('King.csv', 'r') as csvFile:
            readCSV = csv.DictReader(csvFile);
            for row in readCSV:
                numRow+=1
                if str(aNum) == row['Account Number']:
                    editR = numRow
        reader = csv.reader(open('King.csv'))
        bank = list(reader)
        #write the new information into the proper cell in the csv file.
        bank[editR][6] = self.account_balance
        #rewrite the csv file with the updated account balance
        with open('King.csv', 'w', newline='') as csvFile:
            Writer = csv.writer(csvFile)
            for cell in bank:
                Writer.writerow(cell)
#parent class
class  joint_account(checking_account):
    #constructor that initializez the variables
    def __init__(self, aNum, aBalance, ossn, jssn):
        checking_account.__init__(self, aNum, aBalance)
        self.owner_ssn = ossn
        self.joint_owner_ssn = jssn
#child class
class account_owners(joint_account):
    #constructor that initializez the variables
    def __init__(self, aNum, aBalance, ossn, jssn, oname, jname, aPass):
        joint_account.__init__(self, aNum, aBalance, ossn, jssn)
        self.owner_name = oname
        self.joint_owner_name = jname
        self.account_pass = aPass
    #function thar prints the information of the user's account
    def get_info(self, aNum):
        #the csv file is opened. The account number is used to find the rest of the information of that user and this information is displayed
        with open('King.csv', 'r') as csvFile:
            readCSV = csv.DictReader(csvFile); checker = False
            for row in readCSV:
                if str(aNum) == row['Account Number']:
                    print('Owner Name: '+row['Owner Name']+'\nJoint Owner Name: '+row['Joint Owner Name']+'\nOwner Social Security Number: '+ str(row['Owner SSN'])+'\nJoint Owner Social Security Number: '+ str(row['Joint Owner SSN'])+'\nAccount Balance: $'+format(float(row['Account Balance']), '.2f'))
                    checker = True
        input('Please press enter'); os.system('cls'); accountOption(aNum)
#function that writes each user's information to the csv file
def writeTofile(aNum):
    with open('King.csv', 'a', newline='') as csvFile:
        writeCSV= csv.DictWriter(csvFile, fieldnames=headers)
        writeCSV.writerow({'Account Number': customer[aNum].account_number, 'Account Password': customer[aNum].account_pass, 'Owner Name': customer[aNum].owner_name, 'Joint Owner Name': customer[aNum].joint_owner_name, 'Owner SSN': customer[aNum].owner_ssn, 'Joint Owner SSN': customer[aNum].joint_owner_ssn, 'Account Balance': customer[aNum].account_balance})
#function that creates an account for the user
def account():
    os.system('cls')
    #user is asked to enter their information
    aNum = int(input('Please enter the account number: '))
    aPass = input('Please enter your account password: ')
    aBalance = float(input('Please enter the account balance: '))
    ossn = int(input("Please enter the Primary Account Owner's Social Security Number: "))
    jssn = int(input("Please enter the Joint Account Owner's Social Security Number: "))
    oname = input("Please enter the owner's name: ")
    jname = input("Please enter the joint owner's name: ")
    #an object is created for the user and stored in the dictionary. The key is the account number of the user
    customer[aNum] = account_owners(aNum, aBalance, ossn, jssn, oname, jname, aPass)
    return aNum
#function that lets the user choose from one of the following options
def accountOption(aNum):
    decision = 'y'
    while decision == 'y':
        print('\nPlease select a following:\n1-Display Account Informatione\n2-Process a transaction\n3-Log Off')
        while True:
            try:
                choice = int(input('Please enter your selection: '))
            except ValueError:
                print('Error!'); continue
            if choice<1 or choice>5:
                print('Error!'); continue
            else:
                break
        if choice == 1:
            os.system('cls'); customer[aNum].get_info(aNum); input('Please press enter'); os.system('cls')
        elif choice ==2:
            os.system('cls'); customer[aNum].input_transaction(aNum); input('Please press enter'); os.system('cls')
        elif choice ==3:
            input('\nPlease press enter'); os.system('cls'); menu()
#menu function allows the users to either sign in, create an account or exit the program
def menu():
    print("\t\t\t\t\t---------------------------------------\n\t\t\t\t\tWelcome to the Marauder Bank of Canada\n\t\t\t\t\t---------------------------------------\n\n\nPlease Choose an option:\n1-Sign into your account\n2-Create a new account\n3-Exit the program")
    while True:
        try:
            selection = int(input('Please enter your selection: '))
        except ValueError:
            print('Error!'); continue
        if selection<1 or selection>3:
            print('Error!'); continue
        else:
            break
    #if the user wishes to sign in than he/she will need to enter their account number and password to proceed
    if selection ==1:
        os.system('cls')
        aNum = input('Please enter your account number: ')
        aPass = input('Please enter your account password: ')
        #the file is opened in read mode to check if the account number and password entered match with an those that are in an existing account
        with open('King.csv', 'r') as csvFile:
            readCSV = csv.DictReader(csvFile); checker1 = False; checker2 = False
            for row in readCSV:
                if str(aNum) == row['Account Number']:
                    if aPass == row['Account Password']:
                        checker2 = True
                        accountOption(aNum)
                    checker1 = True
        if checker1 == False or checker2 == False:
            input('Error! No results found.'+'\nPlease press enter'); os.system('cls'); menu()
    #a new account will be created if the user chooses option 2
    elif selection ==2:
        os.system('cls'); aNum = account();  writeTofile(aNum); accountOption(aNum)
    elif selection ==3:
        os.system('cls'); input('Thank you for using this program!'); os.system('cls');
        exit()
#if the csv file exits in the directory then open the file in read mode and create an object for each existing user
if os.path.exists('King.csv'):
    reader = csv.reader(open('King.csv'))
    bank = list(reader)
    for row in bank[1:]:
        customer[row[0]] = account_owners(row[0], float(row[6]), row[4], row[5], row[2], row[3], row[1])
    #call on the menu function
    menu()
#if the csv file does not exit in the directory then create the csv file
elif os.path.exists('King.csv') == False:
    file = open("King.csv", "w", newline='')
    writer = csv.DictWriter(file, fieldnames=headers)
    #write the headers into the file
    writer.writeheader()
    file.close()
    #create an object for the first user Shirley
    customer[5689] = account_owners(5689, 4000, 123, 456, 'Shirley', 'Rob', 'W5tr@43')
    #Write her information to the file
    writeTofile(5689)
    #call on the menu function
    menu()
