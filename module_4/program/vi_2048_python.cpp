#include "vi_2048_game.h"

#include <boost/python.hpp>

BOOST_PYTHON_MODULE(vi_2048_python)
{
    using namespace boost::python;
    def("configure", vi::configure);
    def("reset_game", vi::reset_game);
    def("step_game", vi::step_game);
}

