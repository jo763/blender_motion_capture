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
    forearm = length_between_points(shoulder, hand)
    return upper_arm + forearm

def model_dimension_length_calc(shoulder, head):
    pass

def get_arm_model_coords(cam_shoulder, cam_elbow, cam_hand, model_shoulder, model_hand, model_elbow):
    camera_arm_length = arm_length_calc(cam_shoulder, cam_elbow, cam_hand)
    model_arm_length = arm_length_calc(model_shoulder, model_elbow, model_hand)
    scale_factor = camera_arm_length/model_arm_length
    print(scale_factor)
    x1, y1, z1 = cam_shoulder[0], cam_shoulder[1], cam_shoulder[2]
    x2, y2, z2 = cam_hand[0], cam_hand[1], cam_hand[2]
    x3, y3, z3 = model_shoulder[0], model_shoulder[1], model_shoulder[2]
    x4 = x3 + abs((x2-x1) * scale_factor)
    y4 = y3 + abs((y1-y2) * scale_factor)
    z4 = z3 + abs((z1-z2) * scale_factor)
    return x4, y4, z4

    #angleXY, angleYZ = arm_angle_finder(cam_shoulder, cam_hand)


def ree(value):
    return (value[0], value[1], value[2])

x = get_arm_model_coords([0,0,0], [.5,.5,.5], [.25,.25,.25], [1,1,1], [2,2,2], [3,3,3])
print(x)
