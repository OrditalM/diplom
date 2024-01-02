import cv2


def zoom(image, factor, zoom_center):
    if factor != 1:
        height, width, _ = image.shape

        new_width = int(width / factor)
        new_height = int(height / factor)

        roi_x = max(0, int(zoom_center[0] - new_width / 2))
        roi_y = max(0, int(zoom_center[1] - new_height / 2))
        roi_width = min(new_width, width - roi_x)
        roi_height = min(new_height, height - roi_y)

        zoomed_roi = cv2.resize(image[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width], (width, height))
        return zoomed_roi

    return image

