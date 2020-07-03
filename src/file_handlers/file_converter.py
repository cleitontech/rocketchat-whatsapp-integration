from pydub import AudioSegment
import tempfile
import uuid
import base64
import requests

def convert_mp3_ogg(filepath):
    #TODO: delete temporary files
    request = requests.get(filepath, allow_redirects = True)
    file_bytes = request.content

    temp_file_name = "temp/"+str(uuid.uui4()) + ".mp3"
    temp_file = open(temp_file_name, "wb")
    temp_file.write(file_bytes)
    temp_file.close()

    filename = str(uuid.uuid4())
    AudioSegment.from_mp3(temp_file_name).export('static/{}.ogg'.format(filename), format='ogg')

    data = open("static/{}.ogg".format(filename), "rb").read()
    encoded = base64.b64decode(data).decode('ascii')
    return encoded


