#!/usr/bin/env python3

# gengraph.py
# Yunus Emre Demirci
# Date: 13 May 2020
# Requires Python 3.

"""Functions for finding generalized Ramsey numbers & related extremal
graphs.

CONVENTIONS

See isograph.py for our graph representation. A set is represented as a
sorted list or tuple of its elements.

*Predicates* in this file are functions taking a graph and a set of
vertices of that graph, and returning bool. Given a predicate f, and a
graph g, we say a set s of vertices of g is an *f-set* in g if f(g, s)
is True.

An *induced-hereditary* predicate is a predicate f such that, if h is an
induced subgraph of a graph g, and s is a set of vertices of h, then s
is an f-set in h iff s is an f-set in g.

Given predicates f1 & f2 and nonnegative integers b1 & b2, a
*counterexample* graph is a graph that contains no f1-set of order b1
and no f2-set of order b2. In other words, it is a counterexample to the
statement that every graph contains either an f1-set of order b1 or an
f2-set of order b2.

An *extremal* graph is a counterexample graph of maximum order.

Predicates:
is_independent(g, s)
    Return bool: True if s is an independent set in graph g.
is_clique(g, s)
    Return bool: True if s induces a complete subgraph of graph g.

Checking for f-Sets:
has_fset(f, b, g)
    Return bool: True if graph g contains an f-set of order b.
has_fset_with_last(f, b, g)
    Return bool: True if graph g contains an f-set of order b that
    contains vertex n-1 of g.

Finding Extremal Graphs:
extremals(f1, f2, b1, b2, printflag=None)
    f1, f2 are induced-hereditary predicates. Return (n, gs), where n is
    the least order for which no counterexample graphs exist (and so n-1
    is the order of all extremal graphs), and gs is a list of all
    extremal graphs (exactly one from each isomorphism class). If
    printflag is True, prints, one on each line, pairs of the form u v,
    where u is an integer from 0 to n, and v is the number of
    counterexample graphs of order u.

"""

import isograph   # for graphs, isomorphic, powerset, unique_iso
import itertools  # for combinations, count
import sys        # for argv, exit


# ----------------------------------------------------------------------
# Predicates
# ----------------------------------------------------------------------

def is_k_sparse(g, s, k):
    for v in s:
        d = 0
        for x in g[v]:
            if x in s:
                d += 1
                if d > k:
                    return False
    return True

def is_k_dense(g, s, k):
    for v in s:
        d = 0
        for x in s:
            if x != v and x not in g[v]:
                d += 1
                if d > k:
                    return False
    return True
    
# ----------------------------------------------------------------------
# Checking for f-Sets
# ----------------------------------------------------------------------


def has_set_size_k(g, a, k, sparse_or_dense):
    """Return True if g contains k sparse or dense set (depend on sparse_or_dense) 
    of order a.

    Arguments:
    k -- nonnegative int
    a -- nonnegative int
    g -- graph
    sparse_or_dense -- boolean
      We search for an order-b k dense or sparse-set. If sparse_or_dense is True we
    looking for dense set, otherwise sparse set.

    See isograph.py for our graph representation.

    >>> g = [ [3], [3], [3], [0,1,2] ]
    >>> has_fset_with_last(0, 2, g, True)
    True
    >>> has_fset_with_last(0, 2, g, False)
    True
    """
    if a < 0:
        return False

    n = len(g)
    if a > n:
        return False

    for s in itertools.combinations(range(n), a):
        if sparse_or_dense and is_k_sparse(g, s, k):
            return True
        elif not(sparse_or_dense) and is_k_dense(g, s, k):
            return True
    return False


def has_set_size_k_with_last(k, a, g, sparse_or_dense):
    """Return True if g contains k sparse or dense set (depend on sparse_or_dense) 
    of order a containing vertex n-1.

    Arguments:
    k -- nonnegative int
    a -- nonnegative int
    g -- graph
    sparse_or_dense -- boolean
      We search for an order-a k dense or sparse-set. If sparse_or_dense is True we
    looking for dense set, otherwise sparse set.

    See isograph.py for our graph representation.

    >>> g = [ [3], [3], [3], [0,1,2] ]
    >>> has_fset_with_last(0, 2, g, True)
    True
    >>> has_fset_with_last(0, 2, g, False)
    False
    """
    if a < 1:
        return False

    n = len(g)
    if a > n:
        return False

    for ss in itertools.combinations(range(n-1), a-1):
        s = ss + (n-1,)
        if sparse_or_dense and is_k_sparse(g, s, k):
            return True
        elif not(sparse_or_dense) and is_k_dense(g, s, k):
            return True
    return False


# ----------------------------------------------------------------------
# Finding Extremal Graphs
# ----------------------------------------------------------------------


def _counterexamples_zero(a, b, k):
    """Yield all counterexample graphs of order zero.

    Arguments:
    a -- nonnegative int
    b -- nonnegative int
    b -- nonnegative int
    See isograph.py for our graph representation.

    """
    gs = list(isograph.graphs(0))  # list of all graphs of order 0
    for g in gs:
        if not has_set_size_k(g, a, k, True) and not has_set_size_k(g, b, k, False):
            yield g

def graph_check_with_last(g, graphclass):

    def bipartite_check_with_last(g):
        n=len(g)
        if n < 3:
            return True
        colorarr = [-1] * n
        colorarr[n-1] = 0
        queue = []
        queue.append(n-1)
        while queue:
            u = queue.pop()
            for v in g[u]:
                if colorarr[v] == colorarr[u]:
                    return False
                elif colorarr[v] == -1:
                    colorarr[v] = 1 - colorarr[u]
                    queue.append(v)
        return True

    def perfect_check_with_last(g):

        def is_cycle_with_last(g, s):
            n=len(g)
            if n<3:
                return False
            sliste=list(s)
            t=len(sliste)
            colorarr = [-1] * (n)
            colorarr[sliste[0]] = 0
            p=1
            queue = []
            queue.append(sliste[0])
            while queue:
                u = queue.pop()
                w=[]
                w=[x for x in g[u] if x in s]
                if len(w)!=2:
                    return False
                for v in w:
                    if colorarr[v] == -1:
                        colorarr[v]=0
                        p=p+1
                        queue.append(v)
            if p==t:
                return True
            return False

        def is_cycle_complement_with_last(g,s):
            newg=[]
            n=len(g)
            for i in range(n):
                newg.append([x for x in range(n) if (x not in g[i] and x!=i)])
            return is_cycle_with_last(newg,s)

        n=len(g)
        if n < 5:
            return True

        for m in range(5, n+1, 2):
                for vset in itertools.combinations(range(n-1), m-1):
                    s = vset + (n-1,)
                    if is_cycle_with_last(g,s):
                        return False
                    if is_cycle_complement_with_last(g,s):
                        return False
        return True
    
    if graphclass == "bip":
        return bipartite_check_with_last(g)
    if graphclass == "pg":
        return perfect_check_with_last(g)
    if graphclass == "all":
        return True


def _counterexamples_up(k, a, b, graphclass, n, old):
    
    def counterexamples_up_big_list(k, a, b, graphclass, n, old):
        for oldg in old:
            for vset in isograph.powerset(range(n-1)):
                g = oldg + [list(vset)]
                for v in vset:
                    g[v] = g[v]+[n-1]
                if (graph_check_with_last(g, graphclass)):
                    if (not has_set_size_k_with_last(k, a, g, True)) and (not has_set_size_k_with_last(k, b, g, False)):
                        yield g

    return isograph.unique_iso(counterexamples_up_big_list(k, a, b, graphclass, n, old))


def extremals(k, a, b, graphclass, basegraphs=None):

    print("Order & number of counterexample graphs:")
    m=0
    if basegraphs==None:
        gs = list(_counterexamples_zero(a, b, k))
    else:
        gs= basegraphs
        m = len(gs[0])
    howmany = len(gs)
    print(m, howmany)
    if howmany == 0:
        return (0, [])
    for n in itertools.count(m+1):
        oldgs = gs
        gs = list(_counterexamples_up(k, a, b, graphclass, n, oldgs))
        howmany = len(gs)
        print(n, howmany)
        if howmany == 0:
            return (n, oldgs)
