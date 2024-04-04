import numpy as np
import cv2


class ColorGradient:
    def __init__(self, start_ph, end_ph, colors_list, length=800, width=100):
        self.start_ph = start_ph
        self.end_ph = end_ph
        self.length = length
        self.width = width
        self.colors_list = colors_list
        self.gradient = self.create_multi_gradient()

    def create_gradient_segment(self, start_color, end_color, width):
        start_color = np.array(start_color[::-1], dtype=np.uint8)
        end_color = np.array(end_color[::-1], dtype=np.uint8)
        gradient = np.zeros((1, width, 3), dtype=np.uint8)

        for x in range(width):
            alpha = x / (width - 1)
            color = (1 - alpha) * start_color + alpha * end_color
            gradient[0, x] = color

        return gradient

    def create_multi_gradient(self):
        segments_count = len(self.colors_list) - 1
        segment_width = self.length // segments_count
        gradient = np.zeros((self.width, self.length, 3), dtype=np.uint8)

        for i in range(segments_count):
            segment = self.create_gradient_segment(self.colors_list[i], self.colors_list[i + 1], segment_width)
            segment = cv2.resize(segment, (segment_width, self.width), interpolation=cv2.INTER_LINEAR)
            gradient[:, i * segment_width:(i + 1) * segment_width] = segment

        if self.length % segments_count != 0:
            last_segment_width = self.length - (segments_count - 1) * segment_width
            last_segment = self.create_gradient_segment(self.colors_list[-2], self.colors_list[-1], last_segment_width)
            last_segment = cv2.resize(last_segment, (last_segment_width, self.width), interpolation=cv2.INTER_LINEAR)
            gradient[:, -last_segment_width:] = last_segment

        return gradient

    def find_closest_color(self, target_rgb):
        target_bgr = target_rgb[::-1]
        distances = np.sqrt(np.sum((self.gradient - target_bgr) ** 2, axis=2))
        min_dist_index = np.unravel_index(np.argmin(distances), distances.shape)
        closest_color = self.gradient[min_dist_index]

        return closest_color[::-1], min_dist_index