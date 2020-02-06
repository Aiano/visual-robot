from math import *

PI = 3.14159
l1 = 10
l2 = 3
l3 = 15
l4 = 15
l5 = 5

if __name__ == '__main__':
    x = float(input("x:"))
    y = float(input("y:"))
    z = float(input("z:"))

    d1 = sqrt(pow(x, 2) + pow(y, 2))
    d2 = d1 - l2
    d3 = sqrt(pow(l1, 2) + pow(d2, 2))
    b1 = atan(l1 / d2) / PI * 180
    b2 = 90 - b1
    d4 = z + l5
    d5 = sqrt(pow(d3, 2) + pow(d4, 2) - 2 * d3 * d4 * cos(b2 / 180 * PI))

    a1 = (atan(d2 / l1) / PI * 180) + (acos((pow(d3, 2) + pow(d5, 2) - pow(d4, 2)) / (2 * d3 * d5)) / PI * 180) + (
            acos((pow(d5, 2) + pow(l3, 2) - pow(l4, 2)) / (2 * d5 * l3)) / PI * 180) - 90
    a2 = 180 - (acos((pow(l3, 2) + pow(l4, 2) - pow(d5, 2)) / (2 * l3 * l4)) / PI * 180)
    a3 = 180 - ((acos((pow(d4, 2) + pow(d5, 2) - pow(d3, 2)) / (2 * d4 * d5)) / PI * 180) +
                (acos((pow(l4, 2) + pow(d5, 2) - pow(l3, 2)) / (2 * l4 * d5)) / PI * 180))
    a4 = atan(x / y) / PI * 180

    print("a1:%f" % a1)
    print("a2:%f" % a2)
    print("a3:%f" % a3)
    print("a4:%f" % a4)
