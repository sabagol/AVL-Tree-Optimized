# id1: 345020226

# name1: Saba Golbandi

# username1: sabagolbandi

# id2: 325394534

# name2: Nasma Shannan

# username2: nasmashannan





"""A class representing a node in an AVL tree"""





class AVLNode(object):

    """Constructor, you are allowed to add more fields.



    @type key: int

    @param key: key of your node

    @type value: string

    @param value: data of your node

    """



    def __init__(self, key, value):

        self.key = key

        self.value = value

        self.left = None

        self.right = None

        self.parent = None

        self.height = -1



    """returns whether self is not a virtual node 



    @rtype: bool

    @returns: False if self is a virtual node, True otherwise.

    """



    def is_real_node(self):

        return self.height > -1





"""

A class implementing an AVL tree.

"""





class AVLTree(object):



    """

    Constructor, you are allowed to add more fields.

    """



    def __init__(self):

        self.root = None

        self.sizeT = 0



    """searches for a node in the dictionary corresponding to the key (starting at the root)

        

    @type key: int

    @param key: a key to be searched

    @rtype: (AVLNode,int)

    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),

    and e is the number of edges on the path between the starting node and ending node+1.

    """



    def search(self, key):

        if not self.root:

            return None, 0

        curr = self.root

        e = 1

        while curr.is_real_node():

            if curr.key == key:

                return curr, e

            if key < curr.key:

                curr = curr.left

            else:

                curr = curr.right

            e += 1



        return None, e - 1



    """searches for a node in the dictionary corresponding to the key, starting at the max

        

    @type key: int

    @param key: a key to be searched

    @rtype: (AVLNode,int)

    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),

    and e is the number of edges on the path between the starting node and ending node+1.

    """



    def finger_search(self, key):

        if not self.root:

            return None, 0

        curr = self.max_node()

        e = 1

        while curr:

            if curr.key == key:

                return curr, e

            if curr.parent and key <= curr.parent.key:

                curr = curr.parent

            else:

                if curr.left:

                    curr = curr.left

                else:

                    curr = None

                e += 1

                break

            e += 1



        while curr.is_real_node():

            if curr.key == key:

                return curr, e

            if key < curr.key:

                curr = curr.left

            else:

                curr = curr.right

            e += 1



        return None, e - 1



    """inserts a new node into the dictionary with corresponding key and value (starting at the root)



    @type key: int

    @pre: key currently does not appear in the dictionary

    @param key: key of item that is to be inserted to self

    @type val: string

    @param val: the value of the item

    @rtype: (AVLNode,int,int)

    @returns: a 3-tuple (x,e,h) where x is the new node,

    e is the number of edges on the path between the starting node and new node before rebalancing,

    and h is the number of PROMOTE cases during the AVL rebalancing

    """



    def insert(self, key, val):

        self.sizeT += 1

        new_node = AVLNode(key, val)

        new_node.height = 0

        # generate virtual children

        new_node.left = AVLNode(None, None)

        new_node.right = AVLNode(None, None)

        new_node.left.parent, new_node.right.parent = new_node, new_node

        path = (

            []

        )  # path is the list of the path from the root to the parent of the new node

        if not self.root:

            self.root = new_node

            path.append(new_node)

            return self.root, 0, 0

        parent = None

        curr = self.root

        e = 0  # number of edges in the path from the root to the inserted node

        while curr.is_real_node():

            path.append(curr)

            e += 1

            parent = curr

            if key < curr.key:

                curr = curr.left

            else:

                curr = curr.right



        new_node.parent = parent

        if new_node.key < parent.key:

            parent.left = new_node

        else:

            parent.right = new_node

        p = self.promote(new_node)



        # check if the whole tree is balanced

        is_balanced = True

        i = 0

        while is_balanced == True and i < len(path):

            n = path[i]

            if self.get_balance(n) not in [-1, 0, 1]:

                is_balanced = False

            i += 1

        if is_balanced:

            return new_node, e, p

        # the tree is not balanced and we need rotations

        self.perform_rotations(path, new_node)

        return new_node, e, p



    """Checks the path given and in case of unbalanced nodes, performs relevant rotations.

    Returns number of promotions that we do not need, so that we can subtract afterwards

        

    @type path: list

    @param path: the path that may contain unbalanced nodes

    @rtype: int

    @returns: returns number of promotions that we do not need, so that we can subtract afterwards



    """



    def perform_rotations(self, path, new_node):

        p = 0

        # the tree is not balanced and we need rotations

        while len(path) > 0:

            node = path.pop()

            node.height = 1 + max(

                self.get_height(node.left), self.get_height(node.right)

            )

            balance = self.get_balance(node)

            # perform rotation

            if balance > 1:  # left side is heavier

                p += 1

                if new_node.key < node.left.key:  # LL case

                    if path:

                        parent = path[-1]

                        if parent.left == node:

                            parent.left = self.right_rotation(node)

                        else:

                            parent.right = self.right_rotation(node)

                    else:

                        self.root = self.right_rotation(node)

                else:  # LR case

                    node.left = self.left_rotation(node.left)

                    if path:

                        parent = path[-1]

                        if parent.left == node:

                            parent.left = self.right_rotation(node)

                        else:

                            parent.right = self.right_rotation(node)

                    else:

                        self.root = self.right_rotation(node)

            elif balance < -1:

                p += 1

                if new_node.key > node.right.key:  # RR case

                    if path:

                        parent = path[-1]

                        if parent.left == node:

                            parent.left = self.left_rotation(node)

                        else:

                            parent.right = self.left_rotation(node)

                    else:

                        self.root = self.left_rotation(node)

                else:  # RL case

                    node.right = self.right_rotation(node.right)

                    if path:

                        parent = path[-1]

                        if parent.left == node:

                            parent.left = self.left_rotation(node)

                        else:

                            parent.right = self.left_rotation(node)

                    else:

                        self.root = self.left_rotation(node)

        return p



    """ Returns the height of the input node

        

    @type node: AVLNode

    @param node: the node we are looking for its height

    @rtype: int

    @returns: returns the height of the given node

    """



    def get_height(self, node):

        if node and not node.is_real_node():

            return -1

        return node.height



    """ Returns the balance of the input node, which is the difference of the height its left child and 

    the height of its right child

        

    @type node: AVLNode

    @param node: the node we are looking for its balance

    @rtype: int

    @returns: returns the difference of the height its left child and the height of its right child

    """



    def get_balance(self, node):

        if node and not node.is_real_node:

            return 0

        return self.get_height(node.left) - self.get_height(node.right)



    """ Performs a right rotation on the given node, based on the right rotation algorith we learnt at 

    the lecture

        

    @type node: AVLNode

    @param node: the node on which we are performing a right rotation

    @rtype: AVLNode

    @returns: the rotated node

    """



    def right_rotation(self, node):

        l = node.left

        lr = l.right



        # perform rotation

        l.right = node

        node.left = lr



        # update parents

        lr.parent = node

        l.parent = node.parent

        if node.parent:

            if node.parent.left == node:

                node.parent.left = l

            else:

                node.parent.right = l

        node.parent = l



        # update height

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        l.height = 1 + max(self.get_height(l.left), self.get_height(l.right))



        return l



    """ Performs a left rotation on the given node, based on the left rotation algorith we learnt at 

    the lecture

        

    @type node: AVLNode

    @param node: the node on which we are performing a left rotation

    @rtype: AVLNode

    @returns: the rotated node

    """



    def left_rotation(self, node):

        r = node.right

        rl = r.left



        # perform rotation

        r.left = node

        node.right = rl



        # update parents

        rl.parent = node

        r.parent = node.parent

        if node.parent:

            if node.parent.left == node:

                node.parent.left = r

            else:

                node.parent.right = r



        node.parent = r



        # update height

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        r.height = 1 + max(self.get_height(r.left), self.get_height(r.right))



        return r



    """ Updates the height of the node and its parents, in case of any change after insertion 

    and returns the number of these height changes

        

    @type node: AVLNode

    @param node: the node on which we are performing promote

    @rtype: int

    @returns: the number of height changes

    """



    def promote(self, node):

        count = 0

        curr = node

        isBalanced = True

        while curr.parent and curr.height == curr.parent.height:

            if isBalanced:

                count += 1

            curr.parent.height += 1

            curr = curr.parent

            if isBalanced and self.get_balance(curr) not in [-1, 0, 1]:

                count -= 1

                isBalanced = False



        if not curr.parent:

            curr.height = 1 + max(

                self.get_height(curr.left), self.get_height(curr.right)

            )

        return count



    """inserts a new node into the dictionary with corresponding key and value, starting at the max



    @type key: int

    @pre: key currently does not appear in the dictionary

    @param key: key of item that is to be inserted to self

    @type val: string

    @param val: the value of the item

    @rtype: (AVLNode,int,int)

    @returns: a 3-tuple (x,e,h) where x is the new node,

    e is the number of edges on the path between the starting node and new node before rebalancing,

    and h is the number of PROMOTE cases during the AVL rebalancing

    """



    def finger_insert(self, key, val):

        self.sizeT += 1

        new_node = AVLNode(key, val)

        new_node.height = 0

        # generate virtual children

        new_node.left = AVLNode(None, None)

        new_node.right = AVLNode(None, None)

        new_node.left.parent, new_node.right.parent = new_node, new_node

        path = []

        turned_left = False

        first_left = None

        if not self.root:

            self.root = new_node

            path.append(new_node)

            return self.root, 0, 0

        parent = None

        curr = self.max_node()

        e = 0

        if new_node.key > curr.key:

            curr.right = new_node

            new_node.parent = curr

            parent = curr

            e += 1

            path_node = curr

            while path_node.parent:

                path.append(path_node)

                path_node = path_node.parent

            path.append(path_node)

            path.reverse()

        else:

            while curr.is_real_node():

                path.append(curr)

                e += 1

                parent = curr

                if curr.parent and key < curr.parent.key:

                    curr = curr.parent

                else:

                    curr = curr.left

                    turned_left = True

                    first_left = curr

                    path = []

                    break



            while curr.is_real_node():

                path.append(curr)

                e += 1

                parent = curr

                if key < curr.key:

                    curr = curr.left

                else:

                    curr = curr.right



        new_node.parent = parent

        if new_node.key < parent.key:

            parent.left = new_node

        else:

            parent.right = new_node

        p = self.promote(new_node)



        # check if the whole tree is balanced

        # update the path if we turned left

        if turned_left:

            path.reverse()

            while first_left.parent:

                first_left = first_left.parent

                path.append(first_left)

            path.reverse()

        is_balanced = True

        i = 0

        while is_balanced is True and i < len(path):

            n = path[i]

            if self.get_balance(n) not in [-1, 0, 1]:

                is_balanced = False

            i += 1

        if is_balanced is True:

            return new_node, e, p



        # the tree is not balanced and we need rotations

        self.perform_rotations(path, new_node)



        return new_node, e, p



    """deletes node from the dictionary



    @type node: AVLNode

    @pre: node is a real pointer to a node in self

    """



    def delete(self, node):

        # the tree has only one node, and we want to delete it

        if not self.root.left.is_real_node() and not self.root.right.is_real_node():

            self.root = None

            self.sizeT = 0

            return

        # the tree has only two node, and we want to delete the root

        if self.sizeT == 2 and node is self.root:

            if node.left.is_real_node():

                self.root = self.root.left

            else:

                self.root = self.root.right

            self.root.parent = None

            self.sizeT = 1

            return



        path = []

        # Case 1: Node has two children

        if node.left.is_real_node() and node.right.is_real_node():

            # Find the successor

            replacement = self.successorCh(node)

            path.append(replacement.parent)

            node.key = replacement.key

            node.value = replacement.value

            node = replacement



        # Case 2: Node has one child or no children

        parent = node.parent

        if node.left.is_real_node():

            self.update_parent_reference(node, node.left)

        if node.right.is_real_node():

            self.update_parent_reference(node, node.right)

        else:

            none_node = AVLNode(None, None)

            self.update_parent_reference(node, none_node)



        # Build the path to the deleted node

        current = parent

        while current:

            path.append(current)

            current = current.parent

        if len(path) == 0:

            ancestor = None

        else:

            ancestor = path[0]

        # Perform rotations to rebalance the tree

        for ancestor in reversed(path):

            # Update the height of the current node

            ancestor.height = 1 + max(

                self.get_height(ancestor.left), self.get_height(ancestor.right)

            )

        balance = self.get_balance(ancestor)

        # Perform rotations if unbalanced

        while ancestor:

            balance = self.get_balance(ancestor)

            if balance > 1:  # Left-heavy

                if self.get_balance(ancestor.left) >= 0:  # Left-Left case

                    self.right_rotation(ancestor)

                else:  # Left-Right case

                    self.left_rotation(ancestor.left)

                    self.right_rotation(ancestor)

            elif balance < -1:  # Right-heavy

                if self.get_balance(ancestor.right) <= 0:  # Right-Right case

                    self.left_rotation(ancestor)

                else:  # Right-Left case

                    self.right_rotation(ancestor.right)

                    self.left_rotation(ancestor)

            ancestor.height = 1 + max(

                self.get_height(ancestor.left), self.get_height(ancestor.right)

            )

            ancestor = ancestor.parent

        balance = self.get_balance(self.root)

        if balance > 1:

            self.right_rotation(self.root)

            self.root = self.root.parent

        if balance < -1:

            self.left_rotation(self.root)

            self.root = self.root.parent



        if self.root.parent:

            self.root = self.root.parent



        self.sizeT -= 1



    """Updates the parent reference to replace the node with new_node.



    @type node: AVLNode

    @type new_node: AVLNode

    """



    def update_parent_reference(self, node, new_node):



        if node.parent:

            if node.parent.left == node:

                node.parent.left = new_node



            else:

                node.parent.right = new_node

        new_node.parent = node.parent

        node.parent = None



    """Returns the successor of the given node in the tree



    @type node: AVLNode

    @rtype: AVLNode

    """



    def successorCh(self, node):

        if not node.is_real_node():

            return None



        # Case 1: Node has a right subtree

        if node.right.is_real_node():

            return self.find_min(node.right)



        # Case 2: No right subtree, go to the nearest ancestor

        current = node

        while current.parent and current.parent.right == current:

            current = current.parent



        return current.parent



    """Returns the node holding the maximum key in the subtree whose root is the given node



    @type node: AVLNode

    @rtype: AVLNode

    """



    def find_max(self, node):

        while node and node.right.is_real_node():

            node = node.right

        return node



    """Returns the node holding the minimum key in the subtree whose root is the given node



    @type node: AVLNode

    @rtype: AVLNode

    """



    def find_min(self, node):

        while node and node.left.is_real_node():

            node = node.left

        return node



    """joins self with item and another AVLTree



    @type tree2: AVLTree 

    @param tree2: a dictionary to be joined with self

    @type key: int 

    @param key: the key separating self and tree2

    @type val: string

    @param val: the value corresponding to key

    @pre: all keys in self are smaller than key and all keys in tree2 are larger than key,

    or the opposite way

    """



    def join(self, tree2, key, val):

        if not self.root:

            # If current tree is empty, take the other tree

            self.root = tree2.root

            tree2.root = None

            self.insert(key, val)

            # update tree size

            self.sizeT = tree2.sizeT

            return

        elif not tree2.root:

            # If the other tree is empty, just insert the new node

            self.insert(key, val)

            return



        # update tree size

        self.sizeT = self.sizeT + tree2.sizeT

        new_node = AVLNode(key, val)

        new_node.height = 0

        # generate virtual children

        new_node.left = AVLNode(None, None)

        new_node.right = AVLNode(None, None)

        new_node.left.parent, new_node.right.parent = new_node, new_node



        if tree2.root.key > key:

            # If T2 is with bigger keys than self

            # Find the higher tree

            h1 = self.root.height

            h2 = tree2.root.height

            if h2 == h1 or h2 == h1 + 1 or h2 == h1 - 1:

                # Both trees are almost the same height

                new_node.left = self.root

                self.root.parent = new_node

                new_node.right = tree2.root

                tree2.root.parent = new_node

                self.root = new_node

                # invalidate T2

                tree2.root = None

                # update height

                new_node.height = 1 + max(new_node.left.height, new_node.left.height)

                return

            if h2 > h1 + 1:

                # T2 is higher that T1

                curr = tree2.root

                while curr.height > h1 + 1:

                    parent = curr

                    curr = curr.left

                if curr.left.height == h1:

                    parent = curr

                    curr = curr.left

                # curr is the leftest node in T2 with height of at least h-1 and parent is its parent

                parent.left = new_node

                new_node.parent = parent

                new_node.right = curr

                curr.parent = new_node

                new_node.left = self.root

                self.root.parent = new_node

                self.root = tree2.root

                # invalidate T2

                tree2.root = None

                # update heights and generate path

                node = new_node

                path = [new_node]

                while node.parent:

                    node.height = 1 + max(node.left.height, node.right.height)

                    node = node.parent

                    path.append(node)

                node.height = 1 + max(node.left.height, node.right.height)

                path.reverse()



                # check balance, and rebalance

                # check if the whole tree is balanced

                is_balanced = True

                i = 0

                while is_balanced == True and i < len(path):

                    n = path[i]

                    if self.get_balance(n) not in [-1, 0, 1]:

                        is_balanced = False

                    i += 1

                if is_balanced:

                    return



                # the tree is not balanced and we need rotations

                self.perform_rotations(path, new_node)

                return



            if h2 < h1 - 1:

                # T1 is higher than T2

                curr = self.root

                while curr.height > h2 + 1:

                    parent = curr

                    curr = curr.right

                if curr.right.height == h2:

                    parent = curr

                    curr = curr.right

                # curr is the rightest node in self with height of at least h-1 and parent is its parent

                parent.right = new_node

                new_node.parent = parent

                new_node.right = tree2.root

                tree2.root.parent = new_node

                new_node.left = curr

                curr.parent = new_node

                # invalidate T2

                tree2.root = None

                # update heights and generate path

                node = new_node

                path = [new_node]

                while node.parent:

                    node.height = 1 + max(node.left.height, node.right.height)

                    node = node.parent

                    path.append(node)

                node.height = 1 + max(node.left.height, node.right.height)

                path.reverse()



                # check balance, and rebalance

                # check if the whole tree is balanced

                is_balanced = True

                i = 0

                while is_balanced == True and i < len(path):

                    n = path[i]

                    if self.get_balance(n) not in [-1, 0, 1]:

                        is_balanced = False

                    i += 1

                if is_balanced:

                    return



                # the tree is not balanced and we need rotations

                self.perform_rotations(path, new_node)

                return



        if tree2.root.key < key:

            # If T2 is with smaller keys than self

            # Find the higher tree

            h1 = self.root.height

            h2 = tree2.root.height

            if h2 == h1 or h2 == h1 + 1 or h2 == h1 - 1:

                # Both trees are almost the same height

                new_node.right = self.root

                self.root.parent = new_node

                new_node.left = tree2.root

                tree2.root.parent = new_node

                self.root = new_node

                # invalidate T2

                tree2.root = None

                # update heights

                new_node.height = 1 + max(new_node.left.height, new_node.left.height)

                return

            if h2 > h1 + 1:

                # T2 is higher that T1

                curr = tree2.root

                while curr.height > h1 + 1:

                    parent = curr

                    curr = curr.right

                if curr.right.height == h1:

                    parent = curr

                    curr = parent

                # curr is the leftest node in T2 with height of at least h-1 and parent is its parent

                parent.right = new_node

                new_node.parent = parent

                new_node.left = curr

                curr.parent = new_node

                new_node.right = self.root

                self.root.parent = new_node

                self.root = tree2.root

                # invalidate T2

                tree2.root = None

                # update heights and generate path

                node = new_node

                path = [new_node]

                while node.parent:

                    node.height = 1 + max(node.left.height, node.right.height)

                    node = node.parent

                    path.append(node)

                node.height = 1 + max(node.left.height, node.right.height)

                path.reverse()



                # check balance, and rebalance

                # check if the whole tree is balanced

                is_balanced = True

                i = 0

                while is_balanced == True and i < len(path):

                    n = path[i]

                    if self.get_balance(n) not in [-1, 0, 1]:

                        is_balanced = False

                    i += 1

                if is_balanced:

                    return



                # the tree is not balanced and we need rotations

                self.perform_rotations(path, new_node)

                return



            if h2 < h1 - 1:

                # T1 is higher than T2

                curr = self.root

                while curr.height > h2 + 1:

                    parent = curr

                    curr = curr.left

                if curr.left.height == h2:

                    parent = curr

                    curr = curr.left

                # curr is the rightest node in self with height of at least h-1 and parent is its parent

                parent.left = new_node

                new_node.parent = parent

                new_node.left = tree2.root

                tree2.root.parent = new_node

                new_node.right = curr

                curr.parent = new_node

                # invalidate T2

                tree2.root = None

                # update heights and generate path

                node = new_node

                path = [new_node]

                while node.parent:

                    node.height = 1 + max(node.left.height, node.right.height)

                    node = node.parent

                    path.append(node)

                node.height = 1 + max(node.left.height, node.right.height)

                path.reverse()



                # check balance, and rebalance

                # check if the whole tree is balanced

                is_balanced = True

                i = 0

                while is_balanced == True and i < len(path):

                    n = path[i]

                    if self.get_balance(n) not in [-1, 0, 1]:

                        is_balanced = False

                    i += 1

                if is_balanced:

                    return



                # the tree is not balanced and we need rotations

                self.perform_rotations(path, new_node)

                return



    """splits the dictionary at a given node



    @type node: AVLNode

    @pre: node is in self

    @param node: the node in the dictionary to be used for the split

    @rtype: (AVLTree, AVLTree)

    @returns: a tuple (left, right), where left is an AVLTree representing the keys in the 

    dictionary smaller than node.key, and right is an AVLTree representing the keys in the 

    dictionary larger than node.key.

    """



    def split(self, node):

        t1 = AVLTree()

        t2 = AVLTree()

        # if node is max or min just delete them and return the trees one of them her root is none

        n1 = self.max_node()

        if node is n1:

            self.delete(n1)

            t1.root = self.root

            t1.sizeT = self.sizeT

            self.root = None

            return t1, t2

        n1 = self.find_min(self.root)

        if node is n1:

            self.delete(n1)

            t2.root = self.root

            t2.sizeT = self.sizeT

            self.root = None

            return t1, t2



        # Set the roots of t1 and t2 to the left and right subtrees of the node

        if node.left.is_real_node():

            t1.root = node.left

            node.left.parent = None

        else:

            t1.root = None



        if node.right.is_real_node():

            t2.root = node.right

            node.right.parent = None

        else:

            t2.root = None



        # node.left.parent = None  # Disconnect the left subtree

        # node.right.parent = None  # Disconnect the right subtree



        # Traverse up the ancestors of the node to adjust t1 and t2

        current = node

        while current.parent:

            parent = current.parent



            # If the current node is the left child, its parent belongs to t2

            if parent.left == current:

                if parent.right.is_real_node():

                    # Add the right subtree of the parent to t2

                    join_tree = AVLTree()

                    join_tree.root = parent.right

                    join_tree.root.parent = None

                    t2.join(join_tree, parent.key, parent.value)

                    parent.right.parent = None

                current = parent



            # If the current node is the right child, its parent belongs to t1

            else:

                if parent.left.is_real_node():

                    # Add the left subtree of the parent to t1

                    join_tree = AVLTree()

                    join_tree.root = parent.left

                    join_tree.root.parent = None

                    t1.join(join_tree, parent.key, parent.value)

                    parent.left.parent = None

                current = parent



            # Remove the connection to the parent

            parent.left = None

            parent.right = None

            current = parent



        # Update the size of t1 and t2

        t1.sizeT = t1.size()

        t2.sizeT = t2.size()



        if t1.root:

            balanceT1 = t1.get_balance(t1.root)

        else:

            balanceT1 = 0

        if balanceT1 > 1 or balanceT1 < -1:

            # t1 is not balanced

            if balanceT1 > 1:

                t1.right_rotation(t1.root)

                t1.root = t1.root.parent

            if balanceT1 < -1:

                t1.left_rotation(t1.root)

                t1.root = t1.root.parent



            if t1.root.parent is not None:

                t1.root = t1.root.parent

        if t2.root:

            balanceT2 = t2.get_balance(t2.root)

        else:

            balanceT2 = 0

        if balanceT2 > 1 or balanceT2 < -1:

            # t2 is not balanced

            if balanceT2 > 1:

                t2.right_rotation(t2.root)

                t2.root = t2.root.parent

            if balanceT2 < -1:

                t2.left_rotation(t2.root)

                t2.root = t2.root.parent



            if t2.root.parent is not None:

                t2.root = t2.root.parent



        # The current tree and node are no longer valid

        self.root = None

        self.sizeT = 0

        return t1, t2



    """Takes a node and makes it balanced if it is not balanced



    @type node: AVLNode

    @rtype: void

    """



    def balancing(self, node):



        balance = self.get_balance(node)



        if balance in [-1, 0, 1]:



            return



        if balance > 1:



            self.right_rotation(node)



        else:



            self.left_rotation(node)



        node = node.parent



    """returns an array representing dictionary 



    @rtype: list

    @returns: a sorted list according to key of tuples (key, value) representing the data structure

    """



    def avl_to_array(self):

        result = []

        self.in_order_traversal(self.root, result)

        return result



    """Performs an inorder traversal on the subtree whose root is the given node



    @type node: AVLNode

    @rtype: void

    """



    def in_order_traversal(self, node, result):

        if not node or not node.is_real_node():

            return

        self.in_order_traversal(node.left, result)

        result.append((node.key, node.value))

        self.in_order_traversal(node.right, result)



    """returns the node with the maximal key in the dictionary



    @rtype: AVLNode

    @returns: the maximal node, None if the dictionary is empty

    """



    def max_node(self):

        curr = self.root

        while curr and curr.right.is_real_node():

            curr = curr.right

        return curr



    """returns the number of items in dictionary 



    @rtype: int

    @returns: the number of items in dictionary 

    """



    def size(self):

        return self.sizeT



    """returns the root of the tree representing the dictionary



    @rtype: AVLNode

    @returns: the root, None if the dictionary is empty

    """



    def get_root(self):

        return self.root
