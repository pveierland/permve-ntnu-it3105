cmake_minimum_required(VERSION 2.8)
project(permve-ntnu-it3105-module-4)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14")

find_package(Boost COMPONENTS python)
include_directories(${Boost_INCLUDE_DIR})
link_directories(${Boost_LIBRARY_DIRS})

find_package(PythonLibs 2.7 REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})
link_directories(${PYTHON_LIBRARIES})

PYTHON_ADD_MODULE(
    vi_2048_python
    vi_2048_python.cpp
    vi_2048_game.cpp
    vi_2048_ai.cpp
    vi_2048_board.cpp)

target_link_libraries(vi_2048_python ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})

