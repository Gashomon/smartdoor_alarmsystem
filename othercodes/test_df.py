
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from deepface import DeepFace as df

print("CHOICES \n verify : 1\n find: 2 \n find w/ name: 3")
choice = int(input("enter choice: "))

if choice == 1:
    img_path1 = input("Enter path to image1:")
    img_path2 = input("Enter path to image2:")

    im1_found = os.path.exists(img_path1)
    im2_found = os.path.exists(img_path2)

    if im1_found and im2_found:
        result = df.verify(img_path1, img_path2)
        print(f"\ngot the results! \n {result}")
    else:
        print("something went wrong")
    
if choice == 2:
    img_path1 = input("Enter path to image1:")
    db_path1 = input("Enter path to database folder:")

    im_found = os.path.exists(img_path1)
    db_found = os.path.exists(db_path1)

    if im_found and db_found:
        result = df.find(img_path1, db_path1)
        print(f"\ngot the results! \n {result}")
    else:
        print("something went wrong")

if choice == 3:
    img_path1 = input("Enter path to image1:")
    db_path1 = input("Enter path to database folder:")

    im_found = os.path.exists(img_path1)
    db_found = os.path.exists(db_path1)

    if im_found and db_found:
        result = df.find(img_path1, db_path1)
        df.represent()
        print(f"\ngot the results! \n {result}")
    else:
        print("something went wrong")

del os.environ['TF_ENABLE_ONEDNN_OPTS']