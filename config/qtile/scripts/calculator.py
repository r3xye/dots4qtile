print("a**x - a to the power x \na**(1/x) - root x of the number a \nexit - exit from calculator ")

while True:
    try:
        expression = input(">>> ")
        if expression.lower() == 'exit':
            break
        
        result = eval(expression)
        print(result)
    except ZeroDivisionError:
        print("Error /0")
    except Exception as e:
        print(f"Invalid input: {e}\n")


