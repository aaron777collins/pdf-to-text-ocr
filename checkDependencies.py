import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

#Ensures pip is installed:
subprocess.check_call([sys.executable, "-m", "ensurepip", "--default-pip"])

install('opencv-python')
install('pytesseract')
install('pdf2image')
install('PyPDF2')