import cv2
import threading
import playsound
import requests

fire_cascade = cv2.CascadeClassifier(
    rf"C:\Users\avina\OneDrive\Desktop\miniproject\fire_detection.xml")  # Change this file path

vid = cv2.VideoCapture(0)
runOnce = False


def play_alarm_sound_function():
    playsound.playsound(r"C:\Users\avina\OneDrive\Desktop\miniproject\FIre_alert_sound.mp3",
                        True)  # Change this file path
    print("Fire alarm end")


def alert_message_function():
    querystring = {"apikey": "8K45BHDEJALG6UTHNFIA", "number": "918096545332",
                   "text": "EMERGENCY!!! FIRE Accident Took Place AT ABC Rubber Factory,Nampally X Roads,Hyderabad,Telangana.PLEASE SEND FIRE FIGHTERS AND FIRE ENGINES AT THE LOCATION. "}
    url = "https://panel.rapiwha.com/send_message.php"
    # beside number: 91 is India code and any 10digit mobile no.; beside text in double inverted commas u can change it as your msg according to ur requirement
    response = requests.request("GET", url, params=querystring)

    # querystring1 = {"apikey":"CZNT2KLOQJP8LZVA98E1","number":"","text":"SEND FIRE ENGINES AT NGIT"}

    # response1 = requests.request("GET", url, params=querystring1)
    # print(response1.text)

    # to add another number uncomment above code and make changes as required

    print(response.text)


while (True):
    ret, frame = vid.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fire = fire_cascade.detectMultiScale(frame, 1.2, 10)  # (1.2,10)(2.0,10)

    for (x, y, w, h) in fire:
        cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        print("Fire alarm initiated")
        threading.Thread(target=play_alarm_sound_function).start()

        if runOnce == False:
            print("Alert Initiated")
            threading.Thread(target=alert_message_function).start()
            runOnce = True
        if runOnce == True:
            print("Alert message already sent")
            runOnce = True

    cv2.imshow("Fire Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
