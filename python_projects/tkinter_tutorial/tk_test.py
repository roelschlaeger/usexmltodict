import sys
if sys.version_info < (3, 0):
    raise Exception("Must be run from Python 3+")
# short test of TkAgg
# from http://matplotlib.org/users/shell.html
from pylab import plot, xlabel
plot([1, 2, 3, 2, 1])
xlabel('Hi Mom!')
input("Press any key to exit")
