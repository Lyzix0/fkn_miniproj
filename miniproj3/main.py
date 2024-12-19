def evaluate_expression(expr):
    ops = {"плюс": "+", "минус": "-", "умножить на": "*", "поделить на": "/"}

    nums = {
        "ноль": 0,
        # 1
        "один": 1,
        "одного": 1,
        "одному": 1,
        "одним": 1,
        "одном": 1,
        "одна": 1,
        "одной": 1,
        "одну": 1,
        "одною": 1,
        "одно": 1,
        # 2
        "два": 2,
        "двух": 2,
        "двум": 2,
        "двумя": 2,
        "двое": 2,
        "двоих": 2,
        "двоим": 2,
        "двоими": 2,
        # 3
        "три": 3,
        "трёх": 3,
        "трех": 3,
        "трем": 3,
        "трём": 3,
        "тремя": 3,
        "трое": 3,
        "троих": 3,
        "троим": 3,
        "троими": 3,
        # 4
        "четыре": 4,
        "четырех": 4,
        "четырёх": 4,
        "четырем": 4,
        "четырём": 4,
        "четырьмя": 4,
        "четверо": 4,
        "четверых": 4,
        "четверым": 4,
        "четверыми": 4,
        # 5-19
        "пять": 5,
        "шесть": 6,
        "семь": 7,
        "восемь": 8,
        "девять": 9,
        "десять": 10,
        "одиннадцать": 11,
        "двенадцать": 12,
        "тринадцать": 13,
        "четырнадцать": 14,
        "пятнадцать": 15,
        "шестнадцать": 16,
        "семнадцать": 17,
        "восемнадцать": 18,
        "девятнадцать": 19,
        # десятки
        "двадцать": 20,
        "тридцать": 30,
        "сорок": 40,
        "пятьдесят": 50,
        "шестьдесят": 60,
        "семьдесят": 70,
        "восемьдесят": 80,
        "девяносто": 90,
        # сотни
        "сто": 100,
        "двести": 200,
        "триста": 300,
        "четыреста": 400,
        "пятьсот": 500,
        "шестьсот": 600,
        "семьсот": 700,
        "восемьсот": 800,
        "девятьсот": 900,
        # тысяча в разных падежах
        "тысяча": 1000,
        "тысячи": 1000,
        "тысяч": 1000,
        "тысяче": 1000,
        "тысячей": 1000,
    }

    def words_to_number(words):
        total = 0
        current = 0
        for word in words:
            if word in nums:
                value = nums[word]
                if value >= 1000:
                    if current == 0:
                        current = 1
                    total += current * value
                    current = 0
                elif value >= 100:
                    if current == 0:
                        current = 1
                    current *= value
                else:
                    current += value

        return total + current

    def tokenize(expression):
        raw_tokens = expression.split()
        tokens = []

        i = 0
        while i < len(raw_tokens):
            if (
                raw_tokens[i] == "умножить"
                and i + 1 < len(raw_tokens)
                and raw_tokens[i + 1] == "на"
            ):
                tokens.append("умножить на")
                i += 2
            elif (
                raw_tokens[i] == "поделить"
                and i + 1 < len(raw_tokens)
                and raw_tokens[i + 1] == "на"
            ):
                tokens.append("поделить на")
                i += 2
            else:
                tokens.append(raw_tokens[i])
                i += 1

        return tokens

    def combine_number_words(tokens):
        combined = []
        number_buffer = []

        def flush_number_buffer():
            if number_buffer:
                num = words_to_number(number_buffer)
                combined.append(num)
                number_buffer.clear()

        for token in tokens:
            if token in nums:
                number_buffer.append(token)
            else:
                flush_number_buffer()
                combined.append(token)

        flush_number_buffer()
        return combined

    def parse(tokens):
        precedence = {"+": 1, "-": 1, "*": 2, "/": 2}
        output = []
        operators = []

        for token in tokens:
            if isinstance(token, int):
                output.append(token)
            elif token in ["+", "-", "*", "/"]:
                while (
                    operators
                    and operators[-1] != "("
                    and precedence[operators[-1]] >= precedence[token]
                ):
                    output.append(operators.pop())
                operators.append(token)
            elif token == "(":
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(":
                    output.append(operators.pop())
                operators.pop()
            else:
                raise ValueError("Неизвестный токен: " + str(token))

        while operators:
            output.append(operators.pop())

        return output

    def evaluate_rpn(rpn):
        stack = []
        for token in rpn:
            if token in ["+", "-", "*", "/"]:
                b = stack.pop()
                a = stack.pop()

                if token == "+":
                    stack.append(a + b)
                elif token == "-":
                    stack.append(a - b)
                elif token == "*":
                    stack.append(a * b)
                elif token == "/":
                    if b == 0:
                        raise ZeroDivisionError("Деление на ноль!")

                    stack.append(a / b)
            else:
                stack.append(token)

        return stack[0]

    try:
        tokens = tokenize(expr)

        tokens = [ops.get(token, token) for token in tokens]
        tokens = combine_number_words(tokens)

        i = 0
        while i < len(tokens):
            if tokens[i] == "-":
                if i == 0 or tokens[i - 1] in ["+", "-", "*", "/", "("]:
                    tokens.insert(i, 0)
                    i += 1
            i += 1

        rpn = parse(tokens)
        result = evaluate_rpn(rpn)
        return float(result)

    except ZeroDivisionError:
        return "Деление на ноль!"
    except Exception as e:
        return f"Ошибка в выражении: {e}"


examples = [
    ("тридцать три поделить на три", 11),
    ("два плюс два плюс два", 6),
    ("минус два умножить на двадцать", -40),
    ("пятьдесят поделить на ноль", "Деление на ноль!"),
    ("десять минус два плюс один", 9),
    ("девяносто один плюс пять", 96),
    ("сто двадцать три плюс четыреста пятьдесят шесть", 579),
    ("тысяча двести тридцать четыре минус восемьсот девяносто семь", 337),
    ("сто тысяч плюс двадцать один", 100021),
]

for ex, expected in examples:
    res = evaluate_expression(ex)
    print(f"{res}, ожидается: {expected}")
