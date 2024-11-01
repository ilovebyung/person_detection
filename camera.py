import cv2

# Open the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam opened successfully
if not cap.isOpened():
    print("Error opening video stream")
    exit()

# Read a frame from the webcam
ret, frame = cap.read()

# If a frame was read successfully, print its size
if ret:
    height, width, channels = frame.shape
    print("Frame size:", width, "x", height)
else:
    print("Error reading frame from camera")


def categorize_position(h, w):

  if h < (height//5):
    size = "s"
  elif h < (height//5) * 2:
    size = "m"
  else:
    size = "l"

  if w < (width//2):
    direction = "L"
  else:
    direction = "R"

  return size, direction


if __name__ == '__main__':
    # Example usage:
    LR = 3
    LB = 5
    RR = 8
    RB = 10

    h,w = 120, 390

    size, direction = categorize_position(h, w)
    print(f"The size is categorized as: {size}")
    print(f"The direction is categorized as: {direction}")

