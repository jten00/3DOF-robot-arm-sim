import tkinter as tk
import math

class SimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("3DOF Robotic Arm Simulation")

        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()

        self.counter_text = self.canvas.create_text(10, 10, anchor="nw", text="", font=("Helvetica", 10))
        
        self.matrix_text1 = self.canvas.create_text(self.canvas_width - 10, 20, anchor="ne", text="", font=("Helvetica", 10))
        self.matrix_text2 = self.canvas.create_text(self.canvas_width - 10, 70, anchor="ne", text="", font=("Helvetica", 10))
        self.matrix_text3 = self.canvas.create_text(self.canvas_width - 10, 120, anchor="ne", text="", font=("Helvetica", 10))

        self.origin_x = self.canvas_width / 2
        self.origin_y = self.canvas_height / 2

        self.draw_coordinate_plane()

        self.line_id1 = None
        self.line_id2 = None
        self.line_id3 = None

        self.angle_slider1 = self.create_angle_slider("First Line Angle", -math.pi, math.pi)
        self.angle_slider2 = self.create_angle_slider("Second Line Angle", -math.pi, math.pi)
        self.angle_slider3 = self.create_angle_slider("Third Line Angle", -math.pi, math.pi)

        self.update_lines_from_sliders()

    def create_angle_slider(self, label, from_, to):
        slider = tk.Scale(self.root, from_=from_, to=to, resolution=0.01, orient='horizontal', label=label, length=self.canvas_width)
        slider.pack()
        slider.bind("<B1-Motion>", self.update_lines_from_sliders)
        return slider

    def draw_coordinate_plane(self):
        for i in range(0, self.canvas_height, 10):
            self.canvas.create_line(0, i, self.canvas_width, i, fill="#ddd")

        for i in range(0, self.canvas_width, 10):
            self.canvas.create_line(i, 0, i, self.canvas_height, fill="#ddd")

        self.canvas.create_line(self.origin_x, 0, self.origin_x, self.canvas_height, fill="black")
        self.canvas.create_line(0, self.origin_y, self.canvas_width, self.origin_y, fill="black")

    def draw_lines_with_angles(self, angle1, angle2, angle3):
        for line_id in [self.line_id1, self.line_id2, self.line_id3]:
            if line_id:
                self.canvas.delete(line_id)

        self.draw_coordinate_plane()

        end_x1, end_y1 = self.calculate_end_point(100, angle1)
        self.line_id1 = self.canvas.create_line(self.origin_x, self.origin_y, end_x1, end_y1, fill='red', arrow=tk.LAST)

        end_x2, end_y2 = self.calculate_end_point(100, angle1 + angle2, start_x=end_x1, start_y=end_y1)
        self.line_id2 = self.canvas.create_line(end_x1, end_y1, end_x2, end_y2, fill='blue', arrow=tk.LAST)

        end_x3, end_y3 = self.calculate_end_point(20, angle1 + angle2 + angle3, start_x=end_x2, start_y=end_y2)
        self.line_id3 = self.canvas.create_line(end_x2, end_y2, end_x3, end_y3, fill='green', arrow=tk.LAST)

        self.update_counter(end_x3, end_y3)

        self.update_matrix_text(self.matrix_text1, angle1)
        self.update_matrix_text(self.matrix_text2, angle1 + angle2)
        self.update_matrix_text(self.matrix_text3, angle1 + angle2 + angle3)

        self.canvas.tag_raise(self.counter_text)
        self.canvas.tag_raise(self.matrix_text1)
        self.canvas.tag_raise(self.matrix_text2)
        self.canvas.tag_raise(self.matrix_text3)

    def calculate_end_point(self, length, angle, start_x=None, start_y=None):
        if start_x is None or start_y is None:
            start_x = self.origin_x
            start_y = self.origin_y

        end_x = start_x + length * math.cos(angle)
        end_y = start_y - length * math.sin(angle) 
        return end_x, end_y

    def update_counter(self, end_x, end_y):
        angle1 = self.angle_slider1.get()
        angle2 = self.angle_slider2.get()
        angle3 = self.angle_slider3.get()
        converted_end_x = (end_x - self.origin_x) / 10
        converted_end_y = (self.origin_y - end_y) / 10
        counter_text = f"End Point: ({int(converted_end_x)}, {int(converted_end_y)})\nAngles: {angle1:.2f}, {angle2:.2f}, {angle3:.2f} rad"
        self.canvas.itemconfigure(self.counter_text, text=counter_text)

    def update_matrix_text(self, matrix_text_item, angle):
        rotation_matrix = [
            [math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)]
        ]
        matrix_text = f"Rotation Matrix:\n[{rotation_matrix[0][0]:.2f}, {rotation_matrix[0][1]:.2f}]\n[{rotation_matrix[1][0]:.2f}, {rotation_matrix[1][1]:.2f}]"
        self.canvas.itemconfigure(matrix_text_item, text=matrix_text)

    def update_lines_from_sliders(self, event=None):
        angle1 = self.angle_slider1.get()
        angle2 = self.angle_slider2.get()
        angle3 = self.angle_slider3.get()
        self.draw_lines_with_angles(angle1, angle2, angle3)

    def start(self):
        self.root.mainloop()

root = tk.Tk()
app = SimulationApp(root)

app.start()
