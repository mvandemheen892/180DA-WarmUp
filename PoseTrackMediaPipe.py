import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic
mp_pose = mp.solutions.pose

prevwristx=0
prevwristy=0

previousGuesss=np.zeros(7)
potentialGuess=['other','right','left']



# For webcam input:
cap = cv2.VideoCapture(0)
with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue


    width  = cap.get(3)  # float `width`
    height = cap.get(4) 
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = holistic.process(image)

    # Draw landmark annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_holistic.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles
        .get_default_pose_landmarks_style())

    wrist = results.pose_landmarks.landmark[16]
    wristx=int(wrist.x*width)
    wristy=int(wrist.y*height)
    
    #velocity in pixels per frame
    velox=wristx-prevwristx
    veloy=wristy-prevwristy
    velomag=np.sqrt(velox*velox+veloy*veloy)

    #plot velo arrow
    start_point=(wristx,wristy)
    end_point=(int(wristx+(velox)),int(wristy+(veloy)))
    if end_point[0]<width and end_point[1]<height:
        image = cv2.arrowedLine(image, start_point, end_point,(0, 255, 0), 9) 


    prevwristx=wristx
    prevwristy=wristy

    if velox < -30 and abs(veloy) < 20:
        cv2.putText(image,"Right",(100,100),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
    elif velox > 30 and abs(veloy) < 20:
        cv2.putText(image,"Left",(100,100),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
    else:
        cv2.putText(image,"Other",(100,100),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
    flippedimage =cv2.flip(image, 1)
    cv2.putText(image,str(velox),(wristx,wristy -1),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Holistic', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()