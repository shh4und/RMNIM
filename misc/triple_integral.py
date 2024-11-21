import numpy as np

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Space:
    def __init__(self, r1, r2, t1, t2, p1, p2):
        self.r1 = r1
        self.r2 = r2
        self.t1 = t1
        self.t2 = t2
        self.p1 = p1
        self.p2 = p2

class Resolution:
    def __init__(self, nr, nt, np):
        self.nr = nr
        self.nt = nt
        self.np = np

class Domain:
    def __init__(self, space, res):
        self.num_points = res.nr * res.nt * res.np
        self.dr = self.delta(space.r1, space.r2, res.nr)
        self.dt = self.delta(space.t1, space.t2, res.nt)
        self.dp = self.delta(space.p1, space.p2, res.np)
        
        rr = self.interval(space.r1, self.dr, res.nr)
        tt = self.interval(space.t1, self.dt, res.nt)
        pp = self.interval(space.p1, self.dp, res.np)
        
        self.points = [Point(r, t, p) for r in rr for t in tt for p in pp]

    def delta(self, a, b, n):
        return (b - a) / n

    def interval(self, a, d, n):
        return [a + d * i for i in range(n)]

def get_volume(domain, p):
    return p.x * p.x * np.sin(p.z) * domain.dr * domain.dt * domain.dp

def integrate(domain, predicate, function):
    sum = 0
    for p in domain.points:
        if predicate(p):
            sum += function(p) * get_volume(domain, p)
    return sum

def predicate(p):
    return True  # Integrate over all points

def function(p):
    return 1

def main():
    space = Space(0, 1, 0, 3 * np.pi / 2, 0, np.pi/6)
    res = Resolution(100, 200, 200)

    domain = Domain(space, res)

    volume = integrate(domain, predicate, function)
    print(f"Calculated volume: {volume}")

if __name__ == "__main__":
    main()