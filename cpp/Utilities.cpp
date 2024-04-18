#include "Utilities.h"

int Utilities::ConvertPDF(FilePath pdfPath, FilePath outputPath) {
    /* Call convert_pdf_to_png.py */
    std::string command = "python3 python/convert_pdf_to_png.py " + pdfPath + " " + outputPath;
    system(command.c_str());
    
    /* Count the number of pages created */
    /* Get number of .png files in the directory */
    std::string countCommand = "ls " + outputPath + " | grep -c .png";
    FILE* countPipe = popen(countCommand.c_str(), "r");
    if (!countPipe) {
        std::cerr << "Could not count the number of pages created" << std::endl;
        return -1;
    }
    char countBuffer[128];
    std::string countString;
    while (!feof(countPipe)) {
        if (fgets(countBuffer, 128, countPipe) != NULL) {
            countString += countBuffer;
        }
    }
    pclose(countPipe);
    return std::stoi(countString);
}

OS Utilities::GetOS() {
    #ifdef _WIN32
        return OS::WINDOWS;
    #elif __APPLE__
        return OS::MAC;
    #elif __linux__
        return OS::LINUX;
    #else
        return OS::UNKNOWN;
    #endif
}