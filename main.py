# /* класс, описывающий само дерево */
import unittest


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

    # /* метод добавления значения в дерево поштучно. Каждая итерация анализирует вес потомков справа и слева, там где меньше
    # - туда и вставляем значение , если веса равны - идём слева направо
    def _put_value(self, data, curent_node):
        if curent_node.left_child and curent_node.right_child:
            if curent_node.left_child.get_weight(curent_node.left_child) > \
                    curent_node.right_child.get_weight(curent_node.right_child):#оценка веса и соответственно принятие решения
                return self._put_value(data=data, curent_node=curent_node.right_child)
            else:
                return self._put_value(data=data, curent_node=curent_node.left_child)
        if not curent_node.left_child:
            curent_node.left_child = self.newNode(data=data, parent=curent_node, root=curent_node.root)
        elif not curent_node.right_child:
            curent_node.right_child = self.newNode(data=data, parent=curent_node, root=curent_node.root)

    # /* обёртка для _extract_value опят же для того что бы не забыть про рут
    def extract(self):
        if self.root.left_child or self.root.right_child:
            return self._extract_value(self.root)
        else:
            data = self.root.data
            self.root = None
            return data

    # /* метод который достаёт значения из дерева поштучно, идём в обратном направлении - справа налево и так же ориентируясь
    # на веса
    def _extract_value(self, curent_node):
        if curent_node.left_child and curent_node.right_child:
            if curent_node.left_child.get_weight(curent_node.left_child) > \
                    curent_node.right_child.get_weight(curent_node.right_child): #оценка веса и соответственно принятие решения
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


def reversed_polish_notation(expr):

    def tree_creator(expr):
        pl_list = expr.split(" ")
        pl_list.reverse()
        pl_tree = Tree()
        # создание дерева из данной польской записи
        for each in pl_list:
            pl_tree.put(each)
        return pl_tree

    #доступные операторы
    OPERATORS = {
        "+": float.__add__,
        "-": float.__sub__,
        "*": float.__mul__,
        "/": float.__truediv__
    }

    stack = []
    polish_tree = tree_creator(expr)
    while polish_tree.root is not None:
        val = polish_tree.extract()
        try:
            #если нет эксепшена значит перед нами цифра и можно помещать её в стек
            val = float(val)
            stack.append(val)
        except Exception:
            #определяем есть ли полученый из дерева оператор в доступных
            for each in val:
                if each not in OPERATORS.keys():
                    continue
                try:
                    #вычленяем из стака 2 последних операнда
                    operand1 = stack.pop()
                    operand2 = stack.pop()
                except Exception:
                    #недостаточно операндов
                    return False
                try:
                    #производим оперяцию связаную с найденым оператором
                    res = OPERATORS[each](operand2,operand1)
                except Exception:
                    #ошибка деления на ноль
                    return False
                stack.append(res)
    if len(stack) != 1:
        #в стеке должено оставатся только одно значение - результат
        return False
    return stack.pop()


class NegativeTest(unittest.TestCase):
    def runTest(self):
        self.assertFalse(reversed_polish_notation("+"))
        self.assertFalse(reversed_polish_notation("3 3"))
        self.assertFalse(reversed_polish_notation("1 + 2 "))
        self.assertFalse(reversed_polish_notation("1 1 + +"))


class PositiveTest(unittest.TestCase):
    def runTest(self):
        self.assertEqual(1,reversed_polish_notation("1"))
        self.assertEqual(3 + 1, reversed_polish_notation("3 1 +"))
        self.assertEqual(6,reversed_polish_notation("8 2 5 * + 1 3 2 * + 4 - /"))


negative = NegativeTest(methodName='runTest').run()
positive = PositiveTest(methodName='runTest').run()
print(negative)
print(positive)