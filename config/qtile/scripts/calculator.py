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


