import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from tensorflow.keras.models import load_model
import os

# Loading the model
model = load_model('Animal_Detector.keras')

# Verify model summary
model.summary()

# Initializing the GUI
top = tk.Tk()
top.geometry('800x600')
top.title('Animal Detector')
top.configure(background='#CDCDCD')

# Initializing the labels
label1 = Label(top, background="#CDCDCD", font=('arial', 15, 'bold'))
label2 = Label(top, background="#CDCDCD", font=('arial', 15, 'bold'))
sign_image = Label(top)

# Define animal categories
herbivores = ['Cow', 'Sheep', 'Horse', 'Elephant', 'Squirrel']
carnivores  = ['Dog', 'Cat', 'Spider', 'Monkey', 'Chicken']

# Defining Detect function which detects the animal in image using the model
def Detect(file_path):
    try:
        image = Image.open(file_path)
        image = image.resize((224, 224))  # Resize image to the size expected by the model
        image = np.array(image)
        if image.shape[2] == 4:  # Convert RGBA to RGB if needed
            image = image[:, :, :3]
        image = np.expand_dims(image, axis=0)
        image = image / 255.0  # Normalize the image
        
        pred = model.predict(image)
        print(f"Prediction raw output: {pred}")
        
        pred_class = np.argmax(pred, axis=1)[0]
        print(f"Predicted class index: {pred_class}")
        
        animals = ['Cat', 'Dog', 'Horse', 'Elephant', 'Monkey', 'Squirrel', 'Sheep', 'Cow', 'Spider', 'Chicken']  # Adjust based on your model classes
        
        # Check if predicted class index is within the bounds of the animals list
        if pred_class < len(animals):
            predicted_animal = animals[pred_class]
            print('Predicted Animal is ' + predicted_animal)
            
            if predicted_animal in carnivores:
                category = 'Carnivore'
            elif predicted_animal in herbivores:
                category = 'Herbivore'
            else:
                category = 'Unknown'
            
            label1.configure(foreground="#011638", text=f"Animal: {predicted_animal}")
            label2.configure(foreground="#011638", text=f"Category: {category}")
        else:
            print("Error: Predicted class index out of range.")
            label1.configure(foreground="#011638", text="Error: Unknown animal")
            label2.configure(text="")
    except Exception as e:
        print(f"Error during detection: {e}")

# Defining Show_detect button function
def show_Detect_Button(file_path):
    Detect_b = Button(top, text="Detect image", command=lambda: Detect(file_path), padx=10, pady=5)
    Detect_b.configure(background="#364156", foreground='white', font=('arial', 10, 'bold'))
    Detect_b.place(relx=0.79, rely=0.46)

# Upload image function
def Upload_image():
    try:
        file_path = filedialog.askopenfilename(initialdir=os.path.join(os.getcwd(), 'raw-img'))
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width() / 2.25), (top.winfo_height() / 2.25)))
        im = ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image = im
        label1.configure(text=' ')
        label2.configure(text=' ')
        show_Detect_Button(file_path)
    except Exception as e:
        print(f"Error loading image: {e}")

upload = Button(top, text="Upload an image", command=Upload_image, padx=10, pady=5)
upload.configure(background="#364156", foreground='white', font=('arial', 10, 'bold'))
upload.pack(side='bottom', pady=50)
sign_image.pack(side='bottom', expand=True)

label1.pack(side="bottom", expand=True)
label2.pack(side="bottom", expand=True)
heading = Label(top, text='Animal Detector', pady=20, font=("arial", 20, 'bold'))
heading.configure(background="#CDCDCD", foreground="#364156")
heading.pack()

top.mainloop()
