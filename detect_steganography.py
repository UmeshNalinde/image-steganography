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


def shiftLeft(arr, d):
    newArr = list()
    for i in range(len(arr)):
        temp = arr[i]
        newArr.append(temp[d:] + ("1" * d))
    return newArr


# def halfQuality(arr):
#     newArr = list()
#     for i in range(len(arr)):
#         temp = arr[i]
#         newArr.append(temp[0:4] + ("1" * 4))
#     return newArr

img = Image.open("resources/image_output.png")
pixel_map = img.load()

for x in range(1, 5):
    # Create a new image that will be outputted
    new_image = Image.new(img.mode, img.size)
    pixels_new = new_image.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixels_new[i, j] = bin_to_int(
                shiftLeft(int_to_bin(pixel_map[i, j]), x))

    new_image.save("resources/detect_steganography/Pixel_bit_shift_left_by_" +
                   str(x) + ".png")
    print("saving", x)
