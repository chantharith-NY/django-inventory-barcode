import cv2
from pyzbar import pyzbar

def scan_barcode():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type
            print(f"Found {barcode_type} barcode: {barcode_data}")
            return barcode_data

        cv2.imshow('Barcode Scanner', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_barcode()