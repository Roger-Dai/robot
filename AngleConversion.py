import math

def rad_to_deg_list(rads):
    degrees = []
    for i in rads:
        i = float(i)
        deg = i * (180 / math.pi)
        degrees.append(deg)
    return degrees

def deg_to_rad_list(degs):
    rads = []
    for i in degs:
        i = float(i)
        rad = i * (math.pi / 180)
        rads.append(rad)
    return rads

if __name__ == "__main__":
    x = input("Enter: ")
    joints = x.split(", ")
    print(deg_to_rad_list(joints))

    