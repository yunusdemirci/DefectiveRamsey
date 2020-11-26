import json     # for representation
import sys        # for argv, exit, stderr
from itertools import chain, combinations

def powerset(iterable):
    """
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    xs = list(iterable)
    return chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1))

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

def is_k_sparse(g, s, k):
    for v in s:
        d = 0
        for x in g[v]:
            if x in s:
                d += 1
                if d > k:
                    return False
    return True

def is_k_sparse_compl(g, s, k):
    for v in s:
        d = 0
        for x in s:
            if x != v and x not in g[v]:
                d += 1
                if d > k:
                    return False
    return True

def is_k_defective(g, s, k):
    if is_k_sparse(g, s, k) or is_k_sparse_compl(g, s, k):
        return True
    return False

def is_g_k_def_two_colorable(g, k):
    for r in range(len(g)):
        for s in combinations(range(len(g)), r):
            ss=[x for x in range(len(g)) if x not in s]
            if (is_k_defective(g, s, k) and is_k_defective(g, ss, k)):
                return True
    return False

def union_two_graph(a, b):
    c=a[:]
    for vertex in b:
        c.append([x+len(a) for x in vertex])
    return c

def main(argv=None):
    #Let A be the set of all perfect graphs on 6 vertices that are 2-defective
    A = readgraphs("PG_2def_6set.txt")
    #and B be the set of all graphs on 5 vertices that are not 2-defective
    B = readgraphs("PG_not2def_5set.txt")
    n = 30
    for a in A:
        for b in B:
            g = union_two_graph(a,b)
            #trying all possible edges between two graphs
            for edges in powerset(list(range(n))):
                newg=[vert[:] for vert in g]
                for edge in edges:
                    newg[int(edge / 6)].append(6 + (edge % 5))
                    newg[6 + (edge % 5)].append(int(edge / 6))
                if not(is_g_k_def_two_colorable(newg, 2)):
                    print(newg)
    return 0


# Execute main() if running as program, not if imported as module
if __name__ == "__main__":
    sys.exit(main())

