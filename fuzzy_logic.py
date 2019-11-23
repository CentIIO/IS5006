#fuzzy logic needs to be improved



# membership functions
def up(a, b, x):
    a = float(a)
    b = float(b)
    x = float(x)
    if x < a:
        return 0.0
    if x < b:
        return (x - a) / (b - a)
    return 1.0

def down(a, b, x):
    return 1. - up(a, b, x)

def tri(a, b, x):
    a = float(a)
    b = float(b)
    m = (a + b) / 2.
    first = (x - a) / (m - a)
    second = (b - x) / (b - m)
    return max(min(first, second), 0.)
