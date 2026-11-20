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