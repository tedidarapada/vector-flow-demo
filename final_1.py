import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define the vector field functions
def vector_field_0(x, y):
    return 1, 0

def vector_field_o(x, y):
    return x, 0

def vector_field_1(x, y):
    return x, 1

def vector_field_2(x, y):
    return x, y

def vector_field_3(x, y):
    return -y, x

def vector_field_4(x, y):
    return 1, np.sin(x)

def vector_field_5(x, y):
    denom = x**2 + y**2
    return -y / denom, x / denom

def vector_field_6(x, y):
    return x, -y

# List of vector fields with their mathematical notations
vector_fields = [
    (vector_field_0, r"$\vec{F}<x, y> = <1, 0>$"),
    (vector_field_o, r"$\vec{F}<x, y> = <x, 0>$"),
    (vector_field_1, r"$\vec{F}<x, y> = <x, 1>$"),
    (vector_field_2, r"$\vec{F}<x, y> = <x, y>$"),
    (vector_field_3, r"$\vec{F}<x, y> = <-y, x>$"),
    (vector_field_4, r"$\vec{F}<x, y> = <1, \sin(x)>$"),
    (vector_field_5, r"$\vec{F}<x, y> = \left<\frac{-y}{x^2 + y^2}, \frac{x}{x^2 + y^2}\right>$"),
    (vector_field_6, r"$\vec{F}<x, y> = <x, -y>$"),
]

# Plot the vector field
def plot_vector_field(ax, field_function, x_range, y_range):
    X, Y = np.meshgrid(np.linspace(*x_range, 20), np.linspace(*y_range, 20))
    U, V = field_function(X, Y)
    ax.quiver(X, Y, U, V, color='blue')

# Animate a warping square along the vector field
def animate_warping_square(ax, field_function, x_range, y_range):
    # Initialize the square corners and interaction variables
    square_corners = None
    dragging = False
    start_point = None
    square_edges = None
    square_polygon, = ax.plot([], [], color='red', lw=2)

    # Handle mouse press to start drawing the rectangle
    def on_press(event):
        try:
            nonlocal square_corners, square_edges, dragging, start_point
            if event.inaxes != ax:
                return
            dragging = True
            start_point = np.array([event.xdata, event.ydata])
            square_corners = np.array([
                [start_point[0], start_point[1]], 
                [start_point[0], start_point[1]], 
                [start_point[0], start_point[1]], 
                [start_point[0], start_point[1]]
            ])
            square_edges = [square_corners]  # Store the edges
        except:
            None

    # Handle mouse motion to resize the rectangle while dragging
    def on_motion(event):
        try:
            nonlocal square_corners, square_edges
            if not dragging or start_point is None or event.inaxes != ax:
                return
            end_point = np.array([event.xdata, event.ydata])
            square_corners = np.array([
                [start_point[0], start_point[1]], 
                [end_point[0], start_point[1]], 
                [end_point[0], end_point[1]], 
                [start_point[0], end_point[1]]
            ])
            # Update the edges (interpolating between corners)
            square_edges = [
                np.array([np.linspace(square_corners[i][0], square_corners[(i+1) % 4][0], 10),
                        np.linspace(square_corners[i][1], square_corners[(i+1) % 4][1], 10)])
                for i in range(4)
            ]
            # Update the polygon in real time
            update_polygon()
        except:
            None

    # Handle mouse release to finalize the rectangle
    def on_release(event):
        try:
            nonlocal dragging
            dragging = False
        except:
            None

    fig = plt.gcf()
    fig.canvas.mpl_connect('button_press_event', on_press)
    fig.canvas.mpl_connect('motion_notify_event', on_motion)
    fig.canvas.mpl_connect('button_release_event', on_release)

    # Update the polygon with the new edge data
    def update_polygon():
        all_points = np.concatenate([edge.T for edge in square_edges])
        # Use ax.fill to fill the polygon with red color
        ax.fill(all_points[:, 0], all_points[:, 1], color='red', alpha=0.5)  # alpha is for transparency
        square_polygon.set_data(
            np.append(all_points[:, 0], all_points[0, 0]),
            np.append(all_points[:, 1], all_points[0, 1])
        )
    # Animation update function
    def update(frame):
        try:
            nonlocal square_corners, square_edges
            if square_corners is None or dragging:
                return square_polygon,

            # Update all points along the edges based on the vector field
            new_edges = []
            for edge in square_edges:
                new_edge = []
                for i in range(edge.shape[1]):
                    point = edge[:, i]
                    U, V = field_function(point[0], point[1])
                    direction = np.array([U, V])
                    new_edge.append(point + direction * 0.05)  # Adjust step size
                new_edges.append(np.array(new_edge).T)

            square_edges = new_edges
            update_polygon()
            return square_polygon,
        except:
            None
    try:
        ani = FuncAnimation(
            plt.gcf(), update, frames=200, interval=20, blit=True  # Faster frame rate for smoother animation
        )
        return ani
    except:
        None


# Main program
def main():
    while True:
        print("Select a vector field:")
        print("1.<1,0>")
        print("2.<x,0>")
        print("3.<x,1>")
        print("4.<x,y>")
        print("5.<-y,x>")
        print("6.<1, sin(x)>")
        print("7.<-y/(x^2+y^2),x/(x^2+y^2)>")
        print("8.<x,-y>")
        print("9. Exit")

        choice = int(input("Enter the number of the vector field to visualize: "))

        if choice == 9:
            print("Exiting program.")
            break

        if choice < 1 or choice > len(vector_fields):
            print("Invalid choice.")
            continue

        selected_field, selected_name = vector_fields[choice - 1]

        # Set up the plot
        fig, ax = plt.subplots()
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_aspect('equal')
        ax.set_title(selected_name)

        # Plot the vector field
        plot_vector_field(ax, selected_field, (-5, 5), (-5, 5))

        # Animate the warping square
        ani = animate_warping_square(ax, selected_field, (-5, 5), (-5, 5))

        plt.show()

if __name__ == "__main__":
    main()