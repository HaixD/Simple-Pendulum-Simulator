import math
import tkinter
from sys import argv
from time import process_time
from physics.body_replay import BodyReplay

if __name__ == '__main__':
    file_path = argv[1]
    
    #TKINTER VISUAL PARAMETERS
    window_size = (540, 960)
    system_offsets = (480, 240)
    ball_radius = 7
    positional_scale = 400
    arrow_scale = 5
    refresh_ms = 1
    min_line_size = 1

    #SIMULATION PARAMETERS
    pivot_x = 0 + system_offsets[0]
    pivot_y = 0 + system_offsets[1]
    
    body = BodyReplay.load(file_path)
    process_start = process_time()

    def update():
        canvas.delete('all')

        position, velocity, acceleration = body.get_state()

        x = int(position[0][1] * positional_scale) + system_offsets[0]
        y = -int(position[1][1] * positional_scale) + system_offsets[1]

        #DRAW PIVOT
        canvas.create_oval(pivot_x - ball_radius, pivot_y - ball_radius, 
                           pivot_x + ball_radius, pivot_y + ball_radius, 
                           fill = 'black')
        
        #DRAW PENDULUM MASS
        canvas.create_oval(x - ball_radius, y - ball_radius, 
                           x + ball_radius, y + ball_radius, 
                           fill = 'black')
        
        #DRAW "ROPE"
        canvas.create_line(x, y,
                           pivot_x, pivot_y, 
                           width = 3, fill = 'black')

        #ACCELERATION LINE
        if math.sqrt(acceleration[0][1] ** 2 + acceleration[1][1] ** 2) >= min_line_size:
            canvas.create_line(x, y,
                               x + acceleration[0][1] * arrow_scale,
                               y + -acceleration[1][1] * arrow_scale, 
                               arrow = tkinter.LAST, width = 3, fill = 'red')
        
        #VELOCITY LINE
        if math.sqrt(velocity[0][1] ** 2 + velocity[1][1] ** 2) >= min_line_size:
            canvas.create_line(x, y,
                               x + velocity[0][1] * arrow_scale,
                               y + -velocity[1][1] * arrow_scale, 
                               arrow = tkinter.LAST, width = 3, fill = 'blue')

        #PHYSICS STATUS
        canvas.create_text(10, 10, 
                           text = f'acceleration: ({acceleration[0][1]:.2f}, {acceleration[1][1]:.2f})\n'
                                  f'velocity: ({velocity[0][1]:.2f}, {velocity[1][1]:.2f})\n'
                                  f'position: ({position[0][1]:.2f}, {position[1][1]:.2f})\n'
                                  f'distance: {math.sqrt(position[0][1] ** 2 + position[1][1] ** 2):.2f}\n' 
                                  f'angle: {math.degrees(math.atan2(position[1][1], position[0][1]) + math.pi/2):.2f}\n'
                                  f'time: {body.time:.2f}',
                           anchor = 'nw',
                           font = ('Arial', 16))

        while body.time < (process_time() - process_start):
            if not body.step():
                return

        window.after(refresh_ms, update)

    print('reading complete...')
        
    window = tkinter.Tk()
    canvas = tkinter.Canvas(window, bg = 'white', height = window_size[0], width = window_size[1])
    
    window.after(refresh_ms, update)

    canvas.pack()
    window.mainloop()
