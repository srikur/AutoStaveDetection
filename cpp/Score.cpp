#include "Utilities.h"
#include "Score.h"

Score::Score(FilePath scorePath, FileType fileType) {
    /* Load the score from the file */
    if (fileType == FileType::PDF) {
        std::cout << "Loading PDF score from " << scorePath << std::endl;

        /* Get current executing path */
        char cwd[1024];
        getcwd(cwd, sizeof(cwd));
        std::string currentPath(cwd);

        /* Convert the PDF to PNG */
        int numPages = Utilities::ConvertPDF(scorePath, currentPath + "/temp");
        if (numPages <= 0) {
            std::cerr << "Could not convert PDF to PNG" << std::endl;
            return;
        }
        std::cout << "Converted PDF to " << numPages << " PNGs" << std::endl;

        /* Load each page */
        for (int i = 0; i < numPages; i++) {
            FilePath pagePath = currentPath + "/temp/page" + std::to_string(i) + ".png";
            Sheet* page = new Sheet(pagePath);
            pages.push_back(page);
        }

        
    } else if (fileType == FileType::PNG) {
        std::cout << "Loading PNG score from " << scorePath << std::endl;
    }
}

Score::~Score() {
    std::cout << "Destroying " << pages.size() << " sheets" << std::endl;
    /* Delete all the pages */
    for (Sheet* page : pages) {
        delete page;
    }
    pages.clear();

    /* Remove all the /temp files that were created and the /temp directory */
    OS os = Utilities::GetOS();
    if (os == OS::WINDOWS) {
        system("del /Q temp\\*");
        system("rmdir temp");
    } else if (os == OS::MAC || os == OS::LINUX) {
        system("rm -f temp/*");
        system("rmdir temp");
    }
}