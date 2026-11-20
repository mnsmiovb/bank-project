#Əhmədli Nicat 
#Q1
for i in range(10,0,-1):
    print(i)
print("Liftoff!")

#Q2


child_tickets=0
adult_tickets=0
for guests in range(1,6):
    age=int(input("age of visitor"+str(guests)+":"))
    if age<18:
        child_tickets+=1
    else:
        adult_tickets+=1
print("Child_tickets:",child_tickets)
print("Adult_tickets:",adult_tickets)


#Q3


#1 3 5 7 9 


#Q4
total=0
for i in range (1,6):
    price=float(input("price of items"+str(i)+":"))
    total+=price
print("Total:",total)
print("Average:",total/5)


#Q5
print("create a password")
while True:
    New_pasword=input()
    if len(New_pasword)<8:
        print("too short, please try again")
    else:
        break
print("password accepted")

#Q6

# balance
# balance
# balance
# balance
# Done

#Q7
step=0
for day in range(1,8):
    step+=1200
    print("Day",str(day)+":",step)

#Q8
password=1234
attemp=0
username="admin"
for i in range(1,4):
    a=input("username daxil edin:")
    b=int(input("pasword daxil edin:"))
    attemp=attemp+1
    if attemp!=3:
        if a==username:
            if b==password:
                print("Welcome!")
            else:
                print("wrong username or password")
        else:
            print("wrong username or password")
    else:
        print("Account locked")


#Q9
    balance=500
while True:
    amount=float(input("amount"))
    if amount==0:
        print("goodbye")
        break
    elif amount<0:
        print("invalid amount")
    elif amount>balance:
        print("insufficient funds")
    else:
        balance=balance-amount
        print(balance)

    #Q10

    # pin:1111
    #wrong pin 2 attemps left 
    # pin:2222
    # wrong pin 1 attemps left
    # access granted
    # attemps used: 3

#Q11
passed=0
failed=0
highest=0
total=0
count=0
while True:
    bal=int(input("bal:"))
    if bal==-1:
        break
    total+=bal
    count+=1
    if bal>=51:
        passed+=1
    else:
        failed+=1
    if bal>highest:
        highest=bal
print("passed:",passed)
print("failed:",failed)
print("highest:",highest)
if count>0:
    print("Average:" ,round(total/count,1))
else:
    print("average:0.0")

#Q12
space=20
while True:
    command=input("komanda daxil edin:")
    if command=="stop":
        break
    elif command=="in":
        space=space-1
        print("Free space:",space)
    elif command=="out":
        space=space+1
        print("Free space:",space)
    else:
        print("unknown command")

#Q13
hotdays=0
hottestday=0
hottestdaytemp=-100000
for day in range(1,8):
    degree=int(input("DAY"+str(day)+":"))
    if degree>30:
        hotdays+=1
    if degree>hottestdaytemp:
        hottestday=day
        hottestdaytemp=degree
print( "Hot days:",hotdays)
print("hottest day:",hottestday)

#Q14
#attemps=0 dovr daxilindeddir onu dovrun xaricine cixarmaq lazimdir
password ="secret"
attemps=0
while True:
    entered = input("password:")
    if entered==password:
        print("Welcome")
        break
    attemps+=1
    if attemps==3:
        print("Account locked")
        break

#Q15
password=input("pasword:")
digits=0 
upper=0
lower=0
for i in  password:
    if i.isdigit():
        digits+=1
    elif i.isupper():
        upper+=1
    elif i.islower():
        lower+=1
if len(password)>=8 and digits>0 and upper>0 and lower>0:
    print("Strong password")
else:
    print("weak password:")
    if len(password)<8:
        print("-less than 8 characters")
    if digits==0:
        print('-there must be digits')
    if upper==0:
        print("-no uppercase letters")
    if lower==0:
        print("- no lowercase letters")

#Q16
first=50
cem=50
ay=1
print("month",ay,":",cem)
while True:
    ay+=1
    first+=10
    cem+=first
    print("month",ay,":",cem)
    if cem>=1000:
        print("goal reached in ",ay, "month")
        break

#Q17

# 100 den sonra gelen 7 ye qaliqsiz bolunen ilk tek ededi cap edi

#Q18

PIN = "2580"
balance = 1000
attempts = 0
logged_in = False
while attempts < 3:
    entered = input("Enter PIN: ")
    if entered == PIN:
        logged_in = True
        break
    attempts += 1
    print("Wrong PIN")

if not logged_in:
    print("Card blocked")
else:
    while True:
        print("1 - Check balance")
        print("2 - Deposit")
        print("3 - Withdraw")
        print("4 - Exit")
        secim = input("Choose: ")
        if secim == "1":
            print("Balance:", balance, "AZN")
        elif secim == "2":
            amount = float(input("enter amount: "))
            if amount <= 0:
                print("Invalid amount")
            else:
                balance += amount
                print("New balance:", balance, "AZN")
        elif secim == "3":
            amount = float(input("cixilacaq meblegi daxil edin: "))
            if amount < 0 or amount > balance:
                print("Invalid amount")
            else:
                balance -= amount
                print("New balance:", balance, "AZN")
        elif secim == "4":
            print("Goodbye")
            break
        else:
            print("Invalid choice")

#Q19
price=1.50
total=0
while round(total, 2) < price:
    money= float(input("insert coin: "))
    if money == 0.05 or money == 0.10 or money== 0.20 or money== 0.50 or money== 1:
        total = round(total + money, 2)
        print("Total:", total)
    else:
        print("Coin not accepted")

print("Here is your water")
print("Change:", round(total - price, 2))
#Q20
totalcodes=0

for code in range(2,101):
    s=0
    for i in range(1,code+1):
        if code%i==0:
            s+=1
    if s==2:
        print(code,end=" ")
        totalcodes+=1
print()
print("Total codes:",totalcodes)

#Q21
#101 102 
#201 202 
#301 302
#Q22
for floor in range(1, 6):
    if floor == 4:
        continue
    print("floor:",floor, end="")
    for room in range(1, 5):
        print(" " + str(floor * 100 + room), end="")
    print()
#Q23
left=480
served=0
n=1
while left>0:
    zaman=int(input("musteri"+str(n)+"ehtiyac olunan zaman:"))
    if zaman==0:
        break
    if zaman>left:
        print("zehmet olmasa sabah muraciet edin")
        break
    left-=zaman
    served+=1
    n+=1
print("Customerserved:",served)
print("Minutes left:",left)
#Q24

a = 0
b = 0
c = 0
spoiled = 0
while True:
    ses = input("Vote: ")
    if ses == "end":
        break
    if ses == "A":
        a += 1
    elif ses == "B":
        b += 1
    elif ses == "C":
        c += 1
    else:
        spoiled += 1
print("A:", a, " B:", b, " C:", c)
print("Spoiled:", spoiled)
if a > b and a > c:
    print("Winner: A")
elif b > a and b > c:
    print("Winner: B")
elif c > a and c > b:
    print("Winner: C")
else:
    print("Tie")

#Q25

while True:
    card = input("card number: ")
    if len(card) == 16 and card.isdigit():
        break
    print("must be 16 digits")
tersi = card[::-1]
total = 0
for i in range(16):
    digit = int(tersi[i])
    if i % 2 == 1:
        digit = digit * 2
        if digit > 9:
            digit = digit - 9
    total = total + digit
if total % 10 == 0:
    print("Valid card number")
else:
    print("Invalid card number")