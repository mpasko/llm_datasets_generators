from sampler.sampler_algorithm import Sampler

index_range=100
sparcity_range=10

def formatter(indexes):
    mode = indexes[3]
    a=indexes[2]+1
    zero = index_range*sparcity_range
    if mode == 0:
        return solution_exists(indexes[0]-zero, indexes[1], a)
    elif mode == 1:
        return above(indexes[0]-zero, indexes[1], a)
    else:
        return above(indexes[0]-zero, -indexes[1], -a)
    
def solution_exists(n1, n2, a):
    x1 = n1
    x2 = n1 + n2
    b = -a * x1 - a * x2
    c = a*x1*x2
    equation = format_equation(a, b, c)
    return "<<start>>{equation} => x in [{x1}, {x2}]<<stop>>".format(equation=equation, x1=x1, x2=x2)

def above(p, q, a):
    b = -2 * a * p
    c = q + a * p*p
    equation = format_equation(a, b, c)
    return "<<start>>{equation} => x in empty<<stop>>".format(equation=equation)

def format_equation(a, b, c):
    def part(n):
        return "+ {n}".format(n=n) if n >= 0 else "- {n}".format(n=-n)
    b_part = part(b)
    c_part = part(c)
    return "{a}x^2 {b_part}x {c_part} = 0".format(a=a, b_part=part(b), c_part=part(c))

def generate():
    dimensions = [index_range*2, index_range*2, index_range // 10, 3]
    sparcity = [sparcity_range, sparcity_range, sparcity_range, 1]
    sampler = Sampler(formatter, dimensions, sparcity)
    sampler.sample()

generate()
