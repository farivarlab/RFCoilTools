__author__ = "William Mathieu"
__copyright__ = "Copyright 2019, William Mathieu"
__license__ = "MIT"
__date__ = "19Feb2019"

#!/usr/bin/python
import nibabel as nib
import matplotlib.pyplot as plt
import sys
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.patches import Circle
from tkinter import *
from tkinter.filedialog import askopenfilename


root = Tk()
root.withdraw()
root.filename = filedialog.askopenfilename(initialdir = "/", title = "Select NIfTI file", filetypes = (("NIfTI files","*.nii *.nii.gz"),("all files","*.*")))
#print(root.filename)
img = nib.load(root.filename)



"""
root = Tk()


#This is where we lauch the file manager bar.
def OpenFile():
    name = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
                           filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                           title = "Choose a file."
                           )
    print (name)
    #Using try in case user types in unknown file or closes without choosing a file.
    try:
        with open(name,'r') as UseFile:
            print(UseFile.read())
    except:
        print("No file exists")


Title = root.title( "File Opener")
label = ttk.Label(root, text ="I'm BATMAN!!!",foreground="red",font=("Helvetica", 16))
label.pack()

#Menu Bar

menu = Menu(root)
root.config(menu=menu)

file = Menu(menu)

file.add_command(label = 'Open', command = OpenFile)
file.add_command(label = 'Exit', command = lambda:exit())

menu.add_cascade(label = 'File', menu = file)



root.mainloop()
"""

#img = nib.load("MRI_NII_DATA_Test6_MPRAGE_ADNI_20180524171755_3.nii")
img_data = img.get_fdata()
img_shape = img_data.shape

slice_0 = img_data[int(img_shape[0]/2), :, :]
slice_1 = img_data[:, int(img_shape[1]/2), :]
slice_2 = img_data[:, :, int(img_shape[2]/2)]

target_slice = slice_0
def selectSagittal():
	global target_slice
	global slice_0
	target_slice = slice_0
def selectCoronal():
	global target_slice
	global slice_1
	target_slice = slice_1
def selectAxial():
	global target_slice
	global slice_2
	target_slice = slice_2
def Close_start_window():
    start_window.quit()
    start_window.destroy()

start_window = Tk()
start_window.title('Select Orientation')
start_window.config(bg='white')
Sagittal_button = Button(start_window, text = "Sagittal", bg='white', command=selectSagittal)
Coronal_button = Button(start_window, text = "Coronal", bg='white', command=selectCoronal)
Axial_button = Button(start_window, text = "Axial", bg='white', command=selectAxial)
blank_space = Label(start_window, text="          ", bg='white')
Close_start_menu = Button(start_window, text = "GO!", bg='white', command=Close_start_window)

Sagittal_button.grid(sticky='n', row = 0, column = 0)
Coronal_button.grid(sticky='n', row = 1, column = 0)
Axial_button.grid(sticky='n', row = 2, column = 0)
blank_space.grid(sticky='n', row = 3, column = 0)
Close_start_menu.grid(sticky='n', row = 4, column = 0)
start_window.mainloop()

print(target_slice)
NoiseROIradius0 = 10
NoiseROIxGap = 145
NoiseROIyGap = 5

xMax = target_slice.shape[1]
yMax = target_slice.shape[0]

x = np.arange(0, xMax)
y = np.arange(0, yMax)

xCentre = NoiseROIxGap+NoiseROIradius0
yCentre = len(target_slice) - NoiseROIyGap - NoiseROIradius0
mask = (x[np.newaxis,:]-xCentre)**2 + (y[:,np.newaxis]-yCentre)**2 < NoiseROIradius0**2

noise_ROI_values = target_slice[mask]

ROI_noise_mean = np.mean(noise_ROI_values)
ROI_noise_std = np.std(noise_ROI_values)
print("Mean: "+str(ROI_noise_mean))
print("STD: "+str(ROI_noise_std))

# Calculate SNR of image using SNR=A_pixel/STD_noise
slice_SNR = np.true_divide(target_slice, ROI_noise_std)

fig = plt.figure()
ax = fig.add_subplot(111)
fig.subplots_adjust(left=0.25, bottom=0.25)
im = slice_SNR
im1 = ax.imshow(im, cmap="nipy_spectral")
min0 = 0
max0 = np.amax(slice_SNR)
plt.suptitle("SNR Heatmap of Center Slice")
fig.colorbar(im1, label='SNR (Absolute Value)')

circ = Circle((xCentre,yCentre),NoiseROIradius0, fill=False, facecolor=None, edgecolor='white')
ax.add_patch(circ)
plt.text(xCentre, xCentre, str(ROI_noise_std), fontsize=12)

axcolor = 'lightgray'
axmin = fig.add_axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
axmax  = fig.add_axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

smin = Slider(axmin, 'Min', 0, np.amax(slice_SNR), valinit=min0)
smax = Slider(axmax, 'Max', 0, np.amax(slice_SNR), valinit=max0)

def update(val):
    im1.set_clim([smin.val,smax.val])
    fig.canvas.draw()
smin.on_changed(update)
smax.on_changed(update)

plt.show()