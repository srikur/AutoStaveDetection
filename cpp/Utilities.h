#pragma once

#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>
#include <unistd.h>
#include <fstream>
#include <memory>

// OpenCV
#include <opencv2/opencv.hpp>

using std::string;

typedef std::string FilePath;
enum class FileType { PDF, PNG };
enum class OS { WINDOWS, MAC, LINUX };

namespace Utilities {

    extern int ConvertPDF(FilePath pdfPath, FilePath outputPath);
    extern OS GetOS();

    /* Function to call convert_pdf_to_png.py with the PDF path as the first argument. Returns the exit code of the call, which is the number of pages created */
    int ConvertPDF(FilePath pdfPath, FilePath outputPath);

    /* Function to get the current operating system */
    OS GetOS();
}