from core.auto_programmer import AutoProgrammer

agent = AutoProgrammer()

ok, output = agent.build(

    "AI_TEST/calculator.py",

    """
Create a python calculator.

Take two numbers.

Print addition,
subtraction,
multiplication,
division.

Use proper Python.

"""
)

print(ok)

print(output)