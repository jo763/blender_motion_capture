import mediapipe as mp
import cv2
import bpy
import mathutils
import time
# Test
def arm_angle_finder(shoulder, hand):
    x1, y1, z1 = shoulder
    x2, y2, z2 = hand
    tanA = abs((x1-x2)/(y1-y2))
    tanB = abs((y1-y2)/(z1-z2))
    return tanA, tanB

def length_between_points(point1, point2):
    x1, y1, z1 = point1[0], point1[1], point1[2]
    x2, y2, z2 = point2[0], point2[1], point2[2]
    distance = (((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)**0.5)
    return distance

def arm_length_calc(shoulder, elbow, hand):
    upper_arm = length_between_points(shoulder, elbow)
    forearm = length_between_points(elbow, hand)
    upper_arm = 0.14527815580368042
    return upper_arm

def model_dimension_length_calc(shoulder, head):
    pass

def get_arm_model_coords(cam_shoulder, cam_elbow, cam_hand, model_shoulder, model_hand, model_elbow):
    camera_arm_length = arm_length_calc(cam_shoulder, cam_elbow, cam_hand)
    model_arm_length = arm_length_calc(model_shoulder, model_elbow, model_hand)
    try:
        scale_factor = model_arm_length/camera_arm_length
        #print("=" *30)
        #print(f"Scale factor is {scale_factor}")
        #print(f"Camera arm length is {camera_arm_length}")
        #print(f"Model arm length is {model_arm_length}")
        #print(f"Model shoulder position is {model_shoulder}")
        #print(f"Model elbow position is {model_elbow}")
        
    except:
        scale_factor = 0.25
        #print("=" *30)
        #print("Issue calculating scale factor")
    x1, y1, z1 = cam_shoulder[0], cam_shoulder[1], cam_shoulder[2]
    x2, y2, z2 = cam_hand[0], cam_hand[1], cam_hand[2]
    x3, y3, z3 = model_shoulder[0], model_shoulder[1], model_shoulder[2]
    x4 =  ((x2-x1) * scale_factor)
    y4 =  ((y1-y2) * scale_factor)
    z4 =  ((z1-z2) * scale_factor)
    z4 = 0
    return [x4, -.5-y4, .1+z4]

def get_hand_coords(cam_hand, model_hand, cam_finger_tips, model_finger_tips):
    print("+" * 35)
    for i in range(len(cam_finger_tips)):
        try:
            cam_finger_tip = cam_finger_tips[i]
            model_finger_tip = model_finger_tips[i]
            print(cam_finger_tip)
            
            #print(cam_finger_tip)
            #print(model_finger_tip)

            #model_finger_tip_coords = extract_values(landmarks[mp_holistic.PoseLandmark.LEFT_WRIST.value], 0)
            model_finger_tip_coords = extract_values(bpy.data.objects['Armature'].pose.bones[model_finger_tip].location, 0)
            print(f"Model body part: {model_finger_tip}, coords: {model_finger_tip_coords}")

            cam_finger_tip_coords = results.left_hand_landmarks.landmark[cam_finger_tip]
            print(f"Camera body part: {cam_hand_tips_points_desc[i]}, Mediapipe Index: {cam_finger_tip}, coords: {cam_finger_tip_coords}")

        except:
            pass

def extract_values(value, ifCam):
    if ifCam == True:
        listy = [value.y, value.x, value.z]
        pass
    else:
        listy = [value.x, value.y, value.z]
    return listy
#Need to change into strings
cam_hand_tips_points_desc = ['THUMB_TIP', 'INDEX_FINGER_TIP', 'MIDDLE_FINGER_TIP', 'RING_FINGER_TIP', 'PINKY_TIP']
cam_hand_tips_points = [4, 8, 12, 16, 20]
model_hand_tips_L = ['Thumb3.L', 'Pointer3.L', 'Middle3.L', 'Ring3.L', 'Pinky3.L']
model_hand_tips_R = ['Thumb3.R', 'Pointer3.R', 'Middle3.R', 'Ring3.R', 'Pinky3.R']



#obj = bpy.data.armatures['Armature'].bones["handIK.L"]


mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# Drawing specification
mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius = 2)

#mp.drawing.draw_landmarks()
print("Process has started")

# Get realtime webcam feed
cap = cv2.VideoCapture(0)

# initiate holistic model
with mp_holistic.Holistic(min_detection_confidence = 0.5, min_tracking_confidence = 0.5, model_complexity=1) as holistic:

    while cap.isOpened():
        ret, frame = cap.read()

        # Recolour feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Make detections
        results = holistic.process(image)
#        try:
#            print(results)
#        except:
#            print("ree")
        

        # recolor image back to bgr for rendering
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            #landmarks = results.pose_world_landmarks.landmark
        except:
            print("\n============================")
            print("Landmarks tryblock failed")
            print("Rerun program")
            print("============================\n")
            cap.release()
            cv2.destroyAllWindows
            pass
        
        cam_shoulder = extract_values(landmarks[mp_holistic.PoseLandmark.LEFT_SHOULDER.value], 1)
        cam_elbow = extract_values(landmarks[mp_holistic.PoseLandmark.LEFT_ELBOW.value], 1)
        cam_hand = extract_values(landmarks[mp_holistic.PoseLandmark.LEFT_WRIST.value], 1)
        model_shoulder = extract_values(bpy.data.objects['Armature'].pose.bones["coreIK"].location, 0)
        model_elbow = extract_values(bpy.data.objects['Armature'].pose.bones["coreIK"].location, 0)
        model_hand = extract_values(bpy.data.objects['Armature'].pose.bones["handIK.L"].location, 0)
        #print(model_hand, type(model_hand))
        #print("("*30)
        #model_elbow = [3, 3, 3]
        #print(f"Setting model elbow to {model_elbow}")

        
        
        print("="*20)
        list = [cam_shoulder, cam_elbow, cam_hand, model_shoulder, model_elbow, model_hand]
        for item in list:
            #print(item, [item], type([item]))
            #print(item) 
            pass       
        
        
        
        model_hand = get_arm_model_coords(cam_shoulder, cam_elbow, cam_hand, model_shoulder, model_elbow, model_hand)
        
        
        bpy.data.objects['Armature'].pose.bones["handIK.L"].location = model_hand
        print(model_hand)
        #model_hand = [0.168,0.405,0.629]
        
        
        get_hand_coords(cam_hand, model_hand, cam_hand_tips_points ,model_hand_tips_L)
        
        # draw face landmarks
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
        mp_drawing.DrawingSpec(color=(0,0,255), thickness=1, circle_radius = 1),
        mp_drawing.DrawingSpec(color=(0,0,255), thickness=1, circle_radius = 1))

        # right handq
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(255,0,0), thickness=2, circle_radius = 2),
        mp_drawing.DrawingSpec(color=(100,0,0), thickness=2, circle_radius = 2))

        # left hand
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius = 2),
        mp_drawing.DrawingSpec(color=(100,0,0), thickness=2, circle_radius = 2))

        # pose (body + arms+ legs) detection
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(0,0,0), thickness=2, circle_radius = 2),
        mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius = 4))
        
        
        # ========================
        
        

        
        #==================================
        
        
        
        cv2.imshow("Holistic Model Detection", cv2.flip(image, 1))
        boxNewCoord = landmarks[mp_holistic.PoseLandmark.LEFT_WRIST.value].x
        #print(landmarks[mp_holistic.PoseLandmark.LEFT_WRIST.value])
        #print(type(landmarks[mp_holistic.PoseLandmark.LEFT_WRIST.value].x))
        #break
        #boxNewCoord2 = landmarks[mp_holistic.PoseWorldLandmark.LEFT_WRIST.value].x
        #print(boxNewCoord2)
        #boxNewCoord2 = landmarks[mp_holistic.PoseLandmark.RIGHT_WRIST.value].y
        #obj = bpy.data.objects['Armature'].pose.bones["handIK.L"]
        #obj = bpy.data["Blenda-BODY.001"]
        #obj.select = True
        #try:
        #    print(boxNewCoord)
        #    #print(type(boxNewCoord))
        #    if boxNewCoord > 0.5:
        #        print("boxNewCoord")
        #        #obj.rotation_quaternion[2]  = .5
        #        obj.location = [-0.115, -.111, .199]
         #   else:
        #        print("boxNewCoord")
        #        #obj.rotation_quaternion[2]  = -.5
        #        obj.location = [0, 0, 0]
        #except:
         #   pass
        #time.sleep(.05)
        #obj.location.x = -boxNewCoord * 30
        #obj.location.y = boxNewCoord2 * 30
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
        if cv2.waitKey(10) & 0xff == ord('q'):
            break
#for x in mp_holistic.PoseLandmark:
#    print(x)

#print(landmarks[mp_holistic.PoseLandmark.RIGHT_WRIST.value])
cap.release()
cv2.destroyAllWindows

