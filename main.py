import os
import tkinter as tk
from tkinter import filedialog

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageTk


class MainApplication(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Button(self, text='Select Image', command=self.select_images).grid(column=2, row=1)

        self.entry = tk.Entry(self, width=15)
        self.entry.insert(0, 'Nikko Copyright 2022')
        self.entry.grid(column=2, row=2)

        tk.Button(self, text='Add Watermark', command=self.add_watermark).grid(column=2, row=3)
        tk.Button(self, text='Clear Image List', command=self.clear_image_list).grid(column=2, row=4)

        self.image_names = []

    def openfilename(self):
        """Open file dialog box to select image"""
        files = filedialog.askopenfilenames(title='Open File', initialdir=os.getcwd(), multiple=True)

        for file in list(files):
            self.image_names.append(file)

    def select_images(self):
        """Opens image then using PIL psdraw, add the watermark"""

        # select the name of the image form a folder
        self.openfilename()

        # display images
        self.put_image_panel()

    def put_image_panel(self):
        """Display the selected images"""
        for image_name in self.image_names:
            # open the image
            img = Image.open(image_name)

            # resize the image so it fits the window, but will not affect original size
            ratio = img.size[0] / img.size[1]
            img = img.resize((int(100 * ratio), int(100)), Image.ANTIALIAS)

            # add image to widgets in tk using PhotoImage class
            img = ImageTk.PhotoImage(img)

            # set the image as img
            self.panel = tk.Label(self, image=img)
            self.panel.image = img

            # display image, occupy one row at a time
            self.panel.grid(row=self.image_names.index(image_name))

        print(f'image selected {self.image_names}')

    def add_watermark(self):
        """Add watermark"""
        for image_filename in self.image_names:
            if not os.path.exists('watermarked'):
                os.mkdir('watermarked')
            with Image.open(image_filename).convert('RGBA') as im:
                # reference :  https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#example-draw-partial-opacity-text

                folder_path, file_name = os.path.split(image_filename)
                watermark = self.entry.get()

                # dynamic angle, using arctan(opp/adj) and converting it to degrees, the angle in relative to the image dimension
                dynamic_angle = np.degrees(np.arctan(im.size[1] / im.size[0]))
                print(im.size)
                print(dynamic_angle)

                # make a blank image for the text, initialized to transparent text color
                txt = Image.new('RGBA', im.size, (255, 255, 255, 0))

                # get a font
                fnt = ImageFont.truetype('arial.ttf', 200, encoding='unic')

                # get a drawing context
                draw = ImageDraw.Draw(txt)

                # draw text
                draw.text((int(im.size[0] / 5), int(im.size[1] / 2)), watermark.upper(), font=fnt,
                          fill=(255, 255, 255, 100))

                output = Image.alpha_composite(im, txt.rotate(dynamic_angle))
                # output.show()
                converted_output = output.convert('RGB')

                if not os.path.exists('watermarked'):
                    os.mkdir('watermarked')
                outputfilename = os.getcwd() + '\watermarked\\' + file_name + '_watermarked.jpeg'
                converted_output.save(outputfilename, 'JPEG')

        print('add watermark button pressed')

    def clear_image_list(self):
        self.image_names = []
        self.panel.config(image='')


if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root).pack()
    root.mainloop()
