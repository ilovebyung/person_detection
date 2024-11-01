from ultralytics import YOLO
import threading
import camera
import alarm

# Load the exported NCNN model
model = YOLO("yolo11n_ncnn_model")

while True:
    # Read a frame from the webcam
    ret, frame = camera.cap.read()
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect objects in the frame
    result = model(frame)[0]

    # Loop through the detected objects
    for box in result.boxes:
        # Extract the bounding box coordinates and class ID
        class_id = result.names[box.cls[0].item()]
        cords = box.xyxy[0].tolist()
        x1, y1, x2, y2 = [round(x) for x in cords]
        print(class_id, x1, y1)

        # Check if the detected object is a person
        if class_id == 'person':  # 0 is the class ID for 'person' in the COCO dataset
            # Draw a bounding box around the person
            camera.cv2.rectangle(frame, (int(x1), int(y1)),(int(x2), int(y2)), (0, 0, 255), 10)

            # Get the position
            h = int(y2-y1)
            size, side = camera.categorize_position(h, x1)
            seconds = 0.1

            try:

                if size == 'l' or size == 'm':
                    sound_arg = (size,seconds,)
                    t1 = threading.Thread(target=alarm.sound_alarm, args=sound_arg)
                    # alarm.sound_alarm(size, seconds)

                    if side == 'L':
                        light_arg = (alarm.LR,0.1,)
                        t2 = threading.Thread(target=alarm.turn_on_led, args=light_arg)
                        # alarm.turn_on_led(alarm.LR,0.1)
                    else:
                        light_arg = (alarm.RR,0.1,)
                        t2 = threading.Thread(target=alarm.turn_on_led, args=light_arg)
                        # alarm.turn_on_led(alarm.RR,0.1)
                else:
                    alarm.turn_off_led()

                # Start the threads
                t1.start()
                t2.start()

                # Wait for both threads to finish   

                t1.join()
                t2.join()
                
            except Exception as e:
                if "threads can only be started once" not in str(e):
                    print(f"Error playing sound: {str(e)}")

    # Display the frame with bounding boxes
    camera.cv2.imshow('Person Detection', frame)

    # Break the loop if 'q' is pressed
    if camera.cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and video writer objects
camera.cap.release()
# Close all open windows
camera.cv2.destroyAllWindows()

