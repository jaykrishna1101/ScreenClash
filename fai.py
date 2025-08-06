global tree, q, s
tree = {'A': ['B','C'],
        'B': ['D','E'],
        'C': ['F'],
        'D': ['G'],
        'E': [],
        'F': ['H'],
        'G': [],
        'H': []
        }

q = []
s = []

def bfs(start, element):
    q.append(start)

    while q:
        a = qremove()
        print(a,end=" ")
        if a == element:
            return f"Found {a}"
        if tree[a]:
            for s in tree[a]:
                q.append(s)
    return "element not found"


def dfs(start, element):
    s.append(start)

    while s:
        a = s.pop()
        print(a, end = " ")
        if a == element:
            return f"Found {a}"
        if tree[a]:
            for i in tree[a]:
                s.append(i)
    return "element not found"


def qremove():
    global q
    f = q[0]
    q = q[1:]
    return f


element = input("enter: ")
print(bfs('A',element))
print(dfs('A',element))


























# if __name__ == "__main__":
#     main()