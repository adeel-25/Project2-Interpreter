# Project 2 - Simple Interpreter

class SimpleInterpreter:

    def __init__(self, program):
        self.program = program
        self.pos = 0
        self.variables = {}
        self.let_variables = set()
        self.order = []

    def current(self):
        if self.pos >= len(self.program):
            return ""
        return self.program[self.pos]

    def skip_spaces(self):
        while self.current() != "" and self.current().isspace():
            self.pos += 1

    def error(self, message="error"):
        raise Exception(message)

    def read_identifier(self):
        self.skip_spaces()

        if not (self.current().isalpha() or self.current() == "_"):
            self.error()

        start = self.pos

        while self.current().isalnum() or self.current() == "_":
            self.pos += 1

        return self.program[start:self.pos]

    def read_number(self):
        self.skip_spaces()

        if not self.current().isdigit():
            self.error()

        start = self.pos

        while self.current().isdigit():
            self.pos += 1

        number = self.program[start:self.pos]

        if len(number) > 1 and number[0] == "0":
            self.error()

        return int(number)

    def factor(self, in_let):
        self.skip_spaces()
        ch = self.current()

        if ch == "(":
            self.pos += 1
            value = self.expression(in_let)
            self.skip_spaces()

            if self.current() != ")":
                self.error()

            self.pos += 1
            return value

        elif ch == "-":
            self.pos += 1
            return -self.factor(in_let)

        elif ch == "+":
            self.pos += 1
            return self.factor(in_let)

        elif ch.isdigit():
            return self.read_number()

        elif ch.isalpha() or ch == "_":
            name = self.read_identifier()

            if name not in self.variables:
                self.error("error, uninitialized variable")

            if in_let and name not in self.let_variables:
                self.error("error, normal variables in let expression")

            return self.variables[name]

        else:
            self.error()

    def term(self, in_let):
        value = self.factor(in_let)

        while True:
            self.skip_spaces()

            if self.current() == "*":
                self.pos += 1
                value = value * self.factor(in_let)
            else:
                break

        return value

    def expression(self, in_let):
        value = self.term(in_let)

        while True:
            self.skip_spaces()

            if self.current() == "+":
                self.pos += 1
                value = value + self.term(in_let)

            elif self.current() == "-":
                self.pos += 1
                value = value - self.term(in_let)

            else:
                break

        return value

    def check_let(self):
        self.skip_spaces()

        if self.program.startswith("let", self.pos):
            next_pos = self.pos + 3

            if next_pos >= len(self.program):
                return True

            next_char = self.program[next_pos]

            if not (next_char.isalnum() or next_char == "_"):
                return True

        return False

    def assignment(self):
        self.skip_spaces()

        is_let = False

        if self.check_let():
            is_let = True
            self.pos += 3

        name = self.read_identifier()

        self.skip_spaces()

        if self.current() != "=":
            self.error()

        self.pos += 1

        value = self.expression(is_let)

        self.skip_spaces()

        if self.current() != ";":
            self.error()

        self.pos += 1

        if is_let and name in self.variables:
            self.error()

        if name not in self.variables:
            self.order.append(name)

        self.variables[name] = value

        if is_let:
            self.let_variables.add(name)

    def run(self):
        self.skip_spaces()

        while self.pos < len(self.program):
            self.assignment()
            self.skip_spaces()

        for name in self.order:
            print(name, "=", self.variables[name])


def main():

    program = """
let x = 1;
y = 2;
z = ---(x+y)*(x+-y);
"""

    try:
        interpreter = SimpleInterpreter(program)
        interpreter.run()

    except Exception as e:
        print(e)

main()