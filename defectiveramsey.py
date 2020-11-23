#!/usr/bin/env python3

# defectiveramsey.py
# Yunus Emre Demirci
# Date: 13 May 2020
# Requires Python 3.

"""Compute k-defective Ramsey numbers & related extremal graphs.

Command-line usage: defectiveramsey.py [OPTIONS] k a b class"""

import isograph   # for dot_str, isomorphic
import gengraph  # for extremals
import sys        # for argv, exit, stderr
import getopt     # for error, getopt
import time       # for time
import json     # for representation


# ----------------------------------------------------------------------
# Finding k-Sparse Ramsey Numbers & Extremal Graphs
# ----------------------------------------------------------------------

def readgraphs(filename):
    """Return base graphs with array representation.

    Read text in "filename" and convert it array.
    Assume "base.txt" is a txt file and 
    "[[[3, 4, 5], [3, 4, 5], [5], [0, 1, 5], [0, 1], [0, 1, 2, 3]]]"
    >>> readgraphs(base.txt)
    baseg = [[[3, 4, 5], [3, 4, 5], [5], [0, 1, 5], [0, 1], [0, 1, 2, 3]]]
    """
    text = open(filename, "r")
    base = text.read()
    text.close()
    baseg = json.loads(base)
    return baseg 


def print_extremals(k, a, b, graphclass, basegraphs=None):
    """Print R^C_k(a,b) + extremal graphs in DOT language.

    Prints, one on each line, pairs of the form
    u v, where u is an integer from 0 to R^C_k(a,b), and v is the number
    of counterexample graphs of order u.

    Arguments:
    k -- nonnegative int; the "k" in R_k(a,b)
    a -- nonnegative int; the "a" in R^C_k(a,b)
    b -- nonnegative int; the "b" in R^C_k(a,b)
    graphclass -- string; the "C" in R^C_k(a,b)
    basegraphs -- string; the file contains base graphs. DEFAULT; NONE.

    See isograph.py for our graph representation.

    >>> print_extremals(0, 2, 2, bip)
    Finding R^BIP_0(2,2)
    <BLANKLINE>
    1 extremal graph(s):
    <BLANKLINE>
    graph r0_2_2e1 {
        1;
    }
    <BLANKLINE>
    R^BIP_0(2,2) = 2
    1 extremal graph(s)
    """
    assert k >= 0
    assert a >= 0
    assert b >= 0

    print("Finding R^BIP_"+str(k)+"("+str(a)+","+str(b)+")")
    print()

    n, gs = gengraph.extremals(k, a, b, graphclass, basegraphs)


    print()
    print(len(gs), "extremal graph(s):")
    print()
    graphbasename = "r"+str(k)+"_"+str(a)+"_"+str(b)+"e"
    gcount = 0
    for g in gs:
        gcount += 1
        graphname = graphbasename + str(gcount)
        print(isograph.dot_str(g, graphname))
        print()
    print("R^BIP_"+str(k)+"("+str(a)+","+str(b)+") = "+str(n))
    print(len(gs), "extremal graph(s)")

    
# ----------------------------------------------------------------------
# Main program
# ----------------------------------------------------------------------


class UsageError(Exception):

    """Exception class for command-line usage errors.

    >>> isinstance(UsageError(""), Exception)
    True
    >>> UsageError("abc").msg
    'abc'

    """

    def __init__(self, msg):
        """Create UsageError object with the given message."""
        self.msg = msg


def main(argv=None):
    """Print R^C_k(a,b) & extremal graphs, based on command-line options.

    Argument argv is an optional list or tuple of strings, in the format
    of sys.argv (which is its default value).
    """
    tic = time.time()

    if argv is None:
        argv = sys.argv

    printcounterexamples = True
    readbasetxt=False
    try:
        try:
            optlist, args = getopt.getopt(argv[1:], "b",
                ["base"])
        except getopt.error as msg:
            raise UsageError(msg)
        for o, a in optlist:
            if o in ["-b", "--base"]:
                readbasetxt=True
            else:
                assert False, "unhandled option"
        if len(args) != 4:
            raise UsageError("Must have exactly 4 arguments")
        try:
            k = int(args[0])
            a = int(args[1])
            b = int(args[2])
            graph_class=args[3]
        except:
            raise UsageError("Arguments must be integers")
    except UsageError as err:
        print(argv[0]+":", err.msg, file=sys.stderr)
        return 2

    base=None
    if readbasetxt:
        base=readgraphs("base.txt")
    filename = "R^" + graph_class + "_" + str(k) + "def_" + str(a) + "dense_" + str(b) + "sparse.txt"
    f= open(filename,"w")
    sys.stdout = f
    print_extremals(k, a, b, graph_class, basegraphs=base)
    print("running time:" + str(time.time() - tic) + "sec")
    f.close()
    return 0


# Execute main() if running as program, not if imported as module
if __name__ == "__main__":
    sys.exit(main())

