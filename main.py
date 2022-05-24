import cv2
import pytesseract
import numpy as np
import sys
import os
from PIL import Image
from pdf2image import convert_from_path
import tkinter
import tkinter.filedialog
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
import tempfile
import ntpath

# NOTE: the following tutorials were incorperated:
# https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/
# https://nanonets.com/blog/ocr-with-tesseract/
# https://pypi.org/project/pdf2image/

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


##functions that help####################
#
# # get grayscale image
# def get_grayscale(image):
#     return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#
# # noise removal
# def remove_noise(image):
#     return cv2.medianBlur(image, 5)
#
#
# # thresholding
# def thresholding(image):
#     return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
#
#
# # dilation
# def dilate(image):
#     kernel = np.ones((5, 5), np.uint8)
#     return cv2.dilate(image, kernel, iterations=1)
#
#
# # erosion
# def erode(image):
#     kernel = np.ones((5, 5), np.uint8)
#     return cv2.erode(image, kernel, iterations=1)
#
#
# # opening - erosion followed by dilation
# def opening(image):
#     kernel = np.ones((5, 5), np.uint8)
#     return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
#
#
# # canny edge detection
# def canny(image):
#     return cv2.Canny(image, 100, 200)
#
#
# # skew correction
# def deskew(image):
#     coords = np.column_stack(np.where(image > 0))
#     angle = cv2.minAreaRect(coords)[-1]
#     if angle < -45:
#         angle = -(90 + angle)
#
#     else:
#     angle = -angle
#     (h, w) = image.shape[:2]
#     center = (w // 2, h // 2)
#     M = cv2.getRotationMatrix2D(center, angle, 1.0)
#     rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
#     return rotated
#
#
# # template matching
# def match_template(image, template):
#     return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
#

#############

def main():
    # get file to convert from user
    root = tkinter.Tk()
    root.withdraw()
    file = tkinter.filedialog.askopenfile(title='Open Input File', parent=root);
    print("processing:" + str(file) + "\n");

    # get output folder from user
    outputFolder = tkinter.filedialog.askdirectory(title='Select Output Folder', parent=root);

    filetypes = (
        ('text file', '*.txt'),
        ('All files', '*.*')
    )

    initialFileName = str(ntpath.basename(file.name))

    initialFileName = initialFileName.split(".")[0]  # remove extension

    outputFilePath = tkinter.filedialog.asksaveasfilename(title='Select Output File',
                                                          initialfile=initialFileName, parent=root,
                                                          filetypes=filetypes, initialdir=outputFolder,
                                                          defaultextension='.txt')

    # save images as jpg in output folder
    with tempfile.TemporaryDirectory() as path:
        # saves pdf as a list of PIL images
        print("Converting PDF to a list of PIL images:\n...")
        pages = convert_from_path(file.name, output_folder=path, poppler_path=r"poppler-21.03.0\Library\bin");

        # used for counting pages
        image_counter = 1

        print("Saving pdf to images (jpg):")

        for page in pages:
            print("saving page: " + str(image_counter));

            # converting each page in the pdf to a jpg file

            # new file name
            newFile = os.path.join(outputFolder, "page_" + str(image_counter) + ".jpg")

            # save the new jpg file
            page.save(newFile, 'JPEG')

            image_counter += 1

    # delete existing output if it exists
    if os.path.exists(outputFilePath):
        os.remove(outputFilePath)

    # creating output file to write the output
    outputFile = open(outputFilePath, "a")  # opened in append mode so that all images are in the same file

    print("\n\nprocessing images:")

    for i in range(1, image_counter):  # for every image

        progressAsFloat = "{:.1f}".format((float(i) / image_counter * 100))

        progress = str(progressAsFloat) + "%"

        print("Processing image: " + str(i) + " out of " + str(image_counter) + " - " + progress)
        # open each file
        currentFile = os.path.join(outputFolder, "page_" + str(i) + ".jpg")

        # process image
        result = str(pytesseract.image_to_string(Image.open(currentFile), lang='eng'))

        outputFile.write(result + '\n\n');

    outputFile.close()


### end of main

main()
