cmake_minimum_required(VERSION 2.8)
project(permve-ntnu-it3105-module-4)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14")

#set(Boost_USE_STATIC_LIBS    ON)
#set(Boost_USE_MULTITHREADED  ON)
#set(Boost_USE_STATIC_RUNTIME OFF)
#find_package(Boost REQUIRED COMPONENTS mpi serialization)
#include_directories(${Boost_INCLUDE_DIR})

add_executable(2048 2048.cpp board.cpp)
#target_link_libraries(parallel ${Boost_LIBRARIES} ${MPI_LIBRARIES})

