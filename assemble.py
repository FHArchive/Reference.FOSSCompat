#!/usr/bin/env python3
"""Create a series of themed images from a source image
"""
from PIL import Image
import re
import os


def resizeImageAbs(image, width, height):
	"""Resize an image with desired dimensions. This is most suitable for resizing non
	square images where a factor would not be sufficient

	Args:
		image (PIL.Image.Image): A PIL Image
		width (int): width in px
		height (int): height in px

	Returns:
		PIL.Image.Image: Image
	"""
	return image.resize((width, height), Image.ANTIALIAS)


def openImage(file):
	"""Opens a single image and returns an image object.
	Use full file path or file path relative to /lib

	Args:
		file (string): full file path or file path relative to /lib

	Returns:
		PIL.Image.Image: Image
	"""
	return Image.open(file)


def saveImage(fileName, image, optimise=True):
	"""Saves a single image.
	Use full file path or file path relative to /lib. Pass in the image object

	Args:
		fileName (string): full file path or file path relative to /lib
		image (PIL.Image.Image): A PIL Image
		optimise (bool, optional): Optimise the image?. Defaults to True.
	"""
	createDirsIfRequired(fileName)
	if optimise:
		image = image.quantize(colors=255, method=2, kmeans=1, dither=None)
	image.save(fileName, optimize=optimise, quality=75)


def createDirsIfRequired(filepath):
	"""Create directories if required when writing a file

	Args:
		filepath (string): full file path or file path relative to /lib
	"""
	tok = re.split('/|\\\\', filepath)
	checkfile = ''
	for x in tok[:-1]:
		checkfile += x + '\\'
	os.makedirs(checkfile, exist_ok=True)


def findAndReplace(image, find, replace):
	"""Find and replace colour in PIL Image

	Args:
		image (PIL.Image.Image): The Image
		find ((r,g,b,a)): A tuple containing values for rgba from 0-255 inclusive
		replace ((r,g,b,a)): A tuple containing values for rgba from 0-255 inclusive

	Returns:
		PIL.Image.Image: The result
	"""
	def cmpTup(tupleA, tupleB):
		for index, _ in enumerate(tupleA):
			if (tupleA[index] > tupleB[index] +
                                10 or tupleA[index] < tupleB[index] - 10):
				return False
		return True

	converted = image.convert('RGBA')
	pixels = converted.load()
	for i in range(image.size[0]):
		for j in range(image.size[1]):
			if cmpTup(pixels[i, j], find):
				pixels[i, j] = replace

	return converted.convert("RGBA")


COLORS = {
	"text": [
		# Unsure why but 0,0,0,255 gave trouble - probably a bug
		(10, 10, 10, 255), (171, 178, 191, 255), (56, 58, 66, 255), (171, 178, 191, 255)
	],
	"background": [
		(255, 255, 255, 255), (18, 20, 23, 255), (250, 250, 250, 255), (0, 0, 0, 255)
	],
	"danger-arrow": [
		(0, 255, 33, 255), (224, 108, 117, 255), (228, 86, 73, 255), (224, 108, 117, 255)
	],
	"public": [
		(255, 0, 0, 255), (40, 44, 52, 255), (229, 229, 230, 255), (25, 25, 25, 255)
	],
	"permissive-gpl": [
		(0, 147, 254, 255), (40, 44, 52, 255), (229, 229, 230, 255), (25, 25, 25, 255)
	],
	"permissive": [
		(177, 0, 255, 255), (40, 44, 52, 255), (229, 229, 230, 255), (25, 25, 25, 255)
	],
	"copyleft": [
		(255, 216, 0, 255), (40, 44, 52, 255), (229, 229, 230, 255), (25, 25, 25, 255)
	]
}

def removeLeftMargin(image, padding):
	"""Remove the left margin of width = padding from an image

	Args:
		image (PIL.Image.Image): A PIL Image
		padding (int): The padding in pixels

	Returns:
		PIL.Image.Image: A PIL Image
	"""
	return image.crop((padding, 0, image.width, image.height))

def removeBottomMargin(image, padding):
	"""Remove the bottom margin of width = padding from an image

	Args:
		image (PIL.Image.Image): A PIL Image
		padding (int): The padding in pixels

	Returns:
		PIL.Image.Image: A PIL Image
	"""
	return image.crop((0, 0, image.width, image.height - padding))

"""FILES stores data on files to reduce the amount of copying and pasting code
that I would otherwise have to do. Elements in this dictionary are to be accessed
from within a for loop... In the form name: src_file, color_index, bottom_margin
"""
FILES = {
	"SoftwareBlack": ["Software", 3, 400],
	"SoftwareDark": ["Software", 1, 400],
	"SoftwareLight": ["Software", 2, 400],
	"SoftwareBlackS": ["Software", 3, 0],
	"SoftwareDarkS": ["Software", 1, 0],
	"SoftwareLightS": ["Software", 2, 0],

	"MediaBlack": ["Media", 3, 200],
	"MediaDark": ["Media", 1, 200],
	"MediaLight": ["Media", 2, 200],
	"MediaBlackS": ["Media", 3, 0],
	"MediaDarkS": ["Media", 1, 0],
	"MediaLightS": ["Media", 2, 0],
}

if __name__ == "__main__":

	for fileDest in FILES:
		print("Working on: "+ fileDest)
		fileAttributes = FILES.get(fileDest)
		imageSrc = removeBottomMargin(
			removeLeftMargin(
				openImage("ImageSource/"+fileAttributes[0]+".png")
				.quantize(colors=len(COLORS), method=2, kmeans=1, dither=None),
			200
			), fileAttributes[2]
		)

		for color in COLORS:
			print(COLORS.get(color))
			imageSrc = findAndReplace(
				imageSrc,
				COLORS.get(color)[0],
				COLORS.get(color)[fileAttributes[1]]
			)


		saveImage("ImageOut/"+fileDest+".png", imageSrc)
