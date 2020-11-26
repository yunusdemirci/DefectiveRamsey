using IterTools
using Compose
using Combinatorics
using DataStructures

function union_two_graph(a, b)
    c=a[:]
    for vertex in b
        push!(c, [x + size(a, 1) for x in vertex])
    end
    return c
end

function is_k_sparse(g, s, k)
    for v in s
        d = 0
        for x in g[v]
            if x in s
                d += 1
                if d > k
                    return False
                end
            end
        end
    end
    return True
end

function is_k_sparse_compl(g, s, k)
    for v in s
        d = 0
        for x in s
            if x != v && !(x in g[v])
                d += 1
                if d > k
                    return False
                end
            end
        end
    end
    return True
end

function is_k_defective(g, s, k)
    if is_k_sparse(g, s, k) || is_k_sparse_compl(g, s, k)
        return True
    end
    return False
end

function is_g_k_def_three_colorable(g, k)
    for r in range(len(g))
        for m in range(len(g))
            for s in combinations(range(len(g)), r)
                for ss in combinations([x for x in range(len(g)) if !(x in s)], m)
                    sss=[x for x in range(len(g)) if !(x in s) && !(x in ss)]
                    if is_k_defective(g, s, k) && is_k_defective(g, ss, k) && is_k_defective(g, sss, k)
                        return True
                    end
                end
            end
        end
    end
    return False
end

function isCycle(A,s)
    n=size(A,1)
    colorArr = -1 * ones(n)
    colorArr[s[1]] = 0
    p=1
    queue = Queue{Int}()
    enqueue!(queue,s[1])
    while !isempty(queue)
        u = dequeue!(queue)
        w=[]
        w=[x for x in A[u] if x in s]
        if size(w,1)!=2
            return false
        end
        for v in w
            if colorArr[v] == -1
                colorArr[v]=0
                p=p+1
                enqueue!(queue, v)
            end
        end
    end
    if p==size(s,1)
        return true
    end
    return false
end 



function isCompleCycle(A,s)
    newA=[]
    n=size(A,1)

    for i in 1:n
        push!(newA, [x for x in 1:n if ( !(x in A[i]) && x!=i ) ] )
    end
    
    return isCycle(newA,s)
end

function perfect(A)
    n=size(A,1)
    if n < 5
        return true
    end
    
    for m in 5:n
        if m%2==1            
            for vset in combinations(1:n, m)
                if isCycle(A,vset)
                    return false
                elseif m>5 && isCompleCycle(A,vset)
                    return false
                end
            end
        end
    end
    return true
end

# G - J is a perfect graph on 8 vertices which can not be 1-defectivelty 
# cocolored with 2 colors. It follows from Theorem 5.2 that G - J is one
# of the 24 extremal graphs for c^PG_1(2) = 7.
A = [[[4, 6, 7], [4, 6, 7], [5, 6], [5, 7], [0, 1], [2, 3, 7], [0, 1, 2, 7], [0, 1, 3, 5, 6]],
[[4, 5, 6, 7], [4, 5, 6], [5, 6, 7], [], [0, 1, 6, 7], [0, 1, 2, 7], [0, 1, 2, 4], [0, 2, 4, 5]],
[[4, 5, 6, 7], [4, 5, 6], [5, 6, 7], [7], [0, 1, 6, 7], [0, 1, 2, 7], [0, 1, 2, 4], [0, 2, 3, 4, 5]],
[[4, 5, 6, 7], [4, 5, 7], [5, 6, 7], [7], [0, 1, 6, 7], [0, 1, 2, 6], [0, 2, 4, 5], [0, 1, 2, 3, 4]],
[[4, 5, 7], [4, 6], [5, 6, 7], [5, 6, 7], [0, 1, 7], [0, 2, 3], [1, 2, 3, 7], [0, 2, 3, 4, 6]],
[[4, 5, 7], [4, 6], [5, 6, 7], [5, 6], [0, 1, 7], [0, 2, 3, 7], [1, 2, 3, 7], [0, 2, 4, 5, 6]],
[[4, 5, 6], [4, 7], [5, 6, 7], [5, 6, 7], [0, 1, 6, 7], [0, 2, 3, 7], [0, 2, 3, 4], [1, 2, 3, 4, 5]],
[[4, 5, 6], [4, 7], [5, 6, 7], [5, 6, 7], [0, 1, 5, 6, 7], [0, 2, 3, 4, 7], [0, 2, 3, 4], [1, 2, 3, 4, 5]],
[[3, 4, 6, 7], [4, 5, 7], [5, 6, 7], [0, 6], [0, 1, 7], [1, 2], [0, 2, 3, 7], [0, 1, 2, 4, 6]],
[[3, 4, 6, 7], [4, 5], [5, 6, 7], [0, 6, 7], [0, 1, 7], [1, 2, 7], [0, 2, 3], [0, 2, 3, 4, 5]],
[[3, 4, 6, 7], [4, 5, 7], [5, 6, 7], [0, 6, 7], [0, 1, 7], [1, 2, 7], [0, 2, 3], [0, 1, 2, 3, 4, 5]],
[[3, 4, 6, 7], [4, 5, 7], [5, 6, 7], [0, 6, 7], [0, 1, 7], [1, 2], [0, 2, 3, 7], [0, 1, 2, 3, 4, 6]],
[[3, 4, 6, 7], [4, 5, 7], [5, 6, 7], [0, 6, 7], [0, 1], [1, 2, 7], [0, 2, 3, 7], [0, 1, 2, 3, 5, 6]],
[[3, 4, 6, 7], [4, 5, 7], [5, 6, 7], [0, 6], [0, 1, 7], [1, 2, 7], [0, 2, 3, 7], [0, 1, 2, 4, 5, 6]],
[[3, 4, 6, 7], [4, 5, 7], [5, 6, 7], [0, 6, 7], [0, 1, 7], [1, 2, 7], [0, 2, 3, 7], [0, 1, 2, 3, 4, 5, 6]],
[[3, 4, 6, 7], [4, 5], [5, 7], [0, 6], [0, 1, 6, 7], [1, 2, 7], [0, 3, 4, 7], [0, 2, 4, 5, 6]],
[[3, 4, 5, 6, 7], [4, 5, 6], [5, 6, 7], [0], [0, 1, 6, 7], [0, 1, 2, 7], [0, 1, 2, 4], [0, 2, 4, 5]],
[[3, 4, 5, 6], [4, 5, 6, 7], [5, 6, 7], [0], [0, 1, 6, 7], [0, 1, 2, 7], [0, 1, 2, 4], [1, 2, 4, 5]],
[[3, 4, 5, 6], [4, 5, 6, 7], [5, 7], [0, 6, 7], [0, 1, 7], [0, 1, 2, 6, 7], [0, 1, 3, 5], [1, 2, 3, 4, 5]],
[[3, 4, 5, 6], [4, 5, 6, 7], [6, 7], [0, 5, 7], [0, 1, 6, 7], [0, 1, 3], [0, 1, 2, 4, 7], [1, 2, 3, 4, 6]],
[[3, 4, 5, 6], [4, 7], [5, 6, 7], [0, 5, 6, 7], [0, 1, 6, 7], [0, 2, 3, 7], [0, 2, 3, 4], [1, 2, 3, 4, 5]],
[[3, 5, 6, 7], [4, 5, 7], [4, 6], [0, 5, 6, 7], [1, 2, 7], [0, 1, 3], [0, 2, 3, 7], [0, 1, 3, 4, 6]],
[[3, 5, 6, 7], [4, 5, 6], [4, 7], [0, 5, 6, 7], [1, 2, 6, 7], [0, 1, 3, 7], [0, 1, 3, 4], [0, 2, 3, 4, 5]],
[[3, 5, 6, 7], [4, 5, 6], [4, 7], [0, 5, 6, 7], [1, 2, 5, 6, 7], [0, 1, 3, 4, 7], [0, 1, 3, 4], [0, 2, 3, 4, 5]]]

# G has a 1-defective 5-set , say J.
B = [[[], [], [], [], []],
[[1], [0], [], [], []],
[[1], [0], [3], [2], []],
[[1, 2, 3, 4], [0, 2, 3, 4], [0, 1, 3, 4], [0, 1, 2, 4], [0, 1, 2, 3]],
[[2, 3, 4], [2, 3, 4], [0, 1, 3, 4], [0, 1, 2, 4], [0, 1, 2, 3]],
[[2, 3, 4], [2, 3, 4], [0, 1, 4], [0, 1, 4], [0, 1, 2, 3]]]

n = 40
for a in A
    for b in B
        g = union_two_graph(a, b)
        for edges in collect(powerset(range(1; stop=n)))
            newg=[vert[:] for vert in g]
            for edge in edges
                push!(newg[floor(Int8, edge / 6)+1], 6 + (edge % 5))
                push!(newg[6 + (edge % 5)+1], floor(Int8, edge / 6))
            end
            if not(is_g_k_def_three_colorable(newg, 2))
                if perfect(newg)
                    print(newg)
                end
            end
            print(newg)
        end
    end
end

return 0

