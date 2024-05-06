import sys
from AutoStaveDetection import AutoStaveDetection

# Shows the image, staves and notes for the first page of the PDF of Scott Joplin's The Entertainer
# Also try out page 0 of Paganini's Caprices in the data folder! And make sure to try out different thresholds for the best results
if __name__ == "__main__":
    path = "./data/TheEntertainer.pdf"
    auto_stave_detection = AutoStaveDetection(path)
    auto_stave_detection.detect_staves(stave_threshold=1.0, trough_threshold=0.7)
    auto_stave_detection.parse_notes()
    auto_stave_detection.display_image_by_index(0)
    auto_stave_detection.display_staves_by_index(0)
    auto_stave_detection.display_cleaned_notes_by_index(0)