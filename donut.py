import math
import time
import os
import sys

# Screen size
screen_width = 120
screen_height = 36

# Initialize rotation angles
A = 0  # Rotation angle around the X-axis
B = 0  # Rotation angle around the Z-axis

# Characters for luminance mapping
luminance_chars = '.,-~:;=!*#$@'

# Precompute screen center
half_screen_width = screen_width // 2
half_screen_height = screen_height // 2

# Constants for scaling
K1 = 50  # Adjust this value to scale the donut horizontally
K2 = 20  # Adjust this value to scale the donut vertically
K2_inverse = 1 / K2

while True:
    # Initialize buffers
    output = [' '] * (screen_width * screen_height)
    zbuffer = [0] * (screen_width * screen_height)

    j = 0
    while j < 2 * math.pi:
        i = 0
        while i < 2 * math.pi:
            # Sines and cosines of the angles
            sin_i = math.sin(i)
            cos_i = math.cos(i)
            sin_j = math.sin(j)
            cos_j = math.cos(j)
            sin_A = math.sin(A)
            cos_A = math.cos(A)
            sin_B = math.sin(B)
            cos_B = math.cos(B)

            # Coordinates of the point on the torus in 3D space
            circle_x = cos_j + 2  # Torus circle radius (R1 + R2 * cos(v))
            circle_y = sin_j

            # Calculate the 3D coordinates after rotation
            x = circle_x * (cos_B * cos_i + sin_A * sin_B * sin_i) - circle_y * cos_A * sin_B
            y = circle_x * (cos_i * sin_B - sin_A * cos_B * sin_i) + circle_y * cos_A * cos_B
            z = cos_A * circle_x * sin_i + circle_y * sin_A + 5  # +5 to prevent division by zero

            # Inverse of z for perspective projection
            ooz = 1 / z

            # Projected 2D coordinates
            xp = int(half_screen_width + K1 * ooz * x)
            yp = int(half_screen_height - K2 * ooz * y)  # Minus sign for proper orientation

            # Calculate luminance
            L = cos_i * cos_j * sin_B - cos_A * cos_j * sin_i - sin_A * sin_j + cos_B * (cos_A * sin_j - cos_j * sin_A * sin_i)
            luminance_index = int(L * 8)
            if luminance_index < 0:
                luminance_index = 0
            if luminance_index > len(luminance_chars) - 1:
                luminance_index = len(luminance_chars) - 1

            # Index in buffers
            idx = xp + screen_width * yp
            if 0 <= xp < screen_width and 0 <= yp < screen_height:
                if ooz > zbuffer[idx]:
                    zbuffer[idx] = ooz
                    output[idx] = luminance_chars[luminance_index]
            i += 0.07
        j += 0.07

    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')

    # Print the frame
    for y in range(screen_height):
        for x in range(screen_width):
            sys.stdout.write(output[x + screen_width * y])
        sys.stdout.write('\n')
    sys.stdout.flush()

    # Increment rotation angles
    A += 0.1
    B += 0.04

    # Control the frame rate
    time.sleep(0.005)
