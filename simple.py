import cv2


image = cv2.imread("src/coffee.jpg")


def view_image(_name_of_window, _image):
    cv2.namedWindow(_name_of_window, cv2.WINDOW_NORMAL)
    cv2.imshow(_name_of_window, _image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


cropped = image[240:740, 320:820]
# view_image("Image", cropped)

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, threshold_image = cv2.threshold(gray_image, 127, 255, 0)
# view_image("Пёсик в градациях серого", gray_image)
view_image("Чёрно-белый пёсик", threshold_image)
