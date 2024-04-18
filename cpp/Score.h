/* 
    * Score.h
    * 
    * Contains information about the entire sheet music. Pages of the score are Sheet objects, which contain the notes and other information about the music.
    *
*/

#pragma once

#include "Utilities.h"
#include "Sheet.h"

class Score {
    public:
        Score(FilePath scorePath, FileType fileType);
        Score(const Score& other) = delete;
        Score& operator=(const Score& other) = delete;
        ~Score();
    private:
        std::vector<Sheet*> pages;
};