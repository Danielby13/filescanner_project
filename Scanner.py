from imutils.perspective import four_point_transform
from skimage.filters import threshold_local
import cv2
import imutils
import tkinter.filedialog
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox

class FileScannerGUI:
    def __init__(self, master):  # gui screen
        self.master = master
        master.title("FileScanner")
        master.geometry('850x630')
        self.label = Label(master, text="Welcome to Inbal and Daniel FileScanner", fg="white", bg="#34A2FE", width=1300, height=1, font=("Calibri Bold", 14))
        self.label.pack()

        self.open_file = Button(master, text="Open File", command=self.find_path, width=15, bg="#34A2FE", fg="white", font=("Calibri Bold", 11))
        self.open_file.place(x=5, y=35)

        self.start_black_white = Button(master, text="Convert to Black&White", command=self.camscanner_generator_black_white, width=25, bg="#34A2FE",fg="white",font=("Calibri Bold", 11))
        self.start_black_white.place(x=140, y=35)

        self.start_gray_scale = Button(master, text="Convert to Grayscale", command=self.camscanner_generator_gray_scale, width=25, bg="#34A2FE",fg="white",font=("Calibri Bold", 11))
        self.start_gray_scale.place(x=355, y=35)

        self.start_original_color = Button(master, text="Convert to Original Color", command=self.camscanner_generator_original_color, width=25, bg="#34A2FE",fg="white",font=("Calibri Bold", 11))
        self.start_original_color.place(x=570, y=35)

        # place of original image display
        width = 400
        height = 500
        self.im = Image.open('background_image1.png')
        self.img = self.im.resize((width, height), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.img)
        self.image_label = Label(master, image=self.image)
        self.image_label.place(x=15, y=80)

        # place of converted image display
        self.im2 = Image.open('background_image2.png')
        self.img2 = self.im2.resize((width, height), Image.ANTIALIAS)
        self.image2 = ImageTk.PhotoImage(self.img2)
        self.image_label2 = Label(master, image=self.image2)
        self.image_label2.place(x=435, y=80)

        # save button of converted image
        save_button = Button(master, text="Save", command=self.save_output, width=30, bg="#34A2FE", fg="white", font=("Calibri Bold", 11))
        save_button.place(x=300, y=595)

    # open original image and save the path
    def find_path(self):
        try:
            width = 400
            height = 500
            self.path = tkinter.filedialog.askopenfilename()
            im = Image.open(self.path)
            img = im.resize((width, height), Image.ANTIALIAS)
            tkimage = ImageTk.PhotoImage(img)
            self.image_label.configure(image=tkimage)
            self.image_label.image = tkimage

            image = cv2.imread(self.path)  # open the image
            global ratio, original_image, screenSquare
            ratio = image.shape[0] / 1000
            original_image = image.copy()
            image = imutils.resize(image, height=1000)

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to grayscale
            gray = cv2.GaussianBlur(gray, (5, 5), 0)  # blur the image for better edge detection ( 2nd - kernel size, 3rd - sigma)
            edge_detector = cv2.Canny(gray, 75, 200)  # find edges (75, 200 -thresholding values)

            contours, hierarchy = cv2.findContours(edge_detector, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # find contours
            sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)  # sort the contours

            for contour in sorted_contours:  # loop over the sorted contours
                peri = cv2.arcLength(contour, True)  # try to find a square
                approx = cv2.approxPolyDP(contour, 0.02 * peri, True)  # approx square

                if len(approx) == 4:  # if approx found square, it will be our screen
                    screenSquare = approx
                    break
        except:
            messagebox.showinfo('Error', 'please choose valid file')

    def save_output(self):  # save the converted image
        try:
            cv2.imwrite("output.jpg", top_down_image)
            self.saved_msg()
        except:
            self.error_msg()

    def camscanner_generator_black_white(self):  # black&white
        try:
            global top_down_image
            top_down_image = four_point_transform(original_image, screenSquare.reshape(4, 2) * ratio)  # to preform top-down view
            top_down_image = cv2.cvtColor(top_down_image, cv2.COLOR_BGR2GRAY) # convert the image to grayscale
            thresh = threshold_local(top_down_image, 17, offset=10)  # threshold the image for black&white effect
            top_down_image = (top_down_image > thresh).astype("uint8") * 255

            width = 400
            height = 500
            im = Image.fromarray(top_down_image)
            global img
            img = im.resize((width, height), Image.ANTIALIAS)
            tkimage = ImageTk.PhotoImage(img)
            self.image_label2.configure(image=tkimage)  # display the converted image
            self.image_label2.image = tkimage

        except:
            self.error_msg()

    def camscanner_generator_gray_scale(self):
        try:
            global top_down_image
            top_down_image = four_point_transform(original_image, screenSquare.reshape(4, 2) * ratio) # to preform top-down view
            top_down_image = cv2.cvtColor(top_down_image, cv2.COLOR_BGR2GRAY) # convert the image to grayscale

            width = 400
            height = 500
            im = Image.fromarray(top_down_image)
            img = im.resize((width, height), Image.ANTIALIAS)
            tkimage = ImageTk.PhotoImage(img)
            self.image_label2.configure(image=tkimage)  # display the converted image
            self.image_label2.image = tkimage

        except:
            self.error_msg()

    def camscanner_generator_original_color(self):
        try:
            global top_down_image
            top_down_image = four_point_transform(original_image, screenSquare.reshape(4, 2) * ratio)  # to preform top-down view
            warped1 = cv2.cvtColor(top_down_image, cv2.COLOR_BGR2RGBA)  # convert BGR to RGB

            width = 400
            height = 500
            im = Image.fromarray(warped1)
            img = im.resize((width, height), Image.ANTIALIAS)
            tkimage = ImageTk.PhotoImage(img)
            self.image_label2.configure(image=tkimage)  # display the converted image
            self.image_label2.image = tkimage

        except:
            self.error_msg()

    def saved_msg(self):  # save message
        messagebox.showinfo('Image saved', 'Image saved successfully!')

    def error_msg(self):  # error message
        messagebox.showinfo('Error', 'Error has occurred')


root = Tk()  # GUI display
my_gui = FileScannerGUI(root)
root.mainloop()


