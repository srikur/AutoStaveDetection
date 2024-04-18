#include "Utilities.h"
#include "Score.h"

using std::unique_ptr;

int main(int argc, char *argv[]) {

    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <score: PDF or PNG>" << std::endl;
        return 1;
    }

    FilePath scorePath = argv[1];

    /* Determine the file type */
    FileType fileType;
    // Cannot rely on the file extension to determine the file type. Need to check the file contents.
    // PDFS begin with "%PDF" (hex 25 50 44 46)
    // PNGs begin with "\x89PNG\r\n\x1a\n" (hex 89 50 4e 47 0d 0a 1a 0a)
    std::ifstream file(scorePath, std::ios::binary);
    char header[8];
    file.read(header, 8);
    file.close();

    if (static_cast<unsigned char>(header[0]) == 0x25 && 
        static_cast<unsigned char>(header[1]) == 0x50 && 
        static_cast<unsigned char>(header[2]) == 0x44 && 
        static_cast<unsigned char>(header[3]) == 0x46) {
        fileType = FileType::PDF;
    } else if (static_cast<unsigned char>(header[0]) == 0x89 && 
               static_cast<unsigned char>(header[1]) == 0x50 && 
               static_cast<unsigned char>(header[2]) == 0x4e && 
               static_cast<unsigned char>(header[3]) == 0x47 && 
               static_cast<unsigned char>(header[4]) == 0x0d && 
               static_cast<unsigned char>(header[5]) == 0x0a && 
               static_cast<unsigned char>(header[6]) == 0x1a && 
               static_cast<unsigned char>(header[7]) == 0x0a) {
        fileType = FileType::PNG;
    } else {
        std::cerr << "Invalid file type" << std::endl;
        return 1;
    }

    Score* score = new Score(scorePath, fileType);
    std::cout << "Score object succesfully created!" << std::endl;

    delete score;
    return 0;
}