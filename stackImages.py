import numpy as np
import cv2


def to_multiple(arr, row, col):
    result = []
    for y in range(0, col):
        for x in range(0, row):
            if x == 0:
                result.append([])
            result[y].append(arr[x + y * row])
    return result


def stack_images(scale, imgArray):
    rows = len(imgArray)
    cols = 1
    for row in imgArray:
        if isinstance(row, list):
            cols = max(cols, len(row))
    print(rows, cols)
    if isinstance(imgArray[0], list):
        width = int(imgArray[0][0].shape[1] * scale)
        height = int(imgArray[0][0].shape[0] * scale)
    else:
        width = int(imgArray[0].shape[1] * scale)
        height = int(imgArray[0].shape[0] * scale)
    dim = (width, height)
    dim3 = (width, height, 3)
    max_col = int(1920 / width)
    new_array = []
    if cols == 1:
        if rows > max_col:
            new_rows = int(rows / max_col) + 1
            for i in range(0, new_rows * max_col):
                new_array.append(np.zeros(dim3, dtype=np.uint8))
            for i in range(rows):
                if len(imgArray[i].shape) == 2:
                    new_array[i] = cv2.resize(cv2.cvtColor(imgArray[i], cv2.COLOR_GRAY2BGR), dim)
                else:
                    new_array[i] = cv2.resize(imgArray[i], dim)
            new_array = to_multiple(new_array, max_col, new_rows)
            hor = []
            for r in new_array:
                hor.append(np.hstack(r))
            return np.vstack(hor)
        else:
            for img in imgArray:
                if len(img.shape) == 2:
                    new_array.append(cv2.resize(cv2.cvtColor(img, cv2.COLOR_GRAY2BGR), dim))
                else:
                    new_array.append(cv2.resize(img, dim))
            return np.hstack(new_array)
    else:
        for row in imgArray:
            if isinstance(row, list):
                for i in row:
                    if len(i.shape) == 2:
                        new_array.append(cv2.resize(cv2.cvtColor(i, cv2.COLOR_GRAY2BGR), dim))
                    else:
                        new_array.append(cv2.resize(i, dim))
                for i in range(len(row), cols):
                    new_array.append(np.zeros(dim3, dtype=np.uint8))
            else:
                new_array.append(cv2.resize(row, dim))
        new_array = to_multiple(new_array, cols, rows)
        hor = []
        for r in new_array:
            hor.append(np.hstack(r))
        return np.vstack(hor)


def imshow(imgArray, scale=1, windowName="Stack Images Window"):
    img = stack_images(scale, imgArray)
    cv2.imshow(windowName, img)
