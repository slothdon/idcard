import cv2


def face_check(path):
    face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
    video = cv2.VideoCapture(0)

    count = 1
    face_unhold = 0
    count_face = 2

    while True:
        ret, frame = video.read()

        if count % 2 != 0:
            count += 1
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(5, 5))

        if count_face != len(faces):
            face_unhold += 1
        elif count_face == len(faces):
            face_unhold = 0
        print('holding:', face_unhold)

        if face_unhold == 10:
            video.release()
            cv2.destroyAllWindows()
            return False

        for (x, y, w, h) in faces:
            img = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            f = cv2.resize(gray[y:y + h, x:x + w], (200, 200))

            cv2.imwrite('auto/alin/%s.pgm' % (str(count)), f)
            count += 1

        cv2.imshow('video', frame)

        if cv2.waitKey(120) & 0xff == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

    return True


if __name__ == '__main__':
    path = '../img/video/x.mp4'
    face_check()