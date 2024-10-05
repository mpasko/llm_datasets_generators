from sampler.sampler_algorithm import Sampler

def formatter(indexes):
    a = indexes[0]
    b = indexes[1]
    c = a+b
    return "<<start>>"+str(a) + " + " + str(b) + " = " + str(c)+"<<stop>>"

def generate():
    dimensions = [1000, 1000]
    sparcity = [1000, 1000]
    sampler = Sampler(formatter, dimensions, sparcity)
    sampler.sample()

generate()
