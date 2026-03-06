import cv2
import threading
import queue

class CameraController:
    def __init__(self):
        self.cap = None
        self.running = False
        self.command_queue = queue.Queue()
        self.thread = None
        self.photo_event = threading.Event()  # Event to signal photo capture completion

    def _camera_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                # Display the camera feed in a window
                cv2.imshow("Camera Feed", frame)

                # Check for commands in the queue
                try:
                    command = self.command_queue.get_nowait()
                    if command[0] == "take_photo":
                        filepath = command[1]
                        cv2.imwrite(filepath, frame)
                        self.photo_event.set()  # Signal that the photo has been saved
                    elif command[0] == "quit":
                        break
                except queue.Empty:
                    pass

                # Close the camera feed window on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.quit_camera()
            else:
                print("Failed to capture frame.")

        # Close the OpenCV window when done
        cv2.destroyAllWindows()

    def open_camera(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise RuntimeError("Failed to open camera.")
            self.running = True
            self.thread = threading.Thread(target=self._camera_loop)
            self.thread.start()
            print("Camera opened.")

    def take_photo(self, save_path):
        if self.running:
            self.photo_event.clear()  # Reset the event
            self.command_queue.put(("take_photo", save_path))
            self.photo_event.wait()  # Wait until the photo is captured
        else:
            raise RuntimeError("Camera is not running.")

    def quit_camera(self):
        if self.running:
            self.command_queue.put(("quit",))
            self.thread.join()
            self.cap.release()
            self.running = False
            print("Camera closed.")
