import cv2
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
camera = cv2.VideoCapture('3831765-uhd_2160_4096_25fps.mp4')

while True:
    ret, frame= camera.read()
    if not ret:
        break

    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _,thresholded = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    text=pytesseract.image_to_string(Image.fromarray(thresholded),config='--psm 11').strip()

    if text:
        print("Detected Text: \n",text)
        cv2.imshow("OCR",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


camera.release()
cv2.destroyAllWindows()
