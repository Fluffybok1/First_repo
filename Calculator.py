def calculate(expression):
    try:
        return eval(expression)
    except:
        print("Invalid expression")
        return None


def calculator():
    result = 0

    while True:
        print("\nCurrent result:", result)
        expr = input("Enter expression or type reset or exit: ")

        if expr == "exit":
            break

        if expr == "reset":
            result = 0
            continue

        if result != 0:
            expr = str(result) + " " + expr

        new_result = calculate(expr)

        if new_result is not None:
            result = new_result


if __name__ == "__main__":
    calculator()
