import cv2
import numpy as np
import streamlit as st
from PIL import Image

# Dictionaries for character encoding
d = {chr(i): i for i in range(225)}
c = {i: chr(i) for i in range(225)}

def encrypt_message(image, msg):
    img = np.array(image)
    n, m, z = 0, 0, 0
    for i in range(len(msg)):
        img[n, m, z] = d[msg[i]]
        n += 1
        m += 1
        z = (z + 1) % 3
    return Image.fromarray(img)

def decrypt_message(image, length):
    img = np.array(image)
    n, m, z = 0, 0, 0
    message = ""
    try:
        for i in range(length):
            message += c[img[n, m, z]]
            n += 1
            m += 1
            z = (z + 1) % 3
    except KeyError:
        return "Decryption failed."
    return message

st.title("Steganography Tool")

uploaded_file = st.file_uploader("pool.jpg", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    option = st.radio("Choose an action", ("Encrypt", "Decrypt"))
    
    if option == "Encrypt":
        msg = st.text_input("Enter Secret Message")
        passcode = st.text_input("Enter Passcode", type="password")
        if st.button("Encrypt and Save"):
            encrypted_image = encrypt_message(image, msg)
            encrypted_image.save("encryptedImage.png")
            st.success("Message encrypted successfully!")
            st.image(encrypted_image, caption="Encrypted Image", use_column_width=True)
    
    if option == "Decrypt":
        passcode = st.text_input("Enter Passcode", type="password")
        if st.button("Decrypt Message"):
            correct_pass = "SECURED"
            if passcode == correct_pass:
                length = st.number_input("Enter Message Length", min_value=5, step=1)
                decrypted_msg = decrypt_message(image, length)
                st.success(f"Decrypted Message: {decrypted_msg}")
            else:
                st.error("Incorrect passcode. Decryption failed.")
