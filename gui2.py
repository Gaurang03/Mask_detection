import tkinter as tk
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from PIL import Image, ImageTk
import random
import pandas as pd
import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pygame
import math

root = tk.Tk()

canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=3, rowspan=3)

logo = Image.open('logo1.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(columnspan=3, column=0, row=1)

welcome = tk.Label(
    root, text="Welcome to the \n E-Challan Generation System for Non-Mask People.", font="Raleway")
welcome.grid(columnspan=3, column=0, row=2, padx=20, pady=20)


def myclick():

    # path of images
    path = 'images'
    images = []
    personnames = []

    mylist = os.listdir(path)
    print(mylist)
    for cu_img in mylist:
        current_img = cv2.imread(f'{path}/{cu_img}')
        images.append(current_img)
        personnames.append(os.path.splitext(cu_img)[0])

    print(personnames)

# general function for finding the 128 dimension(encoding) of every picture

    def faceencodings(image):
        encodelist = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodelist.append(encode)
        return encodelist

    encodelistknown = faceencodings(images)
    print('All Encodings Complete!!!')

    # general function for storing name and date and time of the detected person

    def defaluter(emp_name):
        with open('defaulters.csv', 'r+') as f:
            mydatalist = f.readlines()
            namelist = []
            for line in mydatalist:
                entry = line.split(',')
                namelist.append(entry[0])

            if emp_name not in namelist:
                time_now = datetime.now()
                tstr = time_now.strftime('%H:%M:%S')
                dstr = time_now.strftime('%d/%m/%Y')
                amount = 'Rs.500'
                challan = random.randint(0, 1000000000)
                f.writelines(f'{name},{tstr},{dstr},{amount},{challan}\n')

    # opening the camera window and matching the encoding of the new person with the encodings generated from the images

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

        facescurrentframe = face_recognition.face_locations(faces)
        encodescurrentframe = face_recognition.face_encodings(
            faces, facescurrentframe)

        for encodeFace, faceLoc in zip(encodescurrentframe, facescurrentframe):
            matches = face_recognition.compare_faces(
                encodelistknown, encodeFace)
            facedis = face_recognition.face_distance(
                encodelistknown, encodeFace)
            # print(faceDis)
            matchindex = np.argmin(facedis)

            if matches[matchindex]:
                name = personnames[matchindex].upper()
                # print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2),
                              (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                defaluter(name)

        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) == 13:
            break

    cap.release()
    cv2.destroyAllWindows()


def defaulter_list():
    with open('defaulters.csv', 'r+') as file:
        reader = pd.read_csv(file, sep=',')
        # print(reader)

        # text box
        textbox = tk.Text(root, height=10, width=80, padx=5, pady=5)
        textbox.insert(1.0, reader)
        textbox.grid(column=1, row=7)


def email_sending():

    email_sender = "nomask.challan@gmail.com"
    password = "LaLaLand@2021"
    subject = "E-challan For Not Wearing Mask"

    with open('defaulters.csv', 'r+') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            text = "Hello " + line[0] + "\n" + "This is you inform you that you have been caught without mask at " + line[2] + " on " + line[2] + "\n" + \
                "You are requested to pay the fine of " + \
                line[3] + "\n" + "Your challan number is:- " + line[4] + "\n \n" + \
                "Thank You!" + "\n" + "Regards" + "\n" + "No-Mask Challan \n"
            # print(text)
            email_send = line[0]
            msg = MIMEMultipart()
            msg['From'] = email_sender
            msg['To'] = email_send
            msg['Subject'] = subject
            msg.attach(MIMEText(text))
            text = msg.as_string()

            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(email_sender, password)
            server.sendmail(email_sender, email_send, text)

            server.quit()


def mask_the_corona():

    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    background = pygame.image.load("bg.jpg")

    pygame.display.set_caption("Mask the Corona")
    icon = pygame.image.load('doctor.png')
    pygame.display.set_icon(icon)

    playerImg = pygame.image.load("player.png")
    playerX = 370
    playerY = 480
    playerX_change = 0

    enemy_1_Img = []
    enemy_1_X = []
    enemy_1_Y = []
    enemy_1_X_change = []
    enemy_1_Y_change = []
    num_of_enemies = 6

    for i in range(num_of_enemies):

        enemy_1_Img.append(pygame.image.load("enemy_2.png"))
        enemy_1_X.append(random.randint(0, 735))
        enemy_1_Y.append(random.randint(0, 100))
        enemy_1_X_change.append(1)
        enemy_1_Y_change.append(40)

    maskImg = pygame.image.load("mask.png")
    maskX = 0
    maskY = 480
    maskX_change = 0
    maskY_change = 1
    mask_state = "ready"

    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    textX = 390
    textY = 10

    gameover_font = pygame.font.Font('freesansbold.ttf', 32)

    def gameover_text():
        over_text = gameover_font.render(
            "Gaame Over", True, (255, 255, 255))
        screen.blit(over_text, (200, 250))

    def score(x, y):
        score = font.render("Score: " + str(score_value),
                            True, (255, 255, 255))
        screen.blit(score, (x, y))

    def fire(x, y):
        global mask_state
        mask_state = "fire"
        screen.blit(maskImg, (x+30, y + 20))

    def player(x, y):
        screen.blit(playerImg, (x, y))

    def enemy_1(x, y, i):
        screen.blit(enemy_1_Img[i], (x, y))

    def collision(enemy_1_X, enemy_1_Y, maskX, maskY):
        distance = math.sqrt((math.pow(enemy_1_X-maskX, 2)) +
                             (math.pow(enemy_1_Y-maskY, 2)))
        if distance < 27:
            return True
        else:
            return False

    running = True
    while running:
        screen.fill((255, 0, 0))
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.5
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RIGHT:
                    playerX_change = 0.5
                if event.key == pygame.K_SPACE:
                    if mask_state is "ready":
                        maskX = playerX
                        fire(maskX, maskY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 700:
            playerX = 700

        for i in range(num_of_enemies):

            if enemy_1_Y[i] > 440:
                for j in range(num_of_enemies):
                    enemy_1_Y[j] = 2000
                gameover_text()
                break

            enemy_1_X[i] += enemy_1_X_change[i]

            if enemy_1_X[i] <= 0:
                enemy_1_X_change[i] = 1
                enemy_1_Y[i] += enemy_1_Y_change[i]
            elif enemy_1_X[i] >= 736:
                enemy_1_X_change[i] = -1
                enemy_1_Y[i] += enemy_1_Y_change[i]

            iscollision = collision(enemy_1_X[i], enemy_1_Y[i], maskX, maskY)
            if iscollision:
                maskY = 480
                mask_state = "ready"
                score_value += 1
                enemy_1_X[i] = random.randint(0, 735)
                enemy_1_Y[i] = random.randint(0, 100)

            enemy_1(enemy_1_X[i], enemy_1_Y[i], i)

        if maskY <= 0:
            maskY = 480
            mask_state = "ready"

        if mask_state is "fire":
            fire(maskX, maskY)
            maskY -= maskY_change

        player(playerX, playerY)
        score(textX, textY)
        pygame.display.update()


myButton = tk.Button(root, text="Start Scanning", command=myclick,
                     fg="White", bg="#e192ba", height=5, width=30)
myButton.grid(column=1, row=3)

myButton1 = tk.Button(root, text="See Defaulters", command=defaulter_list,
                      fg="White", bg="#e192ba", height=5, width=30)
myButton1.grid(column=1, row=4)

myButton2 = tk.Button(root, text="Send Email", command=email_sending,
                      fg="White", bg="#e192ba", height=5, width=30)
myButton2.grid(column=1, row=5)

myButton3 = tk.Button(root, text="Mask The Corona", command=mask_the_corona,
                      fg="White", bg="#e192ba", height=5, width=30)
myButton3.grid(column=1, row=6)

canvas = tk.Canvas(root, width=600, height=100)
canvas.grid(columnspan=3)


root.mainloop()
