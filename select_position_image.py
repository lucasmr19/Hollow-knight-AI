import cv2

# Cargar la imagen
image_path = "img_2.png"  # Ruta a la imagen subida
image = cv2.imread(image_path)

# show image
def select_region(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, selecting

    if event == cv2.EVENT_LBUTTONDOWN:  # selection
        x_start, y_start = x, y
        selecting = True

    elif event == cv2.EVENT_MOUSEMOVE and selecting:  # while selection
        x_end, y_end = x, y
        temp_image = image.copy()
        cv2.rectangle(temp_image, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
        cv2.imshow("Select Health Bar Region", temp_image)

    elif event == cv2.EVENT_LBUTTONUP:  # Finish selection
        x_end, y_end = x, y
        selecting = False
        print(f"Selected region: x_min={x_start}, y_min={y_start}, x_max={x_end}, y_max={y_end}")

# global variables
x_start, y_start, x_end, y_end = 0, 0, 0, 0
selecting = False

# show window to select region
cv2.imshow("Select Health Bar Region", image)
cv2.setMouseCallback("Select Health Bar Region", select_region)
cv2.waitKey(0)
cv2.destroyAllWindows()
