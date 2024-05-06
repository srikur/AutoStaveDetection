import sys
from AutoStaveDetection import AutoStaveDetection

# Shows the image, staves and notes for the first page of the PDF of Paganini's 24 Caprices
if __name__ == "__main__":
    path = "./data/paganini-caprices.pdf"
    auto_stave_detection = AutoStaveDetection(path)
    auto_stave_detection.detect_staves()
    auto_stave_detection.parse_notes()
    auto_stave_detection.display_image_by_index(0)
    auto_stave_detection.display_staves_by_index(0)
    auto_stave_detection.display_cleaned_notes_by_index(0)