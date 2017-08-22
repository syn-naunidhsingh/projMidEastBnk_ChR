import Base64TestImages
from pkg_resources import resource_string, resource_listdir


BASE_64_TEST_IMAGES_RES_PKG_NAME = Base64TestImages.__name__
TEXT_FILE_EXTENSION = ".txt"

def getBase64ResourceImages():

    Base64Strings = {}

    for imgB64TextFile in resource_listdir(BASE_64_TEST_IMAGES_RES_PKG_NAME, ''):

        if imgB64TextFile.endswith(TEXT_FILE_EXTENSION):

            imgB64TextString = resource_string(BASE_64_TEST_IMAGES_RES_PKG_NAME, imgB64TextFile)

            Base64Strings[imgB64TextFile] = imgB64TextString

    return Base64Strings

