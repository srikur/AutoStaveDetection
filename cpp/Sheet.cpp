#include "Utilities.h"
#include "Sheet.h"

Sheet::Sheet(FilePath pagePath) {
    /* Load the image */
    image = new cv::Mat(cv::imread(pagePath, cv::IMREAD_GRAYSCALE));
    if (image->empty()) {
        std::cerr << "Could not read image at " << pagePath << std::endl;
    }
}

Sheet::~Sheet() {
    delete image;
}