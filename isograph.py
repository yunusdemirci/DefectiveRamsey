#!/usr/bin/env python3

# isograph.py
# Glenn G. Chappell
# Date: 26 Aug 2016
# Requires Python 3.

"""Functions for dealing with finite, simple graphs & graph isomorphism.

CONVENTIONS

Functions in this module deal with finite, simple graphs. We represent a
graph using a list of adjacency lists. The length of a list representing
a graph is the order of the graph. Indices are vertex labels: 0..n-1.
Item k is a sorted list of labels of neighbors of vertex k. A graph with
0 vertices is allowable.

For example, here is the representation of K_4-e, where e is (0,3):

    [ [1,2], [0,2,3], [0,1,3], [1,2] ]

We represent a set of vertices using a list or tuple of the labels of
the vertices in the set, in sorted order. We do not use the Python "set"
facility.

INTERFACE

Set/Combinatorics Tools:
powerset(iterable)
    Generator. Yield all subsets of given finite iterable.

General Graph Tools:
is_graph(g)
    Return bool: True if g is a graph. g may be of any type.
dot_str(g, graphname=None, maxlen=72)
    Return multi-line string holding representation of graph g in DOT
    language. String does not end with newline. graphname is optional
    string holding name of graph. maxlen is maxmimum allowable line
    length in returned string.
graphs(n)
    Generator. Yield all (vertex-labeled) graphs of order n.
clique_number(g)
    Return clique number of graph g.

Graph Isomorphism Tools:
isomorphic(g, h)
    Return bool: True if graphs g, h are isomorphic.
unique_iso(gs)
    Generator. Given iterable yielding graphs, yield first from each
    isomorphism class.
graphs_iso(n)
    Generator. Yield graphs of order n, one in each isomorphism class.
graphs_conn_iso(n)
    Generator. Yield graphs of order n, one in each isomorphism class
    of connected graphs.

"""

import itertools  # for chain, combinations, islice, permutations
import sys        # for argv, exit


# ----------------------------------------------------------------------
# Set/Combinatorics Tools
# ----------------------------------------------------------------------


def powerset(iterable):
    """Yield all subsets of given finite iterable.

    Based on code from itertools docs.

    Arguments:
    iterable -- finite iterable
      We yield all subsets of the set of all items yielded by iterable.

    >>> sorted(list(powerset([1,2,3])))
    [(), (1,), (1, 2), (1, 2, 3), (1, 3), (2,), (2, 3), (3,)]

    """
    s = list(iterable)
    return itertools.chain.from_iterable( itertools.combinations(s, r)
        for r in range(len(s)+1) )


# _partition_perms - not part of public interface of module
def _partition_perms(parts, n):
    """Yield, as lists, permutations of range(n) that respect parts.

    Arguments:
    parts -- list/tuple of lists/tuples of ints in range(n)
      Each item is a "part". Parts, considered as sets, must be
      pairwise-disjoint. An integer not in any part, is considered to
      lie in a part of size 1. Permutations yielded are those that keep
      each int within its part.
    n -- the "n" in the description of argument parts

    >>> sorted(list(_partition_perms([[0,2], [4,1]], 5)))
    [[0, 1, 2, 3, 4], [0, 4, 2, 3, 1], [2, 1, 0, 3, 4], [2, 4, 0, 3, 1]]

    """
    if not parts:
        yield list(range(n))
        return
    prt = parts[0]
    if len(prt) <= 1:
        for p in _partition_perms(parts[1:], n):
            yield p
        return
    for baseperm in _partition_perms(parts[1:], n):
        for newperm in itertools.permutations(prt):
            p = baseperm[:]
            for i in range(len(prt)):
                p[prt[i]] = newperm[i]
            yield p


# ----------------------------------------------------------------------
# General Graph Tools
# ----------------------------------------------------------------------


def is_graph(g):
    """Return True if g is a representation of a graph.

    Arguments:
    g -- value of any type
      Return value is True if g is a graph representation.

    See beginning of this file for our graph representation.

    >>> is_graph("Hello")
    False
    >>> is_graph([])
    True
    >>> is_graph([ [] ])
    True
    >>> is_graph([ [0] ])
    False
    >>> is_graph([ [1,2], [0,2,3], [0,1,3], [1,2] ])
    True
    >>> is_graph([ [1], [] ])
    False

    """
    # g must be list
    if type(g) is not list:
        return False
    n = len(g)

    # Neighbors must all be vertices, and given in order, no dups
    for adjl in g:
        # Each adj list must be of type list
        if type(adjl) is not list:
            return False
        # Neighbors must be ints in [0,n)
        for v in adjl:
            if type(v) is not int:
                return False
            if v < 0 or v >= n:
                return False
        # Check adj list sorted & no duplicates
        # (Do *after* above so we know nbrs can be ordered & hashed)
        if adjl != sorted(list(set(adjl))):
            return False

    # Edges must be symmetric, and no loops
    for v1 in range(n):
        if v1 in g[v1]:
            return False
        for v2 in range(v1):
            e12 = v2 in g[v1]
            e21 = v1 in g[v2]
            if e12 != e21:
                return False
    return True


def dot_str(g, graphname=None, maxlen=None):
    """Return string form of graph g in DOT language. No newline @ end.

    Given graphname is included if it is passed. Vertices are numbered
    1 .. n; the vertex with internal label k is handled in the output as
    k+1. Vertices are listed first, then edges, in lexicographic order.

    Arguments:
    g -- graph to represent in DOT language
    graphname -- optional string holding name of graph
    maxlen -- optional maximum line length (default 72)

    See beginning of this file for our graph representation.

    >>> print(dot_str([ [1,2], [0,2,3], [0,1,3], [1,2] ], "mygraph"))
    graph mygraph {
        1; 2; 3; 4;
        1 -- 2; 1 -- 3; 2 -- 3; 2 -- 4; 3 -- 4;
    }

    >>> print(dot_str([ [1], [0] ]))
    graph {
        1; 2;
        1 -- 2;
    }

    """
    # Helper class StringMaker, for creating a string consisting of
    # indented lines containing blank-separated items, with a given
    # maximum line length. Output stored in member str.
    class StringMaker:
        def __init__(self, theMaxlen):
            self.maxlen = theMaxlen
            self.line = ""
            self.str = ""

        def new_line(self):
            if self.line:
                self.str += self.line + "\n"
            self.line = ""

        def add_to_line(self, s):
            if self.line and len(self.line + " " + s) > self.maxlen:
                self.new_line()
            if not self.line:
                self.line = "    " + s
                return
            self.line += " " + s

    # Initialization
    if maxlen is None:
        maxlen = 72
    sm = StringMaker(maxlen)

    # Add vertex labels
    for i in range(len(g)):
        sm.add_to_line(str(i) + ";")
    sm.new_line()

    # Add edges
    for i in range(len(g)):
        for j in g[i]:
            if i < j:
                sm.add_to_line(str(i) + " -- " + str(j) + ";")
    sm.new_line()
    sm.add_to_line(str(g))
    sm.new_line()

    # Construct final string
    retval = "graph "
    if graphname is not None:
        retval += graphname + " "
    retval += "{\n" + sm.str + "}"
    return retval


def graphs(n):
    """Yield all (vertex-labeled) n-vertex graphs.

    Has a partially unrolled loop, for speed.

    Arguments:
    n -- order of graphs to yield

    See beginning of this file for our graph representation.

    >>> list(graphs(0))
    [[]]
    >>> list(graphs(1))
    [[[]]]
    >>> sorted(list(graphs(3))) #doctest: +NORMALIZE_WHITESPACE
    [[[], [], []], [[], [2], [1]], [[1], [0], []], [[1], [0, 2], [1]],
    [[1, 2], [0], [0]], [[1, 2], [0, 2], [0, 1]], [[2], [], [0]],
    [[2], [2], [0, 1]]]
    >>> len(list(graphs(5)))
    1024
    >>> all(map(is_graph, graphs(5)))
    True

    """
    assert n >= 0

    # Special cases for small vertex sets
    if n <= 2:
        if n == 0:
            yield []
            return
        if n == 1:
            yield [ [] ]
            return
        if n == 2:
            yield [ [], [] ]
            yield [ [1], [0] ]
            return

    # Make generator yielding all possible edges.
    # If a < b < c, then we yield edge (a,b) before (a,c).
    # If b < c < a, then we yield edge (b,a) before (c,a).
    # As a result, we will construct graph representations having sorted
    # adjacency lists, which our graph representation requires.
    alledges = ( (j, i) for i in range(n) for j in range(i) )

    # Generate all graphs
    # We unroll the portion of the loop dealing with edges (0,1), (0,2)
    for edges in powerset(itertools.islice(alledges, 2, None)):
        # unrolling for edges (0,1) and (0,2)
        g = [ [] for v in range(n) ]
        for e in edges:
            g[e[0]].append(e[1])
            g[e[1]].append(e[0])
        yield g

        # Add edge (0,1)
        g2 = g[:]
        # We can't use .insert below, since we don't want to modify the
        # items in the list we have (shallowly!) copied.
        g2[0] = [1]+g2[0]
        g2[1] = [0]+g2[1]
        yield g2

        # Add edge (0,2)
        g3 = g[:]
        g3[0] = [2]+g3[0]
        g3[2] = [0]+g3[2]
        yield g3

        # Add edges (0,1) and (0,2)
        g4 = g3[:]  # Not copied from g!
        g4[0] = [1]+g4[0]
        g4[1] = [0]+g4[1]
        yield g4


def clique_number(g):
    """Returns the clique number of graph g.

    Arguments:
    g -- a graph

    >>> g = [[1,2,3],[0,3],[0,3],[0,1,2]]
    >>> clique_number(g)
    3
    >>> g = [[1,4],[0,2],[1,3],[2,4],[3,0]]
    >>> clique_number(g)
    2
    >>> g = [[1,4,5],[0,2,5],[1,3,5],[2,4,5],[3,0,5],[0,1,2,3,4]]
    >>> clique_number(g)
    3
    >>> g = [[],[],[],[],[],[],[],[],[],[],[],[]]
    >>> clique_number(g)
    1

    """
    def clique_number_with(g, n, s, v):
        """Returns max order of clique containing given set.

        Parameters:
        g - a graph
        n - the order of g
        s - a set of vertices of g that forms a clique in g
        v - a vertex of g; index greater than all vertices in s

        Returns:
        Max order of clique in g containing all vertices in s
        and zero or more vertices with index v or higher.

        """
        for x in range(v, n):  # Look for vert to add to clique s
            for z in s:        # try all z in s to see if x is adjacent
                if z not in g[x]:
                    break      # No - go to next x
            else:              # Found an x; use it
                if x+1 == n:
                    return len(s)+1
                c1 = clique_number_with(g, n, s, x+1)
                s.append(x)
                c2 = clique_number_with(g, n, s, x+1)
                s.pop()
                return max(c1, c2)
        return len(s)  # No vert found; s is biggest

    n = len(g)
    if n < 2:
        return n
    return clique_number_with(g, n, [], 0)


# ----------------------------------------------------------------------
# Graph Isomorphism Tools
# ----------------------------------------------------------------------


# Note: In this section we use an ad hoc algorithm here to determine
# whether two graphs are isomorphic. Replacing this with some published
# isomorphism algorithm would be a good idea.


# _degree_verts - not part of public interface of module
def _degree_verts(g):
    """Given graph, return dict mapping degrees of nbrs to verts.

    Keys in return value are tuples giving numbers of neighbors with
    each possible degree. Associated values are lists of vertices whose
    neighbors have the given degrees.

    Keys whose associated value would be [] are not in the dict.

    Arguments:
    g -- a graph

    >>> _degree_verts([])
    {}
    >>> _degree_verts([[]])
    {(0,): [0]}
    >>> _degree_verts([ [1,2], [0,2,3], [0,1,3], [1,2] ])
    {(0, 0, 2, 1): [1, 2], (0, 0, 0, 2): [0, 3]}

    In the example above, the key (0, 0, 2, 1) means:
    - 0 neighbors of degree 0
    - 0 neighbors of degree 1
    - 2 neighbors of degree 2
    - 1 neighbor of degree 3
    The associated value is [1, 2]. This means that the above describes
    the neighborhoods of vertices 1 and 2.

    See beginning of this file for our graph representation.

    """
    n = len(g)
    # degs = map(len, g) is a tiny bit slower than the following line
    degs = [ len(g[v]) for v in range(n) ]
    dv = dict()
    for v in range(n):
        degnbr = [0] * n
        for w in g[v]:
            degnbr[degs[w]] += 1
        # Could use defaultdict below, but it does not seem to be faster
        dv.setdefault(tuple(degnbr), []).append(v)
    return dv


def isomorphic(g, h):
    """Return True if graphs g, h are isomorphic.

    Uses sorting by degree sequences of neighborhoods.

    Arguments:
    g -- a graph
    h -- another graph

    See beginning of this file for our graph representation.

    >>> g0 = []
    >>> g1 = [[]]
    >>> g2a = [[],[]]
    >>> g2b = [[1],[0]]
    >>> g8a = [[2,4,5,6], [3,4,5,7], [0,4,6,7], [1,5,6,7], [0,1,2,6],
    ... [0,1,3,7], [0,2,3,4,7], [1,2,3,5,6]]
    >>> g8b = [[2,4,5,6,7], [3,4,5,7], [0,4,6,7], [1,5,6,7], [0,1,2,6],
    ... [0,1,3,7], [0,2,3,4], [0,1,2,3,5]]
    >>> g8c = [[2,4,5,6,7], [3,4,5,7], [0,4,6,7], [1,5,6,7], [0,1,2,6],
    ... [0,1,3,7], [0,2,3,4], [0,1,2,3]]
    >>> isomorphic(g0, g0)
    True
    >>> isomorphic(g0, g1)
    False
    >>> isomorphic(g2a, g2a)
    True
    >>> isomorphic(g2b, g2b)
    True
    >>> isomorphic(g2a, g2b)
    False
    >>> isomorphic(g8a, g8b)
    True
    >>> isomorphic(g8a, g8c)
    False

    """
    # Note: for some applications, it can speed things up to
    # check equality of orders here.
    #n = len(g)
    #if n != len(h):
    #    return False

    # Make dicts of verts of each nbr-degree, for graphs g, h
    gdv = _degree_verts(g)
    hdv = _degree_verts(h)

    # Compare nbr-degree sequences
    if len(gdv) != len(hdv):
        return False
    for k in gdv:
        if k not in hdv:
            return False
        if len(gdv[k]) != len(hdv[k]):
            return False
    # Now we know that g, h have the same order

    # Sort (& renumber) verts by nbr-degree
    gvp = list(itertools.chain.from_iterable(
        ( gdv[k] for k in sorted(gdv.keys()) )
        ))
    g = [ sorted([gvp.index(w) for w in g[v]]) for v in gvp ]
    hvp = list(itertools.chain.from_iterable(
        ( hdv[k] for k in sorted(hdv.keys()) )
        ))
    h = [ sorted([hvp.index(w) for w in h[v]]) for v in hvp ]

    # Remake dict of verts of each nbr-degree, for g
    gdv = _degree_verts(g)

    # Try all permutations of the vertex set of graph g that take each
    # vertex to a vertex whose neighbors have the same degree sequence.
    n = len(g)
    hsets = list(map(set, h))
    for p in _partition_perms(list(gdv.values()), n):
        for v in range(n):
            if hsets[p[v]] != set([p[w] for w in g[v]]):
                # A set comprehension would be nice above
                break
        else:
            return True
    return False


def unique_iso(gs):
    """Given iterable yielding graphs, yield 1st from each iso. class.

    For example, if gs yields graphs a, b, c, d, e, and a & c are
    isomorphic, and also b & e are isomorphic, then this function yields
    a, b, d.

    Uses sorting by degree sequences of neighborhoods.

    Arguments:
    gs -- iterable yielding graphs

    See beginning of this file for our graph representation.

    >>> result = sorted(list(unique_iso(graphs(3))))
    >>> result #doctest: +NORMALIZE_WHITESPACE
    [[[], [], []], [[1], [0], []], [[1, 2], [0], [0]],
    [[1, 2], [0, 2], [0, 1]]]
    >>> len(list(unique_iso(graphs(5))))
    34

    """
    # For speed, instead of using a separate isomorphism-checking
    # function, we use our own helper function ck_iso. This checks
    # isomorphism of 2 graphs, given the graphs and their _degree_verts
    # output.
    def ck_iso(gc, gcdv, hc, hcdv):
        # Compare nbr-degree sequences
        if len(gcdv) != len(hcdv):
            return False
        for k in gcdv:
            if k not in hcdv:
                return False
            if len(gcdv[k]) != len(hcdv[k]):
                return False
        # Now we know that gc, hc have the same order

        # Try all permutations of the vertex set of graph g that take
        # each vertex to a vertex whose neighbors have the same degree
        # sequence.
        n = len(gc)
        hcsets = list(map(set, hc))
        for p in _partition_perms(list(gcdv.values()), n):
            for v in range(n):
                if hcsets[p[v]] != set([p[w] for w in gc[v]]):
                    # A set comprehension would be nice above
                    break
            else:
                return True
        return False

    # canons is list of pairs: (gc, gcdv)
    canons = []

    for g in gs:
        gdv = _degree_verts(g)
        gvp = list(itertools.chain.from_iterable(
            ( gdv[k] for k in sorted(gdv.keys()) )
            ))

        # Make semi-canonical form of g
        gc = [ sorted([gvp.index(w) for w in g[v]]) for v in gvp ]
        gcdv = _degree_verts(gc)

        # Check isomorphism w/ each graph in canons
        for hc, hcdv in canons:
            if ck_iso(gc, gcdv, hc, hcdv):
                break
        else:
            canons.append((gc, gcdv))
            yield g


def graphs_iso(n):
    """Yield graphs of order n, one in each isomorphism class.

    Arguments:
    n -- order of graphs to yield

    >>> list(graphs_iso(0))
    [[]]
    >>> list(graphs_iso(1))
    [[[]]]
    >>> sorted(list(graphs_iso(2)))
    [[[], []], [[1], [0]]]
    >>> [ len(list(graphs_iso(n))) for n in range(6) ]
    [1, 1, 2, 4, 11, 34]

    """
    assert n >= 0
    for g in unique_iso(graphs(n)):
        yield g


def graphs_conn_iso(n):
    """Yield graphs of order n, one in each connected isomorphism class.

    Arguments:
    n -- order of graphs to yield

    >>> list(graphs_conn_iso(0))
    [[]]
    >>> list(graphs_conn_iso(1))
    [[[]]]
    >>> list(graphs_conn_iso(2))
    [[[1], [0]]]
    >>> [ len(list(graphs_conn_iso(n))) for n in range(7) ]
    [1, 1, 1, 2, 6, 21, 112]

    """
    def graphs_conn_helper(n):
        for oldg in graphs_conn_iso(n-1):
            for s in powerset(range(n-1)):
                if s == ():
                    continue
                g = oldg + [list(s)]
                for v in s:
                    g[v] = g[v] + [n-1]
                    # NOT g[v] += ... or g[v].append(...)
                    #  to avoid changing items in oldg
                yield g

    assert n >= 0
    if n >= 3:
        for g in unique_iso(graphs_conn_helper(n)):
            yield g
    elif n == 2:
        yield [ [1], [0] ]
    elif n == 1:
        yield [ [] ]
    else:  # n == 0
        yield []


# ----------------------------------------------------------------------
# Main program
# ----------------------------------------------------------------------


def main(argv=None):
    """Run doctests; verbose mode if argv[1] is "--Test".
    If argv is not given, then sys.argv is used.

    """
    if argv is None:
        argv = sys.argv

    import doctest
    verbose = (len(argv) >= 2 and argv[1] == "--Test")
    if verbose:
        print("Running doctests (verbose mode)")
    else:
        print("Running doctests")
    doctest.testmod(verbose=verbose)
    return 0


# Execute main() if running as program, not if imported as module
if __name__ == "__main__":
    sys.exit(main())

