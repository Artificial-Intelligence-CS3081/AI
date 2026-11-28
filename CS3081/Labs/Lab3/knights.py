"""Lab 3 - Knights and Knaves (Puzzles 0-2)."""
from logic import And, Or, Not, Symbol, Implication, Biconditional, model_check


def person_rules(name):
    knight = Symbol(f"{name}Knight")
    knave = Symbol(f"{name}Knave")
    return knight, knave, Or(knight, knave), Not(And(knight, knave))


def says(knight, knave, statement):
    return And(Implication(knight, statement), Implication(knave, Not(statement)))


def show(puzzle, kb, people):
    print(f"Puzzle {puzzle}:")
    for name, knight, knave in people:
        if model_check(kb, knight):
            result = "Knight"
        elif model_check(kb, knave):
            result = "Knave"
        else:
            result = "Unknown"
        print(f"  {name} is a {result}")


# Puzzle 0: A says "I am both a knight and a knave."
a_k, a_v, a_one, a_not_both = person_rules("A")
kb0 = And(a_one, a_not_both, says(a_k, a_v, And(a_k, a_v)))
show(0, kb0, [("A", a_k, a_v)])

# Puzzle 1: A says "We are both knaves." B says nothing.
b_k, b_v, b_one, b_not_both = person_rules("B")
kb1 = And(a_one, a_not_both, b_one, b_not_both,
          says(a_k, a_v, And(a_v, b_v)))
show(1, kb1, [("A", a_k, a_v), ("B", b_k, b_v)])

# Puzzle 2: A says "We are the same kind."
# B says "We are of different kinds."
same_kind = Biconditional(a_k, b_k)
kb2 = And(a_one, a_not_both, b_one, b_not_both,
          says(a_k, a_v, same_kind),
          says(b_k, b_v, Not(same_kind)))
show(2, kb2, [("A", a_k, a_v), ("B", b_k, b_v)])
