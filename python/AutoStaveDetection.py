import fitz
import cv2
from Utils import document_to_images, show_images_grid
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

class AutoStaveDetection():
    pdf_path = None
    images = None
    # Contains the staves for each image
    staves_list = None
    # Cleaned notes images
    notes_without_lines = None

    def __init__(self, path: str):
        self.pdf_path = path
        self.images = document_to_images(self.pdf_path)
        self.staves_list = {i: [] for i in range(len(self.images))}
        self.notes_without_lines = {i: [] for i in range(len(self.images))}

    def display_image_by_index(self, i):
        if i < 0 or i >= len(self.images):
            # raise an exception
            raise Exception(f"Image index out of bounds. Index: {i}, Number of images: {len(self.images)}")
        plt.imshow(self.images[i], cmap='gray')
        plt.show()

    def display_staves_by_index(self, i):
        if i < 0 or i >= len(self.staves_list):
            # raise an exception
            raise Exception("Stave index out of bounds")
        show_images_grid(self.staves_list[i])

    def display_cleaned_notes_by_index(self, i):
        if i < 0 or i >= len(self.notes_without_lines):
            # raise an exception
            raise Exception("Notes index out of bounds")
        show_images_grid(self.notes_without_lines[i])

    def _find_troughs(self, img, std_modifier):
        inverted_img = np.max(img) - img
        troughs = []
        while len(troughs) == 0:
            threshold_value = np.mean(np.sum(inverted_img == 0, axis=1)) + std_modifier * np.std(np.sum(inverted_img == 0, axis=1))
            troughs, _ = find_peaks(np.sum(inverted_img == 0, axis=1), height=0)
            troughs = troughs[np.sum(inverted_img == 0, axis=1)[troughs] > threshold_value]
            std_modifier -= 0.1

        # Plot the histogram with troughs
        # plt.plot(np.sum(inverted_img == 0, axis=1))
        # plt.plot(troughs, np.sum(inverted_img == 0, axis=1)[troughs], "o", color='green')
        # plt.show()

        return troughs
    
    def _group_peaks_into_staves(self, peaks, troughs):
        staffs = []
        for i, peak in enumerate(peaks[:-1]):
            next_peak = peaks[i + 1]
            trough_indices = [j for j, tr in enumerate(troughs) if peak < tr < next_peak]
            if len(trough_indices) == 1:
                trough = troughs[trough_indices[0]]
                staffs.append((peak, trough, next_peak))
        return staffs

    def _find_staff_bounds(self, staffs, troughs):
        bounds = []
        for staff in staffs:
            start_trough_index = np.where(troughs == staff[1])[0][0] - 1
            end_trough_index = np.where(troughs == staff[1])[0][0] + 1
            if start_trough_index >= 0 and end_trough_index < len(troughs):
                bounds.append((troughs[start_trough_index], troughs[end_trough_index]))
        return bounds

    def _cluster_points(self, points, max_distance):
        clusters = []
        current_cluster = [points[0]]
        for point in points[1:]:
            if point - current_cluster[-1] <= max_distance:
                current_cluster.append(point)
            else:
                clusters.append(current_cluster)
                current_cluster = [point]
        if current_cluster:
            clusters.append(current_cluster)
        return clusters

    def _calculate_cluster_centers(self, clusters):
        return [int(np.mean(cluster)) for cluster in clusters]

    def _find_staff_bounds_from_troughs(self, trough_centers):
        staff_bounds = []
        for i in range(len(trough_centers) - 1):
            staff_start = trough_centers[i]
            staff_end = trough_centers[i + 1]
            staff_bounds.append((staff_start, staff_end))
        return staff_bounds

    def _remove_false_troughs(self, trough_centers):
        distances = np.diff(trough_centers)  # Calculate distances between consecutive troughs
        mean_distance = np.mean(distances)
        std_distance = np.std(distances)
        
        # Identify troughs to remove based on being significantly lower than the mean
        # Here we consider a trough to be an outlier if it's less than half the mean distance
        to_remove = []
        for i, distance in enumerate(distances):
            if distance < mean_distance / 2:
                # Mark the index of the second trough in the pair for removal
                to_remove.append(i + 1)
        
        # Remove the identified troughs
        cleaned_troughs = [tr for i, tr in enumerate(trough_centers) if i not in to_remove]
        return cleaned_troughs

    def _parse_staves(self, original_img_index, stave_threshold=1.0, trough_threshold=0.7):
        # Goal: Get coordinates for each staff line
        original_img = self.images[original_img_index]

        # convert to black and white
        original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
        _, original_img = cv2.threshold(original_img, 200, 255, cv2.THRESH_BINARY)

        # For each row of the image, get the number of black pixels
        black_pixels = np.sum(original_img == 0, axis=1)

        # Find peaks
        black_pixels = black_pixels.flatten()
        peaks, _ = find_peaks(black_pixels, height=0)

        # plot the histogram with peaks
        # plt.plot(black_pixels)
        # plt.plot(peaks, black_pixels[peaks], "x", color='orange')
        # plt.show()

        # Threshold for staves
        staff_line_peaks = []
        std_modifier = stave_threshold
        while len(staff_line_peaks) == 0:
            threshold_value = np.mean(black_pixels) + std_modifier * np.std(black_pixels)
            staff_line_peaks = peaks[black_pixels[peaks] > threshold_value]
            std_modifier -= 0.1
        staff_line_troughs = self._find_troughs(original_img, trough_threshold)

        # Clustering peaks and troughs into means
        # make max_distance the average distance between staff line peaks
        max_distance = np.mean(np.diff(staff_line_peaks)) / 2
        peak_clusters = self._cluster_points(staff_line_peaks, max_distance)
        trough_clusters = self._cluster_points(staff_line_troughs, max_distance)

        # Calculate cluster centers
        # peak_centers = self._calculate_cluster_centers(peak_clusters)
        trough_centers = self._calculate_cluster_centers(trough_clusters)

        # Remove false troughs
        trough_centers = self._remove_false_troughs(trough_centers)

        # Find staff bounds
        staff_bounds = self._find_staff_bounds_from_troughs(trough_centers)

        # Plot the histogram with peak_centers and trough_centers
        # plt.plot(black_pixels)
        # plt.plot(peak_centers, black_pixels[peak_centers], "x", color='orange')
        # plt.plot(trough_centers, black_pixels[trough_centers], "o", color='green')
        # for lower, upper in staff_bounds:
        #     plt.axvline(x=lower, color='green', linestyle='--')
        #     plt.axvline(x=upper, color='red', linestyle='--')
        # plt.show()

        # Split the image into staves
        staves = []
        for lower, upper in staff_bounds:
            stave = original_img[lower:upper, ]
            # Remove extraneous white space from the stave's top or bottom
            # stave = stave[np.sum(stave == 1, axis=1) > 0, ]
            staves.append(stave)

        # plot all the staves in a grid
        # plt.figure(figsize=(20, 20))
        # for i, staff in enumerate(staves):
        #     plt.subplot(len(staves) // 2 + 1, 2, i + 1)
        #     plt.imshow(staff, cmap='gray')
        # plt.show()

        self.staves_list[original_img_index] = staves

    def _remove_staff_lines(self, staff):
        # Idea: Staff lines are horizontal lines, so we can use a horizontal kernel to detect them
        kernel = np.ones((1, 100), np.uint8)
        staff_without_lines = cv2.morphologyEx(staff, cv2.MORPH_CLOSE, kernel)
        _, staff_without_lines = cv2.threshold(staff_without_lines, 200, 255, cv2.THRESH_BINARY)

        # If a staff image is mostly or completely black, it's probably not a staff and we can remove it from the staff list to return
        if np.sum(staff_without_lines == 0) < 0.01 * staff_without_lines.size:
            return None
        
        return staff_without_lines
    
    def _get_notes_without_staves(self, staves, staves_without_lines):
        notes_without_staves = []
        for i in range(len(staves)):
            staff = staves[i]
            staff_without_lines = staves_without_lines[i]
            filtered_staff = cv2.subtract(staff_without_lines, staff)
            #invert the colors of the images
            filtered_staff = cv2.bitwise_not(filtered_staff)
            notes_without_staves.append(filtered_staff)
        return notes_without_staves
    
    def parse_notes(self):
        for i in range(len(self.images)):
            for j, staff in enumerate(self.staves_list[i]):
                staff_without_lines = self._remove_staff_lines(staff)
                if staff_without_lines is not None:
                    self.notes_without_lines[i].append(self._get_notes_without_staves(staff, staff_without_lines))

    def detect_staves(self, stave_threshold=1.0, trough_threshold=0.7):
        for i in range(len(self.images)):
            self._parse_staves(i)
