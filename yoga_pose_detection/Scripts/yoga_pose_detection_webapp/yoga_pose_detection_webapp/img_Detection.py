import cv2
from time import time
import pickle as pk
import mediapipe as mp
import pandas as pd
import pyttsx4
import multiprocessing as mtp
from . import DBOperations
from . import recommendations  
from . import landmarks  
from . import calc_angles  


def init_cam():
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    cam.set(cv2.CAP_PROP_FOCUS, 360)
    cam.set(cv2.CAP_PROP_BRIGHTNESS, 130)
    cam.set(cv2.CAP_PROP_SHARPNESS, 125)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    return cam


def get_pose_name(index):
    names = {
        0: "Adho Mukha Svanasana",
        1: "Phalakasana",
        2: "Utkata Konasana",
        3: "Vrikshasana",
    }
    return str(names[index])


def init_dicts():
    landmarks_points = {
        "nose": 0,
        "left_shoulder": 11, "right_shoulder": 12,
        "left_elbow": 13, "right_elbow": 14,
        "left_wrist": 15, "right_wrist": 16,
        "left_hip": 23, "right_hip": 24,
        "left_knee": 25, "right_knee": 26,
        "left_ankle": 27, "right_ankle": 28,
        "left_heel": 29, "right_heel": 30,
        "left_foot_index": 31, "right_foot_index": 32,
    }
    landmarks_points_array = {
        "left_shoulder": [], "right_shoulder": [],
        "left_elbow": [], "right_elbow": [],
        "left_wrist": [], "right_wrist": [],
        "left_hip": [], "right_hip": [],
        "left_knee": [], "right_knee": [],
        "left_ankle": [], "right_ankle": [],
        "left_heel": [], "right_heel": [],
        "left_foot_index": [], "right_foot_index": [],
    }
    col_names = []
    for i in range(len(landmarks_points.keys())):
        name = list(landmarks_points.keys())[i]
        col_names.append(name + "_x")
        col_names.append(name + "_y")
        col_names.append(name + "_z")
        col_names.append(name + "_v")
    cols = col_names.copy()
    return cols, landmarks_points_array


engine = pyttsx4.init()


def tts(tts_q):
    while True:
        objects = tts_q.get()
        if objects is None:
            break
        message = objects[0]
        engine.say(message)
        engine.runAndWait()
    tts_q.task_done()


def cv2_put_text(image, message):
    cv2.putText(
        image,
        message,
        (50, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (255, 0, 0),
        5,
        cv2.LINE_AA
    )


def destory(cam, tts_proc, tts_q):
    cv2.destroyAllWindows()
    cam.release()
    tts_q.put(None)
    tts_q.close()
    tts_q.join_thread()
    tts_proc.join()


def pose_prediction(imgpath="NA",imgpath1="NA",id=0,userid="NA"):
    #cam = init_cam()
    try:
        imgoriginal=imgpath
        imgpath="../yoga_pose_detection_webapp/static/Photos/"+imgpath
        imgpath2=imgpath1
        imgpath1="../yoga_pose_detection_webapp/static/Photos/"+imgpath1
        model = pk.load(open("../yoga_pose_detection_webapp/static/models/4_poses.model", "rb"))
        cols, landmarks_points_array = init_dicts()
        angles_df = pd.read_csv("../yoga_pose_detection_webapp/static/csv_files/4_angles_poses_angles.csv")
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose

        tts_q = mtp.JoinableQueue()

        tts_proc = mtp.Process(target=tts, args=(tts_q, ))
        tts_proc.start()

        tts_last_exec = time() + 5

        
            #result, image = cam.read()
        image = cv2.imread(imgpath)
        flipped = cv2.flip(image, 1)
        
        resized_image = cv2.resize(
            flipped,
            (640, 360),
            interpolation=cv2.INTER_AREA
            )
        
        err, df, landmarks1 = landmarks.extract_landmarks(
                resized_image,
                mp_pose,
                cols
            ) 
        print("error="+str(err))
        if err == False:
            prediction = model.predict(df)
            probabilities = model.predict_proba(df)
            print(prediction)
            print(get_pose_name(prediction[0]))
            print(probabilities)
            
            mp_drawing.draw_landmarks(
                flipped,
                landmarks1,
                mp_pose.POSE_CONNECTIONS
            )
            cv2_put_text(
                            flipped,
                            get_pose_name(prediction[0])
                        )
            #cv2.imshow("Frame", flipped)
            #cv2.waitKey()
        print("prob= ")
        print(probabilities[0, prediction[0]])
        if probabilities[0, prediction[0]] >= 0.8:
            cv2_put_text(
            flipped,
            get_pose_name(prediction[0])
            )
            cv2.imwrite(imgpath1,flipped)
            print("suggestions= ")
            angles = calc_angles.rangles(df, landmarks_points_array)
            suggestions = recommendations.check_pose_angle(
            prediction[0], angles, angles_df)
            print("suggestions= ")
            print(suggestions)
            DBOperations.insertPosture(id,userid,get_pose_name(prediction[0]),str(suggestions),imgpath2)
        else:
            DBOperations.insertPosture(id,userid,"No Pose Detected","NA",imgoriginal)
    except Exception:
        DBOperations.insertPosture(id,userid,"No Pose Detected","NA",imgoriginal)

        