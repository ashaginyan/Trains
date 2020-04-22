import cv2
from sympy.solvers import solve
from sympy import Symbol
from sympy.core.numbers import Float

# For image with shape (1920x1080)

def get_k_b(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    k = (y1 - y2) / (x1 - x2)
    b = y1 - k * x1
    return round(k, 2), round(b)

def get_dist(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    r = ((x2-x1)**2+(y2-y1)**2)**0.5
    return round(r)

class Sector():
    def __init__(self, sec_num):
        self.sec_num = sec_num
        if sec_num == 1:
            self.r = 60 # пиксели
            self.A = [(134, 206), (77, 407), (15, 614), (0, 894)]
            self.B = [(1062, 184), (938, 382), (967, 581), (959, 856)]
            self.C = [(1919, 162), (1919, 357), (1919, 548), (1919, 819)]
            self.L = [30, 31, 32, 33] # метры

        elif sec_num == 2:
            self.r = 100
            self.A = [(0, 435), (260, 1079), (620, 1079), (1163, 1079), (1508, 1079), (1836, 1079)]
            self.B = [(44, 218), (203, 540), (657, 540), (1153, 540), (1471, 540), (1773, 540)]
            self.C = [(87, 0), (386, 0), (693, 0), (1142, 0), (1433, 0), (1710, 0)]
            self.L = [10, 20, 20, 20, 20, 20]

        elif sec_num == 3:
            self.r = 120
            self.C = [(0, 849), (0, 587), (0, 393), (0, 216)]
            self.B = [(921, 873), (887, 610), (856, 411), (831, 231)]
            self.A = [(1842, 897), (1773, 632), (1712, 429), (1661, 245)]
            self.L = [43, 42, 40, 39]

        elif sec_num == 4:
            pass
        elif sec_num == 5:
            pass
        elif sec_num == 6:
            pass
        elif sec_num == 7:
            pass
        elif sec_num == 8:
            self.r = 60
            self.A = [(0, 318), (0, 525), (0, 764), (88, 1078), (392, 1078), (696, 1078), (1115, 1078), (1387, 1078),
                      (1662, 1078), (1918, 1007), (1918, 702), (1918, 478)]
            self.B = [(194, 140), (290, 216), (355, 262), (504, 315), (650, 326), (818, 333), (1045, 333), (1226, 333),
                      (1365, 326), (1507, 315), (1522, 281), (1682, 143)]
            self.C = [(349, 5), (474, 0), (562, 0), (672, 0), (765, 0), (870, 0), (1013, 0), (1106, 0), (1202, 0),
                      (1301, 0), (1386, 0), (1470, 0)]
            self.L = [70, 80, 98, 114, 114, 114, 114, 114, 114, 98, 86, 76]

        elif sec_num == 9:
            pass
        elif sec_num == 10:
            pass
        elif sec_num == 11:
            pass
        elif sec_num == 12:
            pass
        self.railroad_range = range(len(self.L))

        self.set_M()
        self.set_W()
        self.set_k_b()

    def set_M(self):
        # Расстояния от А до середины видимого отрезка пути в пикселях (АВ)
        M = []
        for i in self.railroad_range:
            M.append(get_dist(self.A[i], self.B[i]))
        self.M = M

    def set_W(self):
        W = []
        for i in self.railroad_range:
            W.append(get_dist(self.A[i], self.C[i]))
        self.W = W

    def set_k_b(self):
        k = []
        b = []
        # Рассчитываем угловой коэффициент и b для каждой прямой
        for i in self.railroad_range:
            k_, b_ = get_k_b(self.A[i], self.C[i])
            k.append(k_)
            b.append(b_)
        self.k = k
        self.b = b

    def get_K(self, x, N):
        n = N
        K = (self.W[n] - self.M[n]) / self.M[n]
        return K

    def get_D(self, x, N):
        n = N
        K = (self.W[n] - self.M[n]) / self.M[n]
        D = self.L[n] * K / ((self.W[n] / x) - 1 + K)
        return round(D)

    def get_x(self, D, N):
        n = N
        K = (self.W[n] - self.M[n]) / self.M[n]
        x = self.W[n] / (self.L[n] * K / (D) + 1 - K)
        return round(x)

    def check(self, point):
        way = [-1]
        for i in self.railroad_range:
            x = Symbol('x')
            solution = solve(self.r**2 - (x - point[0])**2 - (self.k[i]*x + self.b[i] - point[1])**2, x)
            if type(solution[0]) == Float:
                way.remove(-1)
                way.append(i)
        return way


def main():
    sector = Sector(1)
    print(sector.check((429, 756)))

main()