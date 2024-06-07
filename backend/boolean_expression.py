class BooleanExpression:
    """
    Represents a Boolean expression.

    first: ExtendedBool
    second (optional): ExtendedBool
    operator (optional): String
    """
    def __init__(self, first=None, operator=None, second=None, value=None):
        self.operator = operator
        self.first = first
        self.second = second
        self.evaluate(value)


    def get_value(self, value=None):
        if value is not None:
            return value
        
        if self.first is None and self.second is None:
            return value

        if self.operator == "AND" and self.first.value and self.second.value:
            return True
        if self.operator == "OR" and (self.first.value or self.second.value):
            return True
        if self.operator == "NOT":
            return not self.first.value

    def evaluate(self, value=None):
        self.value = self.get_value(value)

    def __and__(self, other):
        return BooleanExpression(first=self, second=other, operator="AND", value=(self.value & other.value))

    def __or__(self, other):
        return BooleanExpression(first=self, second=other, operator="OR", value=(self.value | other.value))

    def __invert__(self):
        value = not self.value
        return BooleanExpression(first=self, operator="NOT", value=value)

    def __bool__(self):
        return bool(self.evaluate())
    
    def __repr__(self):
        return f"ExtendedBool({self.first=}, {self.second=}, {self.value=}, {self.operator=})"


a = BooleanExpression(value=False)
b = BooleanExpression(value=True)
c = BooleanExpression(value=False)
d = a | b
e = d & c
f = BooleanExpression(a | b) & c



print(f"{a.value=}")
print(f"{b.value=}")
print(f"{c.value=}")
print(f"{d.value=}")
print(f"{e.value=}")

