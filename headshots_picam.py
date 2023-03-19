import cv2
import os
import time

name = input("Enter Username=") #replace with your name
parent_dir = "dataset/"
path = os.path.join(parent_dir, name)
os.mkdir(path)
print("Directory '% s' created" % name)
    
i = 0
camera = cv2.VideoCapture(0)
while True:
    return_value, image = camera.read()
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('image', gray)
    k=input("Start?")
    if k=='Start':#cv2.waitKey(1) & 0xFF == ord('s'):  # take a screenshot if 's' is pressed
        for i in range(20):
            cv2.imwrite('dataset/'+name+'/image_{0}.png'.format(i), image)
            return_value, image = camera.read()
            i += 1
            print(i)
            time.sleep(0.2)

        break

camera.release()
cv2.destroyAllWindows()
os.system('python3 train_model.py')

