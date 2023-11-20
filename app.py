#importing flask and its packages
from flask import Flask, render_template, Response, redirect, url_for, jsonify, request
import cv2
import face_recognition

app = Flask(__name__)

#load a image from given image
#face encoding function is used to generate facial endoing 
#[0] is used to recognize first person in the picture
vanshika_image = face_recognition.load_image_file("tutorials/vanshika .jpg")
vanshika_encoding = face_recognition.face_encodings(vanshika_image)[0]

# to check if the user is identified or  not
user_identified = False

# Open the camera , 0 is used for default camera or we can use 1 for any secondary camera
video_capture = cv2.VideoCapture(0)

#generate the frames and user_identified is used for identification status 
def generate_frames():
    global user_identified  

    while True:
        #.read function capture the single function from the videocapture
        # ret will contain a boolean value indicating the success of the frame capture
        # frame will contain the image data if the capture was successful.
        ret, frame = video_capture.read()

        # .face_locations detect face locations within the frame
        # .face_encoding function generates the numerical encoding of the faces from frames and the face_encoding
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        user_identified = False  # Reset the flag for each frame

        for face_encoding in face_encodings:
            # comparing the facial and the known encoding
            matches = face_recognition.compare_faces([vanshika_encoding], face_encoding)

            if True in matches:    # out of the loop when matches
                user_identified = True
                break  

        # Draw rectangles and names on the frame
        # (0,255,255) is the yellow color in BGR format 
        # 2 is the thickness of the rectangle
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 2)

        # Convert the frame to JPG format
        #tobytes encodeimage data into bytes and overwritesin frame
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')

#  user validation
user_validation = {
    "Email ID": "vanshika123@gmail.com",
    "password": "vanshika123"
}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    Email_ID = request.form['Email ID']
    password = request.form['password']

    if Email_ID == user_validation['Email ID'] and password == user_validation['password']:
        return redirect(url_for('face_recogination_file'))
    else:
        return render_template('login.html', error='invalid ')

@app.route('/face_recogination_file')
def face_recogination_file():
    return render_template('face_recogination_file.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/check_identification')
def check_identification():
    global user_identified  # Make sure to use the global variable

    return jsonify({'user_identified': user_identified})

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(debug=True)
                
