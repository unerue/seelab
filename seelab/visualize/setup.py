import numpy as np
from numpy.distutils.misc_util import Configuration


def configuration(parent_package='', top_path=None):
    config = Configuration('visualize', parent_package, top_path)
    config.add_extension(
        '_cython_utils',
        sources=['_cython_utils.pyx'],
        include_dirs=[np.get_include()])

    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup

    setup(**configuration().todict())
