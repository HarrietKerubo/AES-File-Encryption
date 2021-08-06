from django.shortcuts import render
from django.shortcuts import render
from cryptography.fernet import Fernet
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib import messages
import os
# Create your views here.
def index(request):
    return render(request, 'index.html')

def encryption(request):

            # Encrypt
    #Key generation
    key = Fernet.generate_key()  # Keep this secret!
    print(type(key))  # bytes
    print( " The key is: ",key)  # base64 encoded 32 bytes

    # store the key in a file
    with open ('filekey.key', 'wb') as filekey: #this creates the file
        filekey.write(key) #stores the key in the file created

    print ("filekey stored")
    #Encrypt the file using the key generated
    # opening the file containing the key and read the key

    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()

    #using the generated key : By initializing the Fernet object

    my_fernet = Fernet(key)

    # open the original file to encrypt
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        print(filename)

        #reading file from the default storage which is the media folder
        #this code reads the file, encrypts the file
        #then opens the file and writes encrypted data on it
        file = default_storage.open(os.path.join('', filename), 'rb')
        original = file.read()
        encrypted = my_fernet.encrypt(original)
        encrypted_file = default_storage.open(os.path.join('', filename), 'wb')
        encrypted_file.write(encrypted)
        messages.success(request, 'Document Encrypted Successfully access it at:'+ settings.MEDIA_ROOT )


    return render(request, 'encrypted.html')


def decryption(request):
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()

        # using the key
        fernet = Fernet(key)


    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        print(filename)

        enc_file = default_storage.open(os.path.join('', filename), 'rb')
        encrypted = enc_file.read()

    # decrypting the file
        decrypted = fernet.decrypt(encrypted)
        dec_file = default_storage.open(os.path.join('', "decrypted " + filename), 'wb')
        dec_file.write(decrypted)
        messages.success(request, 'Document Decrypted Successfully access it at:'+ settings.MEDIA_ROOT )

    return render(request, 'decrypted.html')


