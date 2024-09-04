# (src: https://courses.cs.washington.edu/courses/cse427/12wi/progressive.html)
# Details of guide tree construction
# 1. Initially, each node is the root of its own tree.
# 2. Consider edges in increasing order of edge label.
# 3. If the next edge e connects nodes {a,b} in the same tree, discard e.
# 4. Otherwise, find the root v of the tree containing a, and the root w of the tree containing b. 
#    Add a new root u with children v and w, thus merging the trees containing a and b into a single tree.

class Node:
    count = 0
    def __init__(self):
        # 1. Initially, each node is the root of its own tree.
        self.root = True
        self.i = Node.count
        self.children = []
        self.createdBy = None
        self.seq = ""
        # 2. Consider edges in increasing order of edge label.
        Node.count += 1
        
    def adopt(self, child1, child2):
        self.children.append(child1)
        self.children.append(child2)
        child1.root = False
        child2.root = False
        return self

    def is_root(self):
        return self.root

    def get_childer(self):
        childList = []
        for child in self.children: 
            childList.append(child.i)
        return childList
    
    def created_by(self, nodeA, nodeB):
        self.createdBy = (nodeA, nodeB)
        return self 
    
    def has_children(self):
        return self.children != []
    
    def info(self):
        if self.createdBy == None:
            return f"Node: {self.i}, root: {self.root}, children: {self.get_childer()}, created by: None, sequence: {self.seq}"
        return f"Node: {self.i}, root: {self.root}, children: {self.get_childer()}, created by: ({self.createdBy[0].i}, {self.createdBy[1].i}), sequence: {self.seq}"


class GuideTree:
    def __init__(self):
        self.nodes = []
        for _ in range(15): self.nodes.append(Node())

    def construct(self, MST):
        for edge in MST:
            nodeA, nodeB = self.nodes[edge[0]], self.nodes[edge[1]]
            createNewRoot = True
            for node in self.nodes:
                if not node.is_root(): continue
                treeNodes = self.tree_nodes(node)
                nodeA_found = nodeA in treeNodes
                nodeB_found = nodeB in treeNodes
                # 3. If the next edge e connects nodes {a,b} in the same tree, discard e.
                if nodeA_found and nodeB_found:
                    createNewRoot = False
                    break
                # 4. Otherwise, find the root v of the tree containing a, and the root w of the tree containing b.
                if nodeA_found:
                    rootA = node
                elif nodeB_found:
                    rootB = node
            # Add a new root u with children v and w, thus merging the trees containing a and b into a single tree.
            if createNewRoot: self.nodes.append(Node().created_by(nodeA, nodeB).adopt(rootA, rootB))
        return self

    def tree_nodes(self, rootNode, visited = []):
        if not rootNode.has_children(): 
            return visited + [rootNode]
        for child in rootNode.children:
            visited = self.tree_nodes(child, visited)
        return visited + [rootNode]
    
    def info(self):
        info = ""
        for node in self.nodes:
            info += node.info() + "\n"
        return info
