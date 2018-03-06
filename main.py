# /* класс, описывающий само дерево */
class Tree:
    def __init__(self, data=None, root=None, left_child=None, right_child=None, parent=None):
        self.root = root  # корень дерева
        self.parent = parent
        self.left_child = left_child
        self.right_child = right_child
        self.data = data

    # /* функция для добавления узла в дерево. Узел является тем же деревом */
    def newNode(self, data, left_child=None, right_child=None, parent=None, root=None):
        return Tree(data=data, left_child=left_child, right_child=right_child, parent=parent, root=root)

    def __str__(self):
        return self.data

    # /* функция вычисляет вес дерева(в нашем случае вес каждого узла = 1).Необходима для балансирования дерева во время построения */
    def get_weight(self, curent_node):
        if curent_node is None:
            return 0
        else:
            height = self.get_weight(curent_node.left_child)
            height += self.get_weight(curent_node.right_child)
            height += 1
            return height

    # /* обёртка для основного метода __put_value для того что бы не забывать про рут */
    def put(self, data):
        if self.root:
            self._put_value(data=data, curent_node=self.root)
        else:
            self.root = self.newNode(data=data, root=self.root)

    # /* метод добавления значения в дерево. Каждая итерация анализирует вес потомков справа и слева, там где меньше
    # - туда и вставляем значение , если веса равны - идём слева направо
    def _put_value(self, data, curent_node):
        if curent_node.left_child and curent_node.right_child:
            if curent_node.left_child.get_weight(curent_node.left_child) > \
                    curent_node.right_child.get_weight(curent_node.right_child):
                return self._put_value(data=data, curent_node=curent_node.right_child)
            else:
                return self._put_value(data=data, curent_node=curent_node.left_child)
        if not curent_node.left_child:
            curent_node.left_child = self.newNode(data=data, parent=curent_node, root=curent_node.root)
        elif not curent_node.right_child:
            curent_node.right_child = self.newNode(data=data, parent=curent_node,root=curent_node.root)

    def extract(self):
        if self.root.left_child and self.root.right_child:
            return self._extract_value(self.root)
        else:
            data = self.root.data
            self.root = None
            return data

    def _extract_value(self, curent_node):
        if curent_node.left_child and curent_node.right_child:
            if curent_node.left_child.get_weight(curent_node.left_child) > \
                    curent_node.right_child.get_weight(curent_node.right_child):
                return self._extract_value(curent_node=curent_node.left_child)
            else:
                return self._extract_value(curent_node=curent_node.right_child)
        par = curent_node.parent
        if curent_node.right_child is None and curent_node.left_child is None:
            par.right_child = None
            return curent_node.data
        if curent_node.right_child is None:
            data = curent_node.left_child.data
            curent_node.left_child = None
            return data


OPERATORS = {
    "+": float.__add__,
    "-": float.__sub__,
    "*": float.__mul__,
    "/": float.__truediv__
}

test_reversed_notation = "8 2 5 * + 1 3 2 * + 4 - /"

polish_list = test_reversed_notation.split(" ")
list_len = len(polish_list)
polish_tree = Tree()

for each in ["1", "2", "3", "4", "5", "6", "7"]:
    polish_tree.put(each)

print("root = " + polish_tree.root.data)
print("left child = " + polish_tree.root.left_child.data)
print("left child _left_child = " + polish_tree.root.left_child.left_child.data)
print("left child _right_child = " + polish_tree.root.left_child.right_child.data)
print("right_child = " + polish_tree.root.right_child.data)
print("right_child _left_child =" + polish_tree.root.right_child.left_child.data)
print("right_child _right_child = " + polish_tree.root.right_child.right_child.data)

print(polish_tree.extract())
print(polish_tree.extract())
print(polish_tree.extract())
print(polish_tree.extract())
print(polish_tree.extract())
print(polish_tree.extract())
