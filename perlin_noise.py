import random
import math
from PIL import Image

# Linear interpolation function for bilinear interpolation
def lerp(start, end, amount):
    return (1 - amount) * start + amount * end

# Dot product function
def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

# Ease curve / S curve function
def fade(t):
    return 3 * pow(t, 2) - 2 * pow(t, 3)

# Perlin noise function with x/y coordinate and resolution as input
def perlin(x, y, res):
    x = x/res
    y = y/res

    # The grid corners surrounding the chosen decimal point
    x0 = math.floor(x) # Left
    x1 = x0 + 1 # Right
    y0 = math.floor(y) # Top
    y1 = y0 + 1 # Bottom

    #print("Point: " + str((x, y)), "Corners:", (x0, y0), (x1, y0), (x1, y1), (x0, y1))

    # Pseudorandom gradient vectors for each grid point, making the seed dependent on both x and y coordinates
    random.seed(y0 + x0 * res)
    g0 = random.choice([(1, 1), (1, -1), (-1, 1), (-1, -1)]) # Top Left
    random.seed(y0 + x1 * res)
    g1 = random.choice([(1, 1), (1, -1), (-1, 1), (-1, -1)]) # Top Right
    random.seed(y1 + x1 * res)
    g2 = random.choice([(1, 1), (1, -1), (-1, 1), (-1, -1)]) # Bottom Right
    random.seed(y1 + x0 * res)
    g3 = random.choice([(1, 1), (1, -1), (-1, 1), (-1, -1)]) # Bottom Left

    #print("Gradient Vectors:" + str(g0), str(g1), str(g2), str(g3))

    d0 = (x - x0, y - y0) # Top Left
    d1 = (x - x1, y - y0) # Top Right
    d2 = (x - x1, y - y1) # Bottom Right
    d3 = (x - x0, y - y1) # Bottom Left

    #print("Distance Vectors:" + str(d0) + str(d1) + str(d2) + str(d3))

    dot0 = dot(g0, d0) # Top Left
    dot1 = dot(g1, d1) # Top Right
    dot2 = dot(g2, d2) # Bottom Right
    dot3 = dot(g3, d3) # Bottom Left

    #print("Dot Products: " + str(dot0) + " " + str(dot1) + " " + str(dot2) + " " + str(dot3))

    # Using s-curve output for the linear interpolation amount, to exaggerate values
    value1 = lerp(dot0, dot1, fade(x - x0))
    value2 = lerp(dot3, dot2, fade(x - x0))
    value = lerp(value1, value2, fade(y - y0))

    #print(value)
    
    return value

xpoints, ypoints = 8, 8 # Dimensions of grid
res = 32 # number of points within each grid square in each dimension

# Creation of image to represent the noise
image = Image.new('RGB', (xpoints * res, ypoints * res))
pixels = image.load()

# Looping through a grid and assigning perlin noise value to each pixel
for x in range(xpoints * res):
    for y in range(ypoints * res):
        intensity = round((perlin(x, y, res) + 1) * 127.5)
        # if intensity > 114 and intensity < 156:
        #     pixels[x, y] = (0, 0, 0)
        # else:
        #     pixels[x, y] = (255, 255, 255)
        pixels[x, y] = (intensity, intensity, intensity)

image.show()