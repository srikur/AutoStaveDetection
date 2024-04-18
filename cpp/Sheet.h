/*
    * Sheet.h
    *
    *  A sheet of music. Contains the notes and other information about the music.
*/

#pragma once

#include "Utilities.h"

class Sheet {
    public:
        Sheet(FilePath pagePath);
        Sheet(const Sheet& other) = delete;
        Sheet& operator=(const Sheet& other) = delete;
        ~Sheet();

    private:
        // PNG image data
        cv::Mat* image;
};