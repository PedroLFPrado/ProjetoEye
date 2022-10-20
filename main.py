from turtle import width
import cv2
import numpy as np
import dlib
from math import hypot
import csv




#inicializar video e quadro
cap = cv2.VideoCapture(0)
board = np.zeros((500, 1400), np.uint8) #quadro do teclado padrão
board[:] = 255

board2 = np.zeros((500, 1400), np.uint8) #quadro de frases salvas
board2[:] = 255 


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


#Teclado
keyboard = np.zeros((600, 1000, 3), np.uint8)
keys_set_1 = {0 : "A", 1: "B", 2: "C", 3: "D", 4: "E", 
                5: "F", 6: "G", 7: "H", 8: "I", 9: "J", 
                10: "K", 11: "L", 12: "M", 13: "N", 14: "<"}
keys_set_2 = {0 : "O", 1: "P", 2: "Q", 3: "R", 4: "S", 
                5: "T", 6: "U", 7: "V", 8: "W", 9: "X", 
                10: "Y", 11: "Z", 12: "_", 13: "<", 14: "<<"}

emotes_set = {0 : ":)", 1: ":(", 2: "Cold", 3: "Hot", 4: "Sick", 
                5: ">:(", 6: ":S", 7: "Hurt", 8: "ZZZ", 9: ":/", 
                10: "Food", 11: ":<", 12: "W.C", 13: ":O", 14: "<"}

emotes_phrases = {0 : "I'm Happy", 1: "I'm Sad", 2: "It's Cold Here", 3: "It's Hot Here", 4: "I'm Feeling Sick", 
                5: "I'm Angry", 6: "I'm Confused", 7: "I'm In Pain", 8: "I Gotta Sleep", 9: "I'm Bored", 
                10: "I'm Hungry", 11: "I'm Stressed", 12: "I Gotta Use The Bathroom", 13: "I'm Surprised!", 14: "<"}

phrases = {0 : "", 1: "", 2: "", 3: "", 4: "", 
                5: ""}

font = cv2.FONT_HERSHEY_DUPLEX

def letter(letter_index, text, letter_light):
    #Teclas
    if letter_index <= 4:
        x = letter_index*200
        y = 0
    elif 4 < letter_index <= 9:
        x = (letter_index-5)*200
        y = 200
    elif 9 < letter_index <= 14:
        x = (letter_index-10)*200
        y = 400

    width = 200
    height = 200
    th = 3 #thickness
   # Cfg Texto
    font_scale = 5
    font_th = 8
    text_size = cv2.getTextSize(text, font, font_scale, font_th)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x
    text_y = int((height + height_text) / 2) + y

    if letter_light is True:
        cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (245, 239, 230), 2)
        cv2.putText(keyboard, text, (text_x, text_y), font, font_scale, (237, 228, 224), font_th)
    else:
        cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (102, 90, 72), 2)
        cv2.putText(keyboard, text, (text_x, text_y), font, font_scale, (133, 133, 133), font_th)



#Fazer menu de Direita e Esquerda
def draw_menu():
    rows, cols, _ = keyboard.shape
    th_lines = 4 # thickness lines
    cv2.line(keyboard, (int(cols/2) - int(th_lines/2), 0),(int(cols/2) - int(th_lines/2), rows),
            (255, 248, 234), th_lines)
    cv2.putText(keyboard, "LEFT", (65, 350), font, 5, (255, 248, 234), 5)
    cv2.putText(keyboard, "RIGHT", (45 + int(cols/2), 350), font, 5, (255, 248, 234), 5)

#Fazer o menu principal
def draw_main_menu():

    rows, cols, _ = keyboard.shape
    th_lines = 4 # thickness lines
    cv2.line(keyboard, (int(cols/3) - int(th_lines/3), 0),(int(cols/3) - int(th_lines/3), rows),
            (255, 248, 234), th_lines)
    cv2.line(keyboard, (int(cols*2/3) - int(th_lines*2/3), 0),(int(cols*2/3) - int(th_lines*2/3), rows),
            (255, 248, 234), th_lines)
    cv2.putText(keyboard, "WRITE", (45, 300), font, 2, (255, 248, 234), 3)
    cv2.putText(keyboard, "PHRASE", (45, 350), font, 2, (255, 248, 234), 3)
    cv2.putText(keyboard, "FEELINGS", (30 + int(cols/3), 300), font, 2, (255, 248, 234), 3)
    cv2.putText(keyboard, "TABLE", (30 + int(cols/3), 350), font, 2, (255, 248, 234), 3)
    cv2.putText(keyboard, "SAVED", (40 + int(cols*2/3), 300), font, 2, (255, 248, 234), 3)
    cv2.putText(keyboard, "PHRASES", (40 + int(cols*2/3), 350), font, 2, (255, 248, 234), 3)


def draw_save_menu():
    rows, cols, _ = keyboard.shape
    th_lines = 4 # thickness lines
    cv2.line(keyboard, (int(cols/2) - int(th_lines/2), 0),(int(cols/2) - int(th_lines/2), rows),
            (255, 248, 234), th_lines)
    cv2.putText(keyboard, "NEW", (65, 350), font, 5, (255, 248, 234), 5)
    cv2.putText(keyboard, "PHRASE", (65, 430), font, 5, (255, 248, 234), 5)
    cv2.putText(keyboard, "SAVED", (45 + int(cols/2), 350), font, 5, (255, 248, 234), 5)
    cv2.putText(keyboard, "PHRASES", (45 + int(cols/2), 430), font, 5, (255, 248, 234), 5)

#Fazer o quadro de emoções
def emote_menu(emote_index, text, letter_light):
    #Teclas
    if emote_index <= 4:
        x = emote_index*200
        y = 0
    elif 4 < emote_index <= 9:
        x = (emote_index-5)*200
        y = 200
    elif 9 < emote_index <= 14:
        x = (emote_index-10)*200
        y = 400

    width = 200
    height = 200
    th = 3 #thickness
   # Cfg Texto
    font_scale = 5
    font_th = 8
    text_size = cv2.getTextSize(text, font, font_scale, font_th)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x
    text_y = int((height + height_text) / 2) + y

    if letter_light is True:
        cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (245, 239, 230), 2)
        cv2.putText(keyboard, text, (text_x, text_y), font, font_scale, (237, 228, 224), font_th)
    else:
        cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (102, 90, 72), 2)
        cv2.putText(keyboard, text, (text_x, text_y), font, font_scale, (133, 133, 133), font_th)

def draw_saved_phrases(index, text, letter_light):
    xrec = 0
    
    if index == 0:    
        y = 0
    elif index == 1:
        y = 100
    elif index == 2:
        y = 200
    elif index == 3:
        y = 300
    elif index == 4:
        y = 400
    else:
        y = 500

    width = 1000
    height = 100
    th = 3 #thickness
    font_scale = 1
    font_th = 1

    text_x = 50
    text_y = int((height/ 2)) + y + 30

    if letter_light is True:
        cv2.rectangle(keyboard, (xrec + th, y + th), (xrec + width - th, y + height - th), (245, 239, 230), 2)
        cv2.putText(keyboard, text, (text_x, text_y), font, font_scale, (237, 228, 224), font_th)
    else:
        cv2.rectangle(keyboard, (xrec + th, y + th), (xrec + width - th, y + height - th), (102, 90, 72), 2)
        cv2.putText(keyboard, text, (text_x, text_y), font, font_scale, (133, 133, 133), font_th)

#Saber onde está o meio do olho
def midpoint (p1, p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

#Saber se está piscando ou não
def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    #hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
    #ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    ratio = hor_line_lenght / ver_line_lenght
    return ratio

#Fazer os circulos nos olhos na camera
def eyes_contour_points(facial_landmarks):
    left_eye = []
    right_eye = []
    for n in range(36, 42):
        x = facial_landmarks.part(n).x
        y = facial_landmarks.part(n).y
        left_eye.append([x, y])
    for n in range(42, 48):
        x = facial_landmarks.part(n).x
        y = facial_landmarks.part(n).y
        right_eye.append([x, y])
    left_eye = np.array(left_eye, np.int32)
    right_eye = np.array(right_eye, np.int32)
    return left_eye, right_eye


#Pegar as regiões do olho na camera apartir do arquivo .dat
def get_gaze_ratio(eye_points, facial_landmarks):
    left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                            (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                            (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                            (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                            (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                            (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)

    #cv2.polylines(frame, [left_eye_region], True, (0 , 0, 255), 2)

    

    height, width, _ = frame.shape
    mask = np.zeros((480, 640), np.uint8)

    cv2.polylines(mask, [left_eye_region], True, 255, 2)
    cv2.fillPoly(mask, [left_eye_region], 255)

    eye = cv2.bitwise_and(gray, gray, mask=mask)
        
    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])

    gray_eye = eye[min_y: max_y, min_x: max_x]
    
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    height, width = threshold_eye.shape

    left_side_threshold = threshold_eye[0: height, 0: int(width/2)]
    left_side_white = cv2.countNonZero(left_side_threshold)

    right_side_threshold = threshold_eye[0: height, int(width/2): width]
    right_side_white = cv2.countNonZero(right_side_threshold)

    gaze_ratio = left_side_white/(right_side_white+0.000000001)

    return gaze_ratio



# Counters
frames = 0 
letter_index = 0
index = 0
emote_index = 0
blinking_frames = 0 #numero de frames que o usuario está piscando
frames_to_blink = 6 #número de frames que usuario precisa estar com o olho fechado
frames_active_letter = 16 #Controle da rapidez da letra ativa no momento (maior = letras passam mais lentamente)
save_phrase = 0 #Saber se o usuario quer salvar a frase escrita ou não



#Texto e cfg Teclado
text = ""
keyboard_selected = "left"
last_keyboard_selected = "left"
select_keyboard_menu = 0 #0 - menu principal, 1 - menu teclado, 2 - teclado, 3 - emoções, 4 - menu de frases, 5 - frases salvas
keyboard_selection_frames = 0

while True:
    _, frame = cap.read()
    rows, cols, _ = frame.shape
    keyboard[:] = (89, 69, 69)
    frames += 1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Desenhar espaço branco para barra de loading
    frame[rows - 50: rows, 0: cols] = (255, 255, 255)


    #Fazer os menus selecionados
    if select_keyboard_menu == 0:
        draw_main_menu()

    if select_keyboard_menu == 1:
        draw_menu()
    
    if select_keyboard_menu == 4:
        draw_save_menu()
    

    

    
    
    if keyboard_selected == "left":
        keys_set = keys_set_1
    else:
        keys_set = keys_set_2

    active_letter = keys_set[letter_index]
    active_phrase = phrases[index]
    active_emotion = emotes_set[emote_index]
    active_emotion_phrase = emotes_phrases[emote_index]

    #Detector de face
    faces = detector(gray)
    for face in faces :
        #x, y = face.left(), face.top()
        #x1, y1 = face.right(), face.bottom()
        #cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)

        landmarks = predictor(gray, face)

        left_eye, right_eye = eyes_contour_points(landmarks)
        
        #Detectar Piscada
        left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        blinking_ratio = (right_eye_ratio + left_eye_ratio)/2

        # Cor olhos
        cv2.polylines(frame, [left_eye], True, (0, 0, 255), 2)
        cv2.polylines(frame, [right_eye], True, (0, 0, 255), 2)

        #Detectar olhar
        gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
        gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
        gaze_ratio = (gaze_ratio_left_eye + gaze_ratio_right_eye)/2


        if select_keyboard_menu == 0:

            if gaze_ratio <= 0.9:
                #Direita
                keyboard_selection_frames += 1
                if keyboard_selection_frames == 15:
                    select_keyboard_menu = 4 # Menu de Frases salvas
                    frames = 0
                    keyboard_selection_frames = 0
            elif 0.9 < gaze_ratio < 1.7:
                #Centro
                keyboard_selection_frames += 1
                if keyboard_selection_frames == 15:
                    select_keyboard_menu = 3 #Menu de emotes
                    frames = 0
                    keyboard_selection_frames = 0
            else:
                #Esqueda
                keyboard_selection_frames += 1
                if keyboard_selection_frames == 15: 
                    select_keyboard_menu = 1 #Menu de teclado
                    frames = 0
                    keyboard_selection_frames = 0
                    save_phrase = 0


        elif select_keyboard_menu == 1:


            #Mostrar direção
            if gaze_ratio < 1:
                keyboard_selected = "right"
                keyboard_selection_frames += 1
                if keyboard_selection_frames == 15:
                    select_keyboard_menu = 2
                    frames = 0
                    keyboard_selection_frames = 0
                if keyboard_selected != last_keyboard_selected:
                    last_keyboard_selected = keyboard_selected
                    keyboard_selection_frames = 0
            else:
                keyboard_selected = "left"
                keyboard_selection_frames += 1
                if keyboard_selection_frames == 15:
                    select_keyboard_menu = 2
                    frames = 0
                    keyboard_selection_frames = 0
                if keyboard_selected != last_keyboard_selected:
                    last_keyboard_selected = keyboard_selected
                    keyboard_selection_frames = 0
        
        
        elif select_keyboard_menu == 4:
            #Mostrar direção
            if gaze_ratio <= 1.1:
                #Direita
                keyboard_selection_frames += 1
                if keyboard_selection_frames == 20:
                    select_keyboard_menu = 5 #Saved Phrases
                    frames = 0
                    keyboard_selection_frames = 0
                    
            else:
                #Esquerda
                keyboard_selection_frames += 1
                if keyboard_selection_frames == 20:
                    select_keyboard_menu = 1 #Teclado que salva
                    frames = 0
                    keyboard_selection_frames = 0
                    save_phrase = 1


        elif select_keyboard_menu == 2 or select_keyboard_menu == 3 or select_keyboard_menu == 5:
            if blinking_ratio > 6.3:
                #cv2.putText(frame, "Blinking", (50, 150), font, 4, (255, 0, 0), thickness=3)
                blinking_frames += 1
                frames -= 1

                #Olhos verdes quando fechados
                cv2.polylines(frame, [left_eye], True, (0, 255, 0), 2)
                cv2.polylines(frame, [right_eye], True, (0, 255, 0), 2)

                # Escrita da letra
                if blinking_frames == frames_to_blink:
                    if select_keyboard_menu == 2:
                        if active_letter != "<" and active_letter != "_" and active_letter != "<<":
                            text += active_letter
                        if active_letter == "_":
                            text += " "
                        

                        if active_letter == "<<":
                            if save_phrase == 1:
                                with open('phrases.csv', 'a') as csv_file:
                                    csv_writer = csv.writer(csv_file)
                                    csv_writer.writerow(text)
                            select_keyboard_menu = 0   
                        else:
                            select_keyboard_menu = 1
                    
                    elif select_keyboard_menu == 3:
                        if active_emotion_phrase != "<":
                            text += active_emotion_phrase
                            select_keyboard_menu = 0
                        else:
                            select_keyboard_menu = 0

 
                    elif select_keyboard_menu == 5:
                        text += active_phrase
                        select_keyboard_menu = 0
        
            else:
                blinking_frames = 0  

                    


   # Mostrar Letras no Teclado (Menu de teclado, menu 2)
    if select_keyboard_menu == 2:
        if frames == frames_active_letter:
            letter_index += 1
            frames = 0
        if letter_index == 15:
            letter_index = 0
        for i in range(15):
            if i == letter_index:
                light = True
            else:
                light = False
            letter(i, keys_set[i], light)
    
    
    if select_keyboard_menu == 3:
        if frames == frames_active_letter:
            emote_index += 1
            frames = 0
        if emote_index == 15:
            letter_index = 0
        for i in range(15):
            if i == emote_index:
                light = True
            else:
                light = False
            emote_menu(i, emotes_set[i], light)


    if select_keyboard_menu == 5:
            
        with open('phrases.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)  
            next(csv_reader)
            if frames == frames_active_letter:
                index += 1
                frames = 0
            if index == 6:
                index = 0

            i = 0
            for line in csv_reader: 
                if i == index:
                    light = True
                else:
                    light = False
                phrases[i] = line[0]
                draw_saved_phrases(i, phrases[i], light)
                i = i + 1
                if i == 6:
                    break      
                    
        


    


    # Mostrar o texto escrito no quadro
    cv2.putText(board, text, (75, 200), font, 2, 0, 2)
    

    # Blinking loading bar
    percentage_blinking = blinking_frames / frames_to_blink
    loading_x = int(cols * percentage_blinking)
    cv2.rectangle(frame, (0, rows - 50), (loading_x, rows), (51, 51, 51), -1)

    cv2.imshow("Frame", frame)
    cv2.imshow("Keyboard", keyboard)
    cv2.imshow("Board", board)
    
    

    key = cv2.waitKey(1)
    if key == 27:
        break



cap.release()
cv2.destroyAllWindows()

