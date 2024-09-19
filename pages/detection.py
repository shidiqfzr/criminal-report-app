import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import json
from urllib.request import urlopen
import mysql.connector
import streamlit as st


connect = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Shubuh28Mei2003',
    database='criminal'
)

class CriminalDetector:
    def __init__(self, path):
        self.__path = path
        self.__images = []
        self.__criminal_names = []
        self.__encodings = []
        self.__load_images()
    
    def __load_images(self):
        criminal_list = os.listdir(self.__path)
        for name in criminal_list:
            cur_img = cv2.imread(f'{self.__path}/{name}')
            self.__images.append(cur_img)
            self.__criminal_names.append(os.path.splitext(name)[0])
        
        self.__encodings = self.__find_encodings(self.__images)
    
    def __find_encodings(self, images):
        encode_list = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encode_list.append(encode)
        return encode_list
    
    def __mark_detect(self, name):
        cursor = connect.cursor()
        query = "SELECT * FROM criminal_detection WHERE name = %s"
        cursor.execute(query, (name,))
        result = cursor.fetchall()

        if not result:
            now = datetime.now()
            date = now.strftime('%Y-%m-%d')
            time = now.strftime('%H:%M:%S')

            url = 'http://ipinfo.io/json'
            response = urlopen(url)
            data = json.load(response)
            country = data.get('country', '')
            region = data.get('region', '')
            city = data.get('city', '')
            coordinates = data.get('loc', '')

            insert_query = "INSERT INTO criminal_detection (name, date, time, country, region, city, coordinates) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            insert_values = (name, date, time, country, region, city, coordinates)
            cursor.execute(insert_query, insert_values)
            connect.commit()

        else:
            # If the person is found in the database, update the date, time, country, state, city, and coordinates
            now = datetime.now()
            date = now.strftime('%Y-%m-%d')
            time = now.strftime('%H:%M:%S')
            url = 'http://ipinfo.io/json'
            response = urlopen(url)
            data = json.load(response)
            country = data.get('country', '')
            region = data.get('region', '')
            city = data.get('city', '')
            coordinates = data.get('loc', '')

            update_query = "UPDATE criminal_detection SET date = %s, time = %s, country = %s, region = %s, city = %s, coordinates = %s WHERE name = %s"
            update_values = (date, time, country, region, city, coordinates, name)
            cursor.execute(update_query, update_values)
            connect.commit()

        cursor.close()

    def detect_criminals(self):
        FRAME_WINDOW = st.image([])
        cap = cv2.VideoCapture(1)
        while True:
            success, img = cap.read()
            img_cam = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            img_cam = cv2.cvtColor(img_cam, cv2.COLOR_BGR2RGB) 

            faces_cur_frame = face_recognition.face_locations(img_cam) 
            encodes_cur_frame = face_recognition.face_encodings(img_cam, faces_cur_frame)

            for encode_face, face_loc in zip(encodes_cur_frame, faces_cur_frame):
                matches = face_recognition.compare_faces(self.__encodings, encode_face)
                face_dis = face_recognition.face_distance(self.__encodings, encode_face)
                match_index = np.argmin(face_dis)


                if matches[match_index]:
                    name_match = self.__criminal_names[match_index].upper()
                    accuracy = (1 - face_dis[match_index]) * 100
                    y1, x2, y2, x1 = face_loc
                    y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f"{name_match} ({accuracy:.2f}%)", (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    self.__mark_detect(name_match)
                
                else:
                    y1, x2, y2, x1 = face_loc
                    y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "UNKNOWN", (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            FRAME_WINDOW.image(img)

            cv2.imshow("Webcam", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
           
        
        cap.release()
        cv2.destroyAllWindows()