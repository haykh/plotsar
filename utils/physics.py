import math


def ComputeBsurf(pulsar):
    I0 = 1e45
    radius = 1000000
    c = 29970254700
    return (1.5 * I0 * c**3 * pulsar["P0"] * pulsar["P1"]) ** (0.5) / (
        2 * math.pi * radius**3
    )


def ComputeRLC(pulsar):
    c = 29970254700
    return (c * pulsar["P0"] / (2 * math.pi)) / 1e5


def ComputeBLC(pulsar):
    radius = 10
    return ComputeBsurf(pulsar) * (ComputeRLC(pulsar) / radius) ** -3


def ComputeGmax(pulsar):
    radius = 10
    return (
        2799248.72930016
        * ComputeBsurf(pulsar)
        * pulsar["P0"]
        * (radius / ComputeRLC(pulsar)) ** 3
    )

def ComputeGammaradLC(pulsar):
    return 1e5 * (ComputeBLC(pulsar) / 1e5)**(-0.5)