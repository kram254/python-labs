from tkinter import ttk, messagebox
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from random import gauss, randint

class dataGenerator:
    def __init__(self, low=0, high=1, start=0.5):
        self.value = start
        self.low = low
        self.high = high
        self.range = high - low
        self.isRise = True 
        self.init()

    # To prevent continuous rise or fall 
    def init(self):
        self.sprint = gauss(30, 6)       
        if (self.isRise == True):
            self.delta = randint(0, 10) * 0.001
        else:
            self.delta = randint(-10, 0) * 0.001

        self.isRise = not self.isRise
        self.counter = 0

    # Random value between 0 and 1
    def update_value(self):
        self.counter += 1
        if self.counter >= self.sprint:
            self.init()
        if self.value + self.delta < 0 or self.value + self.delta > 1:  
            self.value -= self.delta
        else:
            self.value += self.delta

        return self.value

    @property
    def data(self):
        variation = randint(-10, 10) * 0.005
        if self.value + variation < 0 or self.value + variation > 1:
            variation *= -1

        return (self.update_value() + variation) * self.range + self.low   

class TkApp(Tk):
    frame: Frame
    cnvs: Canvas

    # Values used for drawing
    canvas_width = 600
    canvas_height = 500
    incrementY = 20
    incrementX = 20
    startY = canvas_height
    startX = 100
    labelStartX = 50

    # Lists coordinates storage

    lineX = []
    lineY = []
    barItems = []
        
    def __init__(self, title):
        Tk.__init__(self, title)
        self.title(title)

        self.generate_values()
        self.create_form_ui()
        self.create_canvas()
        self.set_form_style()

    def generate_values(self):
        # Generate 20 values bewtween 0 and 100 (Humididty % range)
        gen = dataGenerator(low=0, high=100, start=0.4)
        self.listOfValues = [gen.data for _ in range(20)]
        print(self.listOfValues)  # Print values to compare to chart

    def create_form_ui(self, parent=None):
        self.minsize(500, 500)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Setup frame
        self.frame = Frame(self, width=500, height=500)
        self.frame['padding'] = (5, 10)
        self.frame['borderwidth'] = 10
        self.frame['relief'] = 'ridge'
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid(sticky=(W, E))

        # Fonts
        self.option_add("*Font", "arial")
        title_font = {'font': ('Helvetica', 21)}

        # Create labels
        Label(self.frame,
              text='Humidity Data',
              **title_font).grid(row=0, columnspan=3, pady=10)
        Label(self.frame, text='Value:').grid(
            column=0, row=1, sticky=W, padx=5)

        # Create labels
        Label(self.frame, text='Data range:').grid(
            column=0, row=1, sticky=W, padx=5)
        self.dt = ttk.Label(self.frame, text="Data range: 0-5")
        self.dt.grid(column=1, row=2, sticky=W, padx=5)

        # Create entry
        vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')  # Validation for input
        self.input_value = StringVar()
        self.input_box = Entry(self.frame,
                               textvariable=self.input_value,
                               validate='key',
                               validatecommand=vcmd)
        self.input_box.grid(column=1, row=1, sticky=(W, E))

        Button(self.frame,
               text='Start',
               style='TButton',
               command=self.update_range).grid(column=2, row=1, sticky=(W, E), padx=5)

    def create_canvas(self):
        self.cnvs = Canvas(self.frame,
                           width=self.canvas_width,
                           height=self.canvas_height,
                           bg='#dde5b6',
                           bd=0, highlightthickness=0,
                           relief='ridge')
        self.cnvs.grid(row=3, columnspan=3)

        # Create lines and labels for graph
        startValue = 0
        for x in range(21):
            self.startY -= self.incrementY
            if x % 2 == 0:
                self.cnvs.create_line(
                    self.labelStartX, self.startY, self.labelStartX + self.incrementX, self.startY, width=2)
                self.cnvs.create_text(
                    self.labelStartX - 20, self.startY, text=str(startValue)+'%')
                startValue += 10
            else:
                self.cnvs.create_line(self.labelStartX + self.incrementX, self.startY,
                                      self.labelStartX + (self.incrementX / 2), self.startY, width=2)

        # Draw bars
        self.barStartY = self.canvas_height - self.incrementY
        for x in range(6):
            self.barStartX = self.startX + self.incrementX + 10
            barEndY = self.canvas_height - \
                (self.listOfValues[x] / 100 * self.canvas_height)
            # self.barItems.append(self.cnvs.create_rectangle(
            #     self.startX, self.barStartY, self.barStartX + self.incrementX, barEndY, fill='green'
            # ))
            self.startX = self.barStartX + 30
            self.lineX.append(self.barStartX)
            self.lineY.append(barEndY)

        # Draw line
        self.line = self.cnvs.create_line(
            self.lineX[0], self.lineY[0],
            self.lineX[1], self.lineY[1],
            self.lineX[2], self.lineY[2],
            self.lineX[3], self.lineY[3],
            self.lineX[4], self.lineY[4],
            self.lineX[5], self.lineY[5],
            width=3, fill='red'
        )

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        if (value_if_allowed != ''):
            try:
                value = float(value_if_allowed)
                if value >= 0 and value <= 14:
                    return True
                else:
                    messagebox.showinfo(
                        'Invalid Input', 'Maximum value is 14. Data range can only be between 0 and 19.')
                    return False
            except ValueError:
                return False
        return True

    def set_form_style(self):
        style = Style()
        style.theme_use('alt')
        style.configure('.',
                        background='#90a140',
                        foreground='#2a3052')
        style.configure('TButton', font="Arial 12",
                        foreground="black", background="white")

    def update_range(self):
        if self.input_value.get():
            high_range = int(self.input_value.get()) + 5

            # Display range on UI
            self.dt['text'] = "Data range: " + \
                self.input_value.get() + "-" + str(high_range)
            self.startX = 10

            # Redraw bars
            counter = high_range - 5
            self.lineY.clear()
            self.startX = 100
            for item in self.barItems:
                self.barStartX = self.startX + self.incrementX + 10
                # Scale the values to match the canvas
                barEndY = self.canvas_height - \
                    (self.listOfValues[counter] / 100 * self.canvas_height)
                coords = self.startX, self.barStartY, self.barStartX + self.incrementX, barEndY
                self.cnvs.coords(item, coords)
                self.startX = self.barStartX + 30
                # Add to list of y coordinates for drawing the line
                self.lineY.append(barEndY)
                counter += 1

            # Redraw line
            lineCoords = self.lineX[0], self.lineY[0], self.lineX[1], self.lineY[1], self.lineX[2], self.lineY[
                2], self.lineX[3], self.lineY[3], self.lineX[4], self.lineY[4], self.lineX[5], self.lineY[5]
            self.cnvs.coords(self.line, lineCoords)


app = TkApp('Humidity Data')
app.mainloop()    