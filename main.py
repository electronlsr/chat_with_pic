from pic_to_xlsx import pic_to_xlsx
from tkinter import Tk
from tkinter.filedialog import askopenfilename

root = Tk()
root.withdraw()
pic_path = askopenfilename(initialdir=os.path.dirname(__file__), title="Select an image file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.webp")])
root.destroy()
if not pic_path:
    print("No file selected. Exiting...")
    exit()
    
print("XLSX file:", pic_to_xlsx(pic_path))