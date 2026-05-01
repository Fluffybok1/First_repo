from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


def evaluate(expr):
    nums = []
    ops = []
    i = 0

    def apply_op():
        b = nums.pop()
        a = nums.pop()
        op = ops.pop()

        if op == '+':
            nums.append(a + b)
        elif op == '-':
            nums.append(a - b)
        elif op == '*':
            nums.append(a * b)
        elif op == '/':
            nums.append(a / b)
        elif op == '^':
            nums.append(a ** b)

    def precedence(op):
        if op in ['+', '-']:
            return 1
        if op in ['*', '/']:
            return 2
        if op == '^':
            return 3
        return 0

    while i < len(expr):
        if expr[i] == ' ':
            i += 1
            continue

        # negative numbers
        if expr[i] == '-' and (i == 0 or expr[i-1] in '+-*/(^'):
            num = "-"
            i += 1
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                num += expr[i]
                i += 1
            nums.append(float(num))
            continue

        if expr[i].isdigit() or expr[i] == '.':
            num = ""
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                num += expr[i]
                i += 1
            nums.append(float(num))
            continue

        elif expr[i] == '(':
            ops.append(expr[i])

        elif expr[i] == ')':
            while ops and ops[-1] != '(':
                apply_op()
            ops.pop()

        else:
            # special case for power right associativity
            while (ops and ops[-1] != '(' and
                   ((expr[i] != '^' and precedence(ops[-1]) >= precedence(expr[i])) or
                    (expr[i] == '^' and precedence(ops[-1]) > precedence(expr[i])))):
                apply_op()

            ops.append(expr[i])

        i += 1

    while ops:
        apply_op()

    return nums[0]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def compute():
    data = request.get_json()
    expression = data["expression"]

    try:
        result = evaluate(expression)
    except Exception:
        return jsonify({"result": "Error", "error": True})

    return jsonify({"result": result, "error": False})


if __name__ == "__main__":
    app.run(debug=True)
