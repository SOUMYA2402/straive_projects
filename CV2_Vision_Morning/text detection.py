import cv2
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
image_path='ocr_text.png'
image=cv2.imread(image_path)

if image is None:
    print("Error: Could Not load")
else:
    gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

pil_img=Image.fromarray(gray)
text=pytesseract.image_to_string(pil_img)
print("Extracted Text:\n", text)

cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
