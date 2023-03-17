import os

folders = ['media', 'staticfiles']
for folder in folders:
    if not os.path.exists(folder):
        os.mkdir(folder)

os.system("./rm")
os.system("./migrate")
if input("deseja criar um super usuario? s/n\n") == "s":
    os.system("python3 manage.py createsuperuser")
