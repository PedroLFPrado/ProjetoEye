import cv2
import numpy as np

keyboard = np.zeros((600, 1000, 3), np.uint8)

keys_set_1 = {0 : "A", 1: "B", 2: "C", 3: "D", 4: "E", 
                5: "F", 6: "G", 7: "H", 8: "I", 9: "J", 
                10: "K", 11: "L", 12: "M", 13: "N", 14: "O"}

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
    if letter_light == True:
        cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height- th), (255, 255, 255), -1)
    else:
        cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height- th), (255, 0, 0), th)

    

    #Config texto
    font_letter = cv2.FONT_HERSHEY_PLAIN
    font_scale = 10
    font_th = 4
    text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x
    text_y = int((height - height_text + 50)) + y
    cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (255,0,0), font_th)

for i in range(15):
    if i == 5:
        light = True
    else:
        light = False

    letter(i,keys_set_1[i], light)



cv2.imshow("Teclado", keyboard)
cv2.waitKey(0)
cv2.destroyAllWindows()