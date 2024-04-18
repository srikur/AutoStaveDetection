cmake_minimum_required(VERSION 3.12)
set(CMAKE_CXX_STANDARD 17)
project(NoteWeaver)

find_package(OpenCV REQUIRED)

# Source Files
set(SOURCES
    main.cpp
    cpp/Score.cpp
    cpp/Sheet.cpp
    cpp/Utilities.cpp
)

# Header Files
set(HEADERS
    cpp/Utilities.h
    cpp/Score.h
    cpp/Sheet.h
)

# Additional Dependencies
set(LIBRARIES
    # Libraries
)

# Include Directories
include_directories(cpp)
include_directories(${OpenCV_INCLUDE_DIRS})

# Create the executable
add_executable(NoteWeaver ${SOURCES} ${HEADERS})

# Link libraries
target_link_libraries(NoteWeaver ${LIBRARIES})
target_link_libraries(NoteWeaver ${OpenCV_LIBS})