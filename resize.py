import math
import matplotlib.pyplot as plt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Original square
p1 = Point(3, 3)
p2 = Point(1, 3)
p3 = Point(1, 1)
p4 = Point(3, 1)
points = [p1, p2, p3, p4]

# Scale factor
ds = 2

print(f"Original points:")
for p in points:
    print(f"  ({p.x}, {p.y})")


# Calculate the object's center (centroid)
def calculate_center(points):
    """Calculate the center (centroid) of a set of points"""
    total_x = 0
    total_y = 0
    for p in points:
        total_x += p.x
        total_y += p.y
    center_x = total_x / len(points)
    center_y = total_y / len(points)
    return Point(center_x, center_y)


# Get the object's center
object_center = calculate_center(points)
center_x = object_center.x
center_y = object_center.y

print(f"\nObject Center: ({center_x:.2f}, {center_y:.2f})")
print(f"Scale factor: {ds}")

# Create a copy of original points for display
original_points = [Point(p.x, p.y) for p in points]

# Scale each point around the object's center
for p in points:
    # Calculate vector from center to point
    vector_x = p.x - center_x
    vector_y = p.y - center_y

    # Scale the vector
    vector_x *= ds
    vector_y *= ds

    # Calculate new position
    p.x = center_x + vector_x
    p.y = center_y + vector_y

print(f"\nScaled points:")
for p in points:
    print(f"  ({p.x:.2f}, {p.y:.2f})")

# Prepare for plotting
plt.figure(figsize=(8, 6))

# Plot center point
plt.plot(center_x, center_y, 'rx', markersize=12, markeredgewidth=2, label='Object Center')

# Plot original and scaled shapes
for shape_points, color, label in [
    (original_points, 'blue', 'Original'),
    (points, 'red', 'Scaled')
]:
    x_arr = []
    y_arr = []
    for p in shape_points:
        x_arr.append(p.x)
        y_arr.append(p.y)
    # Close the loop
    x_arr.append(shape_points[0].x)
    y_arr.append(shape_points[0].y)
    plt.plot(x_arr, y_arr, color=color, marker='o', label=label)

plt.axis('equal')
plt.grid(True, alpha=0.3)
plt.xlabel('X')
plt.ylabel('Y')
plt.title(f'Scaling around Object Center ({center_x:.2f}, {center_y:.2f})')
plt.legend()
plt.show()