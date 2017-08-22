from PIL import Image
from io import BytesIO
import base64
import cv2
import numpy



def base64_to_pilImage(b64_Filedata):

    if b64_Filedata is None:
        return None

    try:

        pil_Image = Image.open(BytesIO(base64.b64decode(b64_Filedata)))

    except:

        pil_Image = None

    return pil_Image

def base64_to_openCVImage(b64_Filedata):

    if b64_Filedata is None:
        return None

    pilImage = base64_to_pilImage(b64_Filedata)

    try:
        if pilImage is not None:
            openCVImage = numpy.array(pilImage)
        else:
            openCVImage = None
    except:
        openCVImage = None

    return openCVImage


def opencvImage_to_base64(openCVImage):

    if openCVImage is None or type(openCVImage) is not numpy.ndarray:
        return ""

    try:

        cnt = cv2.imencode('.png', openCVImage)[1]
        b64_Filedata = base64.encodestring(cnt)
        return b64_Filedata

    except:

        return ""
