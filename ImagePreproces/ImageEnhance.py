import cv2
import os
import glob
import numpy as np


def binarizeImage(img, th=127):
	if (len(img.shape) == 3):

		bin_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

		ret, thresh = cv2.threshold(bin_img, th, 255, cv2.THRESH_BINARY)

	else:

		ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

	return thresh


def grayImage(img):
	grey_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

	return grey_img


def displayImage(img):
	# res_img = cv2.resize(img, (500, 700))

	cv2.imshow('image', img)

	cv2.waitKey()

	cv2.destroyAllWindows()


def invertGrayImage(img):
	inv_img = (255 - img)

	return inv_img


def imageRotate(image, angle, center=None, scale=1.0):
	(h, w) = image.shape[:2]

	if center is None:
		center = (w / 2, h / 2)

	# Perform the rotation
	M = cv2.getRotationMatrix2D(center, angle, scale)
	rotated = cv2.warpAffine(image, M, (w, h))

	return rotated


def imageResize(img, w, h):
	res_img = cv2.resize(img, (w, h))

	return res_img


def imageResizeByRatio(img, ratio):
	res = cv2.resize(img, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_CUBIC)

	return res

def getCoordG(thresh):
	coordinates = np.column_stack(np.where(thresh > 0))
	ag = cv2.minAreaRect(coordinates)[-1]
	if ag < -45:
		ag = -(90 + ag)
	else:
		ag = -ag

	return ag


def imageCrop(img, r1, r2, c1, c2):
	crop_img = img[r1:r2, c1:c2]

	return crop_img


def imageEnh(image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.bitwise_not(gray)
	thr = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	(h, w) = image.shape[:2]
	center = (w // 2, h // 2)
	rMat = cv2.getRotationMatrix2D(center, getCoordG(thr), 1.0)
	enh = cv2.warpAffine(image, rMat, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

	return enh
