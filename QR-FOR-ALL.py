import tkinter as tk
from tkinter import ttk
import qrcode
from PIL import Image, ImageTk
import cv2
import pyperclip
from io import BytesIO

def generate_qr_code():
    text = qr_text.get("1.0", "end-1c")
    if text:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img = qr_img.resize((200, 200))
        tk_qr_img = ImageTk.PhotoImage(qr_img)
        qr_code_label.config(image=tk_qr_img)
        qr_code_label.photo = tk_qr_img

        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        qr_code_image_data = buffer.getvalue()
        buffer.close()

        download_button.qr_code_data = qr_code_image_data

def download_qr_code():
    qr_code_data = download_button.qr_code_data
    if qr_code_data:
        with open("generated_qr_code.png", "wb") as f:
            f.write(qr_code_data)

def copy_decoded_text():
    decoded_data = decoded_text.get("1.0", "end-1c")
    if decoded_data:
        pyperclip.copy(decoded_data)

def decode_qr_code():
    image_path = decode_text.get("1.0", "end-1c")
    if image_path:
        image = cv2.imread(image_path)
        detector = cv2.QRCodeDetector()
        val, pts, qr_code = detector.detectAndDecode(image)
        decoded_text.delete("1.0", "end")
        decoded_text.insert("1.0", val)

def clear_inputs_outputs():
    qr_text.delete("1.0", "end-1c")
    decode_text.delete("1.0", "end-1c")
    
    qr_code_label.config(image=None)
    decoded_text.delete("1.0", "end")

window = tk.Tk()
window.title("QR Code Generator and Decoder")

tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Generate QR Code")
tab_control.add(tab2, text="Decode QR Code")
tab_control.pack(expand=1, fill="both")

# Tab 1 - Generate QR Code
qr_text_label = tk.Label(tab1, text="Enter text for QR Code:")
qr_text_label.pack(pady=10)
qr_text = tk.Text(tab1, height=5, width=40)
qr_text.pack(pady=5)
generate_button = tk.Button(tab1, text="Generate QR Code", command=generate_qr_code)
generate_button.pack(pady=10)
qr_code_label = tk.Label(tab1)
qr_code_label.pack()
download_button = tk.Button(tab1, text="Download QR Code", command=download_qr_code)
download_button.pack(pady=10)

# Tab 2 - Decode QR Code
decode_label = tk.Label(tab2, text="Enter the path to the QR Code image:")
decode_label.pack(pady=10)
decode_text = tk.Text(tab2, height=5, width=40)
decode_text.pack(pady=5)
decode_button = tk.Button(tab2, text="Decode QR Code", command=decode_qr_code)
decode_button.pack(pady=10)
decoded_text = tk.Text(tab2, height=5, width=40)
decoded_text.pack()
copy_button = tk.Button(tab2, text="Copy Decoded Text", command=copy_decoded_text)
copy_button.pack(pady=10)

# Add a "Clear" button to both tabs
clear_button_tab1 = tk.Button(tab1, text="Clear", command=clear_inputs_outputs)
clear_button_tab1.pack(pady=10)
clear_button_tab2 = tk.Button(tab2, text="Clear", command=clear_inputs_outputs)
clear_button_tab2.pack(pady=10)

window.mainloop()
