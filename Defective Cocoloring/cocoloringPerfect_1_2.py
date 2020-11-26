import json     # for representation
import sys        # for argv, exit, stderr
import itertools

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

def is_g_k_def_two_colorable(g, k, r):
    for r in range(len(g)):
        for s in itertools.combinations(range(len(g)), r):
            ss=[x for x in range(len(g)) if x not in s]
            if (is_k_defective(g, s, k) and is_k_defective(g, ss, k)):
                return True
    return False

def main(argv=None):
    base = readgraphs("R^PG_1def_5dense_5sparse_8vertex.txt")
    f = open("C_1^PG_2_8vertex.txt","w")
    sys.stdout = f
    for g in base:
        if not is_g_k_def_two_colorable(g, 1, 4):
            print(g)
    f.close()
    return 0


# Execute main() if running as program, not if imported as module
if __name__ == "__main__":
    sys.exit(main())

