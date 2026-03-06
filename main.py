import faceRec
from capturePhoto import CameraController
import datetime 
import serialCommunication as sc

# Main Program
port = 'COM3'
baudrate = 9600
timeout = 1

# Open serial connection once
serial_connection = sc.open_serial_connection(port, baudrate, timeout)
faces = faceRec.load_faces_from_folder("knownFaces")
cam_controller = CameraController()

try:
    while True:
        command = sc.receive_data(serial_connection)
        if command == 'c':
            cam_controller.open_camera()

            while True: 
                letter = sc.receive_data(serial_connection)

                if letter == 'd':
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    captured_photo = f'testedFaces/{timestamp}.jpg'
                    cam_controller.take_photo(captured_photo)
                    results = faceRec.compare_face_with_embeddings(faces, captured_photo)
                    
                    if not results:
                        print("No faces detected or no results available.")
                        sc.send_data(serial_connection, 'b') 
                    else:
                        best_match = min(results.items(), key=lambda x: x[1]['distance'])
                        file_name, result = best_match

                        if result['match']:
                            print(f"Best Match: {file_name} -> Distance: {result['distance']:.2f}")
                            sc.send_data(serial_connection, 'a')
                        else:
                            print("No match found.")
                            sc.send_data(serial_connection, 'b')
                else:
                    cam_controller.quit_camera()
                    break
        else:
            cam_controller.quit_camera()
                
except KeyboardInterrupt:
    print("\nExiting program.")

finally:
    sc.close_serial_connection(serial_connection)
