from pydub import AudioSegment
from urllib.request import urlopen
import tempfile
import uuid
import base64

def convert_mp3_ogg(filepath):
    data = urlopen(filepath).read()
    f = tempfile.NamedTemporaryFile(delete=True)
    f.write(data)
    filename = uuid.uuid4()
    AudioSegment.from_mp3(f.name).export('static/{}.ogg'.format(filename), format='ogg')
    f.close()

    return str(filename) + ".ogg"


