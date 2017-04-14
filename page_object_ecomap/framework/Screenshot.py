from PIL import Image


class Screenshot(object):
    def __init__(self, driver):
        self.driver = driver

    def get_element_location(self, *locator):
        locations = {}
        element = self.driver.find_element(*locator)
        location = element.location
        size = element.size
        locations['left'] = location['x']
        locations['top'] = location['y']
        locations['right'] = location['x'] + size['width']
        locations['bottom'] = location['y'] + size['height']
        return locations

    def get_screenshot_as_file(self, file_path):
        return self.driver.get_screenshot_as_file(file_path)

    def get_cropped_image(self, path_full_img, path_cropped_img, element_locator):
        img_location = self.get_element_location(*element_locator)
        self.get_screenshot_as_file(path_full_img)
        full_screen = Image.open(path_full_img)
        map_img = full_screen.crop(
            (img_location['left'], img_location['top'], img_location['right'], img_location['bottom']))
        map_img.save(path_cropped_img)
        return map_img

    def get_pixels_by_color(self, mode, color_index, image):
        colors = image.convert(mode).getcolors()
        for i in range(len(colors)):
            if color_index in range(256):
                if colors[i][1] == color_index:
                    return colors[i][0]
        return None

    def get_pixels_count(self, image):
        width, height = image.size
        return width * height

    def get_pixels_percentage(self, num, denum):
        return num * 100 / denum
