import cv2
import os
import numpy as np
import pytesseract

# Set the path to the Tesseract executable (replace with your own path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Create a directory to save captured images
if not os.path.exists('captured_images'):
    os.makedirs('captured_images')

# Open the webcam (usually, 0 is the default camera)
cap = cv2.VideoCapture(0)

# Resize factor for the displayed frame
resize_factor = 0.5  # Adjust this value as needed

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Resize the frame
    height, width = frame.shape[:2]
    frame = cv2.resize(frame, (int(width * resize_factor), int(height * resize_factor)))

    # Display the resized frame
    cv2.imshow('Webcam Feed', frame)

    # Wait for the user to press the Enter key
    key = cv2.waitKey(1)
    if key == 13:  # 13 is the ASCII code for Enter
        # Save the current frame as an image
        image_filename = os.path.join('captured_images', 'captured_frame.png')
        cv2.imwrite(image_filename, frame)
        print(f"Captured image saved as {image_filename}")

        # Apply image preprocessing
        captured_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, captured_frame_threshold = cv2.threshold(captured_frame_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Extract text from the captured frame with English language specification
        text = pytesseract.image_to_string(captured_frame_threshold, lang='eng')
        print("Extracted Text:", text)

    # Break the loop when the 'q' key is pressed
    elif key & 0xFF == ord('q'):
        break

# Release the webcam and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
