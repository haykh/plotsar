import math

def ComputeBsurf(pulsar):
    I0 = 1e45
    radius = 1000000
    c = 29970254700
    return (1.5 * I0 * c**3 * pulsar["P0"] * pulsar["P1"])**(0.5) / (2 * math.pi * radius**3)

def ComputeRLC(pulsar):
    c = 29970254700
    return (c * pulsar["P0"] / (2 * math.pi)) / 1e5