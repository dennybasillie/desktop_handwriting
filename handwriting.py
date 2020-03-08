#!/usr/bin/env python3
from tkinter import *
from providers.googleIME import GoogleIMERecognizer

class HandWriting(Frame):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'
    SUPPORTED_LANGUAGES = ['en', 'ja', 'ko', 'zh_CN', 'zh_TW']

    def __init__(self, root):
        self.root = root

        self.init_UI()
        self.init_state()

    def init_UI(self):
        self.root.title('Handwriting')

        # Detection result
        self.text_sentence = Text(self.root, height=1, width=30)
        self.text_sentence.grid(row=0, column=0)
        # Submit current handwriting
        self.button_submit = Button(self.root, text='Submit', command=self.submit)
        self.button_submit.grid(row=0, column=1)
        # Change pen size
        self.scale_pen_size = Scale(self.root, from_=1, to=10, orient=HORIZONTAL, command=self.change_pen_size)
        self.scale_pen_size.set(self.DEFAULT_PEN_SIZE)
        self.scale_pen_size.grid(row=0, column=2)
        # Change language
        self.language = StringVar(self.root)
        self.language.set(self.SUPPORTED_LANGUAGES[0])
        self.option_language = OptionMenu(self.root, self.language, *self.SUPPORTED_LANGUAGES, command=self.change_language)
        self.option_language.grid(row=0, column=3)
        # Writing canvas
        self.c = Canvas(self.root, bg='white', width=640, height=360)
        self.c.grid(row=1, columnspan=4)  # self.c.pack(fill='both',expand=True) 

        # Bind events
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.c.bind('<Return>', self.submit)
        self.c.focus_force()

    def init_state(self):
        self.prev_positions = { 'x': None, 'y': None }
        self.strokes = { 'x': [], 'y': [] }

        self.line_width = self.scale_pen_size.get()
        self.color = self.DEFAULT_COLOR
        self.size = { 'width': self.c.winfo_reqwidth(), 'height': self.c.winfo_reqheight() }
        self.recognizer = GoogleIMERecognizer({ 'width': self.size['width'], 'height': self.size['height'], 'language': self.language.get() })

    def change_pen_size(self, event):
        self.line_width = event

    def change_language(self, event):
        self.recognizer.change_language(event)

    def paint(self, event):
        if self.prev_positions['x'] and self.prev_positions['y']:
            self.c.create_line(self.prev_positions['x'], self.prev_positions['y'], event.x, event.y,
                               width=self.line_width, fill=self.color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.prev_positions = { 'x': event.x, 'y': event.y }
        self.strokes['x'].append(event.x)
        self.strokes['y'].append(event.y)

    def reset(self, event):
        self.prev_positions = { 'x': None, 'y': None }
        #TODO: check if is dot / contain element
        self.recognizer.add_stroke([self.strokes['x'], self.strokes['y']])
        self.strokes['x'] = []
        self.strokes['y'] = []

    def submit(self, event=None):
        result = self.recognizer.detect()
        #TODO: popup window for selection
        self.text_sentence.insert(END, result[0])
        self.c.delete("all")
        


def main():
    root = Tk()
    gui = HandWriting(root)
    root.mainloop()


if __name__ == '__main__':
    main()