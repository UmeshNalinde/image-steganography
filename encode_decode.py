import cv2
import numpy as np
from PIL import Image


def int_to_bin(rgb):
    """
    Convert an integer tuple to a binary (string) tuple.
    :param rgb: An integer tuple (e.g. (220, 110, 96))
    :return: A string tuple (e.g. ("00101010", "11101011", "00010110"))
    """
    r, g, b = rgb
    return ('{0:08b}'.format(r), '{0:08b}'.format(g), '{0:08b}'.format(b))


def bin_to_int(rgb):
    """
    Convert a binary (string) tuple to an integer tuple.
    :param rgb: A string tuple (e.g. ("00101010", "11101011", "00010110"))
    :return: Return an int tuple (e.g. (220, 110, 96))
    """
    r, g, b = rgb
    return (int(r, 2), int(g, 2), int(b, 2))


def reduceQuality(arr):
    newArr = list()
    for i in range(len(arr)):
        temp = arr[i]
        newArr.append(temp[0:4] + ("1" * 4))
    return newArr


def saveReduceQuality():
    img = Image.open("resources/image.png")
    pixel_map = img.load()
    # Create a new image that will be outputted
    new_image = Image.new(img.mode, img.size)
    pixels_new = new_image.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixels_new[i, j] = bin_to_int(
                reduceQuality(int_to_bin(pixel_map[i, j])))

    new_image.save("resources/reducedQuality.png")


def messageToBinary(message):
    if type(message) == str:
        return ''.join([format(ord(i), "08b") for i in message])
    elif type(message) == bytes or type(message) == np.ndarray:
        return [format(i, "08b") for i in message]
    elif type(message) == int or type(message) == np.uint8:
        return format(message, "08b")
    else:
        raise TypeError("Input type not supported")


# Function to hide the secret message into the image


def hideData(image, secret_message):

    # calculate the maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("Maximum bytes to encode:", n_bytes)

    #Check if the number of bytes to encode is less than the maximum bytes in the image
    if len(secret_message) > n_bytes:
        raise ValueError(
            "Error encountered insufficient bytes, need bigger image or less data !!"
        )

    secret_message += "#####"  # you can use any string as the delimeter

    data_index = 0
    # convert input data to binary format using messageToBinary() fucntion
    binary_secret_msg = messageToBinary(secret_message)

    data_len = len(
        binary_secret_msg)  #Find the length of data that needs to be hidden
    for values in image:
        for pixel in values:
            # convert RGB values to binary format
            r, g, b = messageToBinary(pixel)
            # modify the least significant bit only if there is still data to store
            if data_index < data_len:
                # hide the data into least significant bit of red pixel
                pixel[0] = int(
                    r[:-4] + binary_secret_msg[data_index:data_index + 4], 2)
                data_index += 4
            if data_index < data_len:
                # hide the data into least significant bit of green pixel
                pixel[1] = int(
                    g[:-4] + binary_secret_msg[data_index:data_index + 4], 2)
                data_index += 4
            if data_index < data_len:
                # hide the data into least significant bit of  blue pixel
                pixel[2] = int(
                    b[:-4] + binary_secret_msg[data_index:data_index + 4], 2)
                data_index += 4
            # if data is encoded, just break out of the loop
            if data_index >= data_len:
                break

    return image


def showData(image):

    binary_data = ""
    for values in image:
        for pixel in values:
            r, g, b = messageToBinary(
                pixel
            )  #convert the red,green and blue values into binary format
            binary_data += r[
                -4:]  #extracting data from the least significant bit of red pixel
            binary_data += g[
                -4:]  #extracting data from the least significant bit of red pixel
            binary_data += b[
                -4:]  #extracting data from the least significant bit of red pixel
            if (binary_data[-40:] == "1111111111111111111111111111111111111111"):
                break
            
    # split by 8-bits
    all_bytes = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]
    # convert from bits to characters
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[
                -5:] == "#####":  #check if we have reached the delimeter which is "#####"
            break
    #print(decoded_data)
    return decoded_data[:
                        -5]  #remove the delimeter to show the original hidden message


# Encode data into image
def encode_text():
    image_name = "resources/reducedQuality.png"
    image = cv2.imread(image_name)  # Read the input image using OpenCV-Python.
    #It is a library of Python bindings designed to solve computer vision problems.

    #details of the image
    print("The shape of the image is: ", image.shape
          )  #check the shape of image to calculate the number of bytes in it

    file = open('resources/text.txt', 'r')
    data = file.read()
    if (len(data) == 0):
        raise ValueError('Data is empty')

    filename = "resources/image_output.png"
    encoded_image = hideData(
        image, data
    )  # call the hideData function to hide the secret message into the selected image
    cv2.imwrite(filename, encoded_image)


# Decode the data in the image
def decode_text():
    # read the image that contains the hidden image
    image_name = "resources/image_output.png"
    image = cv2.imread(image_name)  #read the image using cv2.imread()

    text = showData(image)
    return text


# Image Steganography
def Steganography():
    a = input(
        "\nImage Steganography \n 1. Encode the data \n 2. Decode the data \n \n Your input is: "
    )
    userinput = int(a)
    if (userinput == 1):
        saveReduceQuality()
        print("\nEncoding....")
        encode_text()

    elif (userinput == 2):
        print("\nDecoding....")
        print("Decoded message is " + decode_text())
    else:
        raise Exception("Enter correct input")


Steganography()