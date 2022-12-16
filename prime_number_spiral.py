import tkinter as tk
import time

class Space_2D:
    def __init__(self, width = 1200, height = 1200, size_sqaure = 2, bg_color = 'white'):
        # create a window
        self.window = tk.Tk()
        self.width = width
        self.height = height
        self.size_sqaure = size_sqaure
        self.canvas = tk.Canvas(self.window, width=width, height=height, bg=bg_color)

    # create a translator from tkinter_coordinates to cartesian_coordinates
    def translate_to_cartesian(self, tk_x, tk_y):
        # center at bottom left
        return tk_x - self.width//2, self.height//2 - tk_y

    # create a translator from cartesian_coordinates to tkinter_coordinates
    def translate_to_tkinter(self, cart_x, cart_y):
        return cart_x +  self.width//2, self.height//2 - cart_y

    # draw a line from (x1, y1) to (x2, y2)
    def draw_line(self, x1, y1, x2, y2, color = 'black', width = 0.5):
        self.canvas.create_line(
            *self.translate_to_tkinter(x1, y1),
            *self.translate_to_tkinter(x2, y2),
            fill=color,
            width=width,
        )

    def draw_grid(self):
        # create a cartesian grid   
        for i in range(-self.width//2, self.height//2, self.size_sqaure):
            self.draw_line(i, -self.height//2, i, self.height//2)
            self.draw_line(-self.width//2, i, self.width//2, i)

        # add numbers to the grid
        for i in range(-self.width//2, self.height//2, 100):
            self.canvas.create_text(
                *self.translate_to_tkinter(i, 0),
                text=str(i),
                font=("Purisa", 8),
            )
            self.canvas.create_text(
                *self.translate_to_tkinter(0, i),
                text=str(i),
                font=("Purisa", 8),
            )
        
        # Reinforce the origin
        self.canvas.create_line(
            *self.translate_to_tkinter(-self.width//2, 0),
            *self.translate_to_tkinter(self.width//2, 0),
            fill="black",
            width=2,
        )
        self.canvas.create_line(
            *self.translate_to_tkinter(0, -self.height//2),
            *self.translate_to_tkinter(0, self.height//2),
            fill="black",
            width=2,
        )
            
    def draw_square(self, x, y, color = 'black', coords = True):
        self.canvas.create_rectangle(
            *self.translate_to_tkinter(x, y),
            *self.translate_to_tkinter(x + self.size_sqaure, y + self.size_sqaure),
            fill=color,
            outline='white',
            stipple="gray50"
        )
        # write the coordinates of the square
        if coords:
            self.canvas.create_text(
                *self.translate_to_tkinter(x + self.size_sqaure//2, y + self.size_sqaure//2),
                text=f"{y//self.size_sqaure}",
                font=("Purisa", 8),
                fill='white',
            )

    def run(self):
        self.canvas.pack()
        self.window.mainloop()

# run the program
if __name__ == "__main__":
    n=100_000

    space = Space_2D()
    space.draw_grid()

    # direction can be n,s,e,w
    def left_(x, y, direction):
        if direction == 'n':
            direction = 'w'
            return x-1, y, direction
        elif direction == 's':
            direction = 'e'
            return x+1, y, direction
        elif direction == 'e':
            direction = 'n'
            return x, y+1, direction
        elif direction == 'w':
            direction = 's'
            return x, y-1, direction

    def right_(x, y, direction):
        if direction == 'n':
            direction = 'e'
            return x+1, y, direction
        elif direction == 's':
            direction = 'w'
            return x-1, y, direction
        elif direction == 'e':
            direction = 's'
            return x, y-1, direction
        elif direction == 'w':
            direction = 'n'
            return x, y+1, direction

    def up_(x, y, direction):
        if direction == 'n':
            direction = 'n'
            return x, y+1, direction
        elif direction == 's':
            direction = 's'
            return x, y-1, direction
        elif direction == 'e':
            direction = 'e'
            return x+1, y, direction
        elif direction == 'w':
            direction = 'w'
            return x-1, y, direction

    def down_(x, y, direction):
        if direction == 'n':
            direction = 'n'
            return x, y-1, direction
        elif direction == 's':
            direction = 's'
            return x, y+1, direction
        elif direction == 'e':
            direction = 'e'
            return x-1, y, direction
        elif direction == 'w':
            direction = 'w'
            return x+1, y, direction

    def check_if_prime(i):
        for j in range(2, i):
            if i % j == 0:
                return False
        return True
    import pandas as pd

    final_dataframe = pd.DataFrame()
    coords = [[0,0, 's']]
    coords_only = [[0, 0]]
    for i in range(n):
        # get current position 
        x, y, direction = coords[-1]
        # get next position
        x_left, y_left, direction_left = left_(x, y, direction)
        if [x_left, y_left] in coords_only:
            x, y, direction = up_(x, y, direction)
        else:
            x, y, direction = x_left, y_left, direction_left
        # add new position to the list
        coords.append([x, y, direction])
        coords_only.append([x, y])
        message = f'At iteration {i+1} the position is {x, y} and the direction is {direction}'
        print(message)
        if check_if_prime(i+1):
            print('prime')
            color = 'black'
            # draw the square
            space.draw_square(x*space.size_sqaure, y*space.size_sqaure, coords = False)
        else:
            color = 'white'
            # draw the square
            space.draw_square(x*space.size_sqaure, y*space.size_sqaure, coords = False, color = 'white')
        # update the dataframe using concat
        # row  = [i, x, y, direction, color]
        final_dataframe = pd.concat([final_dataframe, pd.DataFrame([[i, x, y, direction, color]], columns = ['iteration', 'x', 'y', 'direction', 'color'])], ignore_index = True)

    # save the dataframe
    print(final_dataframe)

    import plotly.graph_objects as go

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=final_dataframe['x'], y=final_dataframe['y'], mode='markers', marker_color=final_dataframe['color']))
    fig.show()
