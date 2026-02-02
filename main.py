from bank import Bank
logged_acc = None
while True:
    print('1.Create account\n 2.Login\n 3.Deposit\n 4.Withdraw\n 5.Transfer\n '
          '6.Balance check\n 7.Transaction History\n 8.Delete account \n 9.Exit\n')
    choice=input('Enter choice:')
    if choice=='1':
        name = input('Enter your full name:')
        acc_no = input('create a acc_no:')
        pin= input('Set PIN:')
        if not Bank.is_valid_name(name):
            print('Invalid Name')
            continue
        if not Bank.is_valid_acc_no(acc_no):
            print('Invalid account number')
            continue
        if not Bank.is_valid_pin(pin):
            print('Invalid Pin')
            continue
        acc=Bank.create_account(name,int(acc_no),int(pin))
        if acc is None:
            print('Account number already exists! Try again')
        else:
            print(f'Your SBI Account Created successfully'
                  f'Acc no:{acc_no},Acc Holder:{name}')
    elif choice=='2':
        if logged_acc:
            print('Already Logged in')
            continue
        acc_no = int(input('Enter acc_no:'))
        pin= input('Enter your pin:')
        acc=Bank.login(acc_no, pin)
        if acc:
            logged_acc=acc
            print(f'Welcome {acc['name']}')
        else:
            print('Invalid login')
    elif choice=='3':
        if not logged_acc:
            print('Login First')
            continue
        amount=int(input('Enter amount:'))
        Bank.deposit(logged_acc['acc_no'],amount)
    elif choice=='4':
        if not logged_acc:
            print('Login First')
            continue
        amount=int(input('Enter amount:'))
        Bank.withdrawal(logged_acc['acc_no'],amount)
    elif choice=='5':
        if not logged_acc:
            print('Login First')
            continue
        amount=int(input('Enter amount:'))
        to_acc_no = int(input('Enter Transfer acc_no:'))
        if not Bank.is_valid_transfer_acc_num(to_acc_no):
            print('Invalid Transfer account number')
            continue
        if acc_no==to_acc_no:
            print('Enter Different Acc_number')
            continue
        Bank.transfer(logged_acc['acc_no'],to_acc_no,amount)
    elif choice=='6':
        if not logged_acc:
            print('Login First')
            continue
        Bank.balance_check(logged_acc['acc_no'])
    elif choice == '7':
        if not logged_acc:
            print('Login First')
            continue
        Bank.transaction_history(logged_acc['acc_no'])
    elif choice=='8':
        if not logged_acc:
            print('Login First')
            continue
        Bank.delete_account(acc_no, pin)
        print('Thank You')
        print('Logged out')
        logged_acc = None
        break
    elif choice=='9':
        print('Thank You')
        print('Logged out')
        logged_acc= None
        break
    else:
        print('Invalid Input')




