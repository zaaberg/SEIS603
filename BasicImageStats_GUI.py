from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image as im
from PIL import ImageStat as imstat
import os
import matplotlib.pyplot as plot
from matplotlib.backends.backend_tkagg import FigureCanvasAgg, NavigationToolbar2TkAgg

class App():
    master = Tk()

    def __init__(self):
        # Assign additional class-level attributes
        # Execute core methods
        self.config_app()
        self.app_config()
        self.run_app()

    def config_app(self):
        # Configure app
        self.master.title('Basic Image Stats')
        loc_bitmap = os.path.join(os.path.dirname(__file__), 'assets', 'icon', 'camera.ico')
        try:
            self.master.iconbitmap(loc_bitmap)
        except:
            pass
    def app_config(self):
        # Insert widgets
        input_label = Label(self.master)
        input_label['text'] = 'Input Image File:'
        input_label.grid(row=2, column=0, pady=3)

        self.input_entry_box = input_entry_box = Entry(self.master)
        input_entry_box['width'] = 50
        input_entry_box.grid(row=2, column=1, pady=3)

        input_button = Button(self.master)
        input_button['text'] = 'BROWSE'
        input_button['command'] = self.open_file
        input_button.grid(row=2, column=2, padx=2, pady=3)

        self.labelbox = labelbox = LabelFrame(self.master)

        labelbox['text']='Help'
        context= Label(labelbox, text='''This tool will provide some basic statistics on images for
JPG, PNG, and a few other simple image types.

Use the 'Browse' button to find your image file. Click 
'Execute' to begin the script.

You'll be provided with a histogram of pixel values. Close
out of it and the stats table will pop-up.

Statistics will be provided per layer (RGB or RGBA).''')
        context.grid(row=0,column=2)
        labelbox.grid(row=0, column=8, padx=10, rowspan=6)

        exec_button = Button(self.master)
        exec_button['text'] = 'EXECUTE'
        exec_button['command'] = self.execute_tool
        exec_button.grid(row=5, column=1, padx=2, pady=5)

    def open_file(self):
        # Define file dialog options
        options = {}
        options['title'] = 'Input GDB:'
        options['initialdir'] = 'C:/'
        # Open file dialog
        file_path = filedialog.askopenfilename(**options)
        # Check to make sure a file was specified
        if file_path:
            # Insert file path into entry box
            self.input_entry_box.delete(0,END)
            self.input_entry_box.insert(0, file_path)
            
    def execute_tool(self):
        input_image = self.input_entry_box.get()

        try:
            with im.open(input_image) as rast_open:
                stats = imstat.Stat(rast_open)

                stat_status = '''                                                     
Min/Max:\n\n{minmax}\n\n
Pixel Count:\n\n{pcount}\n\n
Sum of Pixels:\n\n{psum}\n\n
Sq. Sum of Pixels:\n\n{psum2}\n\n
Pixel Mean:\n\n{pmean}\n\n
Pixel Median:\n\n{pmedian}\n\n
Root-Mean-Square(RMS):\n\n{prms}\n\n
Variance:\n\n{pvar}\n\n
Standard Deviation:\n\n{pstddev}
                '''.format(minmax=stats.extrema, pcount=stats.count, psum=stats.sum, psum2=stats.sum2, pmean=stats.mean,
                           pmedian=stats.median, prms=stats.rms, pvar=stats.var, pstddev=stats.stddev)

                plot.hist(rast_open.histogram(), bins=256)
                plot.show()

                messagebox.showinfo("Image Statistics", stat_status)
        except IOError:
            messagebox.showinfo("Error!", "Error: Not a recognized image type.")

    def run_app(self):
        # Run the mainloop
        self.master.mainloop()


if __name__ == '__main__':

    new_window = App()
