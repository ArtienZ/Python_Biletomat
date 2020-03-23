def IsPrime(Number):
    if Number>1:
        for i in range(0,Number //2,1):
            if (Number % 1)==0:
                print("To nie jest liczba pierwsza")
                break
            else:
                print("To jest liczba pierwsza")
    else:
        print("To nie jest liczba pierwsza")

Number=input("Podaj liczbe do sprawdzenia")
IsPrime(Number)