from flet import *
import flet as ft
import cv2
import numpy as np
import base64
import time
import os
from models.facenet_tensorflow import Facenet

cap = cv2.VideoCapture(0)
deb_capt = False
FN = Facenet()

def main(page:Page):
    page.update()

    # Current Frame
    captured_frame = ft.Image(
        src="placeholder.jpg",
        width=640,
        height=360,
        fit=ft.ImageFit.CONTAIN
    )

    # Iterating Capture Frames
    def capture_frame():
        cap = cv2.VideoCapture(0)
        clear_button.disabled = True
        capture_button.disabled = False
        update_database_button.disabled = False
        page.update()
        try:
            while True:
                ret,frame = cap.read()
                if ret:
                    _, buffer = cv2.imencode('.png', frame)
                    png_as_text = base64.b64encode(buffer).decode('utf-8') 
                    captured_frame.src_base64 = png_as_text
                    captured_frame.update()
                    if deb_capt:
                        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        _, buffer = cv2.imencode('.png', gray_frame)
                        png_as_text = base64.b64encode(buffer).decode('utf-8') 
                        captured_frame.src_base64 = png_as_text
                        captured_frame.update()
                        break
        except Exception as e:
            print(f"Error: {e}")

    # Capture Frames
    def trigger_capture(e):
        global deb_capt
        src_base64_img = captured_frame.src_base64
        if (src_base64_img is not None):
            deb_capt = True
            capture_button.disabled = True
            update_database_button.disabled = True
            clear_button.disabled = True
            page.update()
            if src_base64_img.startswith('data:image'):
                src_base64_img = src_base64_img.split(',')[1]
            img_data = base64.b64decode(src_base64_img)
            np_img = np.frombuffer(img_data, dtype=np.uint8)
            conv_img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
            cv2.imwrite('set_input/capture.png', conv_img)
            print("capture!")
            FN.run_recognition()
            print("finish capturing")
            show_result()

    def show_result():
        if os.path.exists("set_output/capture_recognition.png"):
            captured_frame.src = "set_output/capture_recognition.png"
            captured_frame.src_base64 = None
        capture_button.disabled = True
        update_database_button.disabled = True
        clear_button.disabled = False
        captured_frame.update()
        page.update()

    def modify_database(e):
        capture_button.disabled = True
        update_database_button.disabled = True
        page.update()
        os.remove("known_embeddings.pkl")
        os.remove("known_labels.pkl")
        FN.process_database()
        print("finish updating database")
        capture_button.disabled = False
        update_database_button.disabled = False
        page.update()

    def clear(e):
        global deb_capt
        captured_frame.src = "placeholder.jpg"
        captured_frame.src_base64 = None
        clear_button.disabled = True
        page.update()
        deb_capt = False
        capture_frame()

    # COMPONENTS
    capture_button = ft.ElevatedButton("Recognize Face", on_click=trigger_capture, disabled=True)
    update_database_button = ft.ElevatedButton("Update Database", on_click=modify_database, disabled=True)
    clear_button = ft.ElevatedButton("Clear", on_click=clear, disabled=True)
    
    control_rack = ft.Row([capture_button, update_database_button, clear_button], alignment=ft.MainAxisAlignment.CENTER)    

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.add(captured_frame, control_rack)
    capture_frame()

ft.app(target=main)