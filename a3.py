def sortX(lst):  # O(nlogn)
    lst.sort()
    return lst


def sortY(lst):  # O(nlogn)
    for i in lst:
        i[0], i[1] = i[1], i[0]
    lst.sort()
    for i in lst:
        i[0], i[1] = i[1], i[0]
    return lst


class Node:  # O(1)
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.leafCheck = False
        self.next = None
        self.node = True


def oneDQuerysearchHelper1(currentNode, x, l):  # O((logn)^2)
    if currentNode is not None:
        while not currentNode.leafCheck:  # O(logn)
            if x[0] <= currentNode.val[1]:
                l.extend([currentNode.val])
                incrementNode = currentNode.right
                while not incrementNode.leafCheck and incrementNode is not None:  # O(logn)
                    if incrementNode.val[1] >= x[0]:
                        l.extend([incrementNode.val])
                    incrementNode = incrementNode.right
                currentNode = currentNode.left
            else:
                currentNode = currentNode.right


def oneDQuerysearchHelper2(currentNode, x, l, a):  # O((logn)^2)
    if currentNode is not None:
        while not currentNode.leafCheck and currentNode is not None:  # O(logn)
            if x[1] >= currentNode.val[1]:
                l.extend([currentNode.val])
                incrementNode = currentNode.left
                while not incrementNode.leafCheck and incrementNode is not None:  # O(logn)
                    if incrementNode.val[1] <= x[1]:
                        l.extend([incrementNode.val])
                    incrementNode = incrementNode.left
                currentNode = currentNode.right
            else:
                currentNode = currentNode.left
        if a[len(a) - 1][1] <= x[1]:
            l.extend([a[len(a) - 1]])


class RangeTree(Node):
    def __init__(self, pointlist):  # O(logn)
        if len(pointlist) != 0:
            self.pointlist = pointlist
            self.root = self.buildTreeHelper(pointlist)  # O(logn)
        else:
            self.pointlist = pointlist
            self.root = None

    def getSize(self):  # O(1)
        return len(self.pointlist)

    def buildTreeHelper(self, pointlist):  # O(logn)
        n = len(pointlist)
        if n == 1:
            val = Node(pointlist[0])
            val.leafCheck = True
        else:
            if n % 2 == 0:
                n = (n - 1) // 2
            else:
                n = n // 2
            val = Node(pointlist[n])
            val.left = self.buildTreeHelper(pointlist[:n + 1])  # O(logn)
            val.right = self.buildTreeHelper(pointlist[n + 1:])  # O(logn)
        return val

    def splitnode(self, node, x):  # O(logn)
        if self.root is None:
            return
        if node.leafCheck:
            if x[0] <= node.val[1] <= x[1]:
                return node
            return
        elif x[0] <= node.val[1] <= x[1]:
            return node
        else:
            if x[1] <= node.val[1]:
                return self.splitnode(node.left, x)
            if x[0] >= node.val[1]:
                return self.splitnode(node.right, x)

    def oneDQuerysearch(self, x, l):  # O((logn)^2)
        if self.root is None:
            return l
        Nodesplit = self.splitnode(self.root, x)
        if Nodesplit is None:
            return l
        l.extend([Nodesplit.val])
        currentNode = Nodesplit.left
        oneDQuerysearchHelper1(currentNode, x, l)
        currentNode2 = Nodesplit.right
        oneDQuerysearchHelper2(currentNode2, x, l, self.pointlist)
        return l


def linkerHelper(l, p, i, j, x):  # O(nlogn)
    while i < len(l) and j < len(p):
        if l[i][1] < p[j][1]:
            x.extend([l[i]])
            i += 1
        else:
            x.extend([p[j]])
            j += 1
    if j == len(p):
        while i < len(l):
            x.extend([l[i]])
            i += 1
    if i == len(l):
        while j < len(p):
            x.extend([p[j]])
            j += 1
    return RangeTree(x)


def twoDQuerysearchHelper1(v, x, y, l):  # O((logn)^2)
    if v is not None:
        while not v.leafCheck:
            if x[0] <= v.val[0]:
                l = v.right.next.oneDQuerysearch(y, l)  # O((logn)^2)
                v = v.left
            else:
                v = v.right
        if (x[0] <= v.val[0] <= x[1]) and (y[0] <= v.val[1] <= y[1]):
            l.extend([v.val])


def twoDQuerysearchHelper2(z, x, y, l):  # O((logn)^2)
    if z is not None:
        while not z.leafCheck:
            if x[1] >= z.val[0]:
                l = z.left.next.oneDQuerysearch(y, l)  # O((logn)^2)
                z = z.right
            else:
                z = z.left
        if (x[0] <= z.val[0] <= x[1]) and (y[0] <= z.val[1] <= y[1]):
            l.extend([z.val])


class PointDatabaseHepler(RangeTree):
    def __init__(self, pointlist):  # O(nlogn)
        if len(pointlist) != 0:
            l = sortX(pointlist)  # O(nlogn)
            self.root = self.buildTreeHelper(l)  # O(nlogn)
        else:
            self.root = None

    def linker(self, a, b):  # O(nlogn)
        l = a.pointlist
        p = b.pointlist
        x = []
        i = 0
        j = 0
        k = linkerHelper(l, p, i, j, x)  # O(nlogn)
        return k

    def buildTreeHelper(self, pointlist):  # O(nlogn)
        if len(pointlist) == 0:
            return
        if len(pointlist) == 1:
            val = Node(pointlist[0])
            val.leafCheck = True
            val.next = RangeTree(pointlist)  # O(logn)
            return val
        else:
            if len(pointlist) % 2 == 0:
                n = (len(pointlist) - 1) // 2
            else:
                n = len(pointlist) // 2
            val = Node(pointlist[n])
            val.left = self.buildTreeHelper(pointlist[:n + 1])  # O(nlogn) (base case = logn, for n nodes, nlogn recursively)
            val.right = self.buildTreeHelper(pointlist[n + 1:])  # O(nlogn) (base case = logn, for n nodes, nlogn recursively)
            val.next = self.linker(val.left.next, val.right.next)  # O(nlogn)
            return val

    def splitnode(self, node, x):  # O(logn)
        if node.leafCheck:
            if x[0] <= node.val[0] <= x[1]:
                return node
            return
        elif x[0] <= node.val[0] <= x[1]:
            return node
        else:
            if x[1] <= node.val[0]:
                return self.splitnode(node.left, x)
            elif x[0] >= node.val[0]:
                return self.splitnode(node.right, x)

    def twoDQuerysearch(self, a, x, y, l):  # O((logn)^2)
        if a is None:
            return l
        splitNode = self.splitnode(a, x)  # O(logn)
        if splitNode is None:
            return l
        if splitNode.leafCheck:  # O(1)
            if (x[0] <= splitNode.val[0] <= x[1]) and (
                    y[0] <= splitNode.val[1] <= y[1]):
                l.extend([splitNode.val])
                return l
            else:
                return l
        else:
            v = splitNode.left
            twoDQuerysearchHelper1(v, x, y, l)  # O((logn)^2)
            z = splitNode.right
            twoDQuerysearchHelper2(z, x, y, l)  # O((logn)^2)
            return l

    def searchNearby(self, q, d):  # O(m+(logn)^2)
        x1 = q[0] - d
        x2 = q[0] + d
        y1 = q[1] - d
        y2 = q[1] + d
        x = [x1, x2]
        y = [y1, y2]
        return self.twoDQuerysearch(self.root, x, y, [])  # O(m) reporting time of m coordinates, O((logn)^2) for query


class PointDatabase(PointDatabaseHepler):
    def __init__(self, pointlist):  # O(nlogn)
        super(PointDatabase, self).__init__(pointlist)  # O(nlogn)

    def searchNearby(self, q, d):  # O(m+(logn)^2)
        x1 = q[0] - d
        x2 = q[0] + d
        y1 = q[1] - d
        y2 = q[1] + d
        x = [x1, x2]
        y = [y1, y2]
        l = []
        return self.twoDQuerysearch(self.root, x, y, l)  # O(m+(logn)^2)


'''O(nlogn) proved for constructor __init__'''
'''O(m + log2 n) proved for searchNearby'''

# l = [(1, 6), (2, 4), (3, 7), (4, 9), (5, 1), (6, 3), (7, 8), (8, 10), (9, 2), (10, 5)]
#
# pointDbObject = PointDatabase(l)
# print(pointDbObject.searchNearby((6, 6), 2))
# print(pointDbObject.searchNearby((-3, 1), 3))
# print(pointDbObject.searchNearby((12, 5), 1))
# print(pointDbObject.searchNearby((8, 12), 2))
# print(pointDbObject.searchNearby((5, -2), 2))
# print(pointDbObject.searchNearby((-3, 5), 7))
# print(pointDbObject.searchNearby((13, 1), 2))
# print(pointDbObject.searchNearby((5, 23), 4))
# print(pointDbObject.searchNearby((5, -4), 3))
# print(pointDbObject.searchNearby((0, 6), 4))
# print(pointDbObject.searchNearby((3, 1), 20))
# print(pointDbObject.searchNearby((-3, 1), 20))
# print(pointDbObject.searchNearby((3, 1), 0))
# print(pointDbObject.searchNearby((3, 1), 1))
# print(pointDbObject.searchNearby((-1, 6), 5))
# print(pointDbObject.searchNearby((6, 6), 4))
# print(pointDbObject.searchNearby((6, 6), 0))
# print(pointDbObject.searchNearby((-1, -1), 0))
# print(pointDbObject.searchNearby((11, 11), 0))

# pointDbObject = PointDatabase([(1, 6), (2, 4), (3, 7), (4, 9), (5, 1), (6, 3), (7, 8), (8, 10), (9, 2), (10, 5)])
# query = [[(5, 5), 1, []], [(4, 8), 2, [(3, 7), (4, 9)]], [(10, 2), 1.5, [(9, 2)]]]
#
# import time
# sax = time.time()
# for tc in query:
#     if not sorted(pointDbObject.searchNearby(tc[0], tc[1])) == sorted(tc[2]):
#         print("Kat gaya bhai tera!")
#         break
# print(time.time()-sax)
