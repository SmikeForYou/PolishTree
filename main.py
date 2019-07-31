# /* класс, описывающий само дерево */
import unittest
from math import log, e
import re

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
        #закомичено, уже передается лист
        #pl_list = expr.split(" ")
        expr.reverse()
        pl_tree = Tree()
        # создание дерева из данной польской записи
        for each in expr:
            pl_tree.put(each)
        return pl_tree


    def translate_to_polish_notation(expression):
        """
        функция перевода выражения в обратную польскую строку
        """
        def expression_to_list(expression):
            """
            функция перевода введенного выражения в
            список елементов
            поддержка float, скобок
            """
            OPERATORS = SYMBOLS.copy()
            #удалям закрывающую скобку для правильной интерпритации операторов
            #после нее
            del OPERATORS[')']

            pattern = '\((.+)\)'
            expression = expression.replace(' ', '')
            result = []
            number = ''
            symb_operator = ''
            last_symbol = 0
            #проход по каждому елементу выражения
            for i in range(0, len(expression)):
                #пропуск итераций при обработке символьного оператора (например log(x))
                if i < last_symbol:
                    continue

                #если оператор скобка - добавляем
                if expression[i] == '(' or expression[i] == ')':
                    result.append(expression[i])
                    continue
                #если елемент - оператор
                #проверка последнего значения в результуещем списке
                if len(result) > 0:
                    last_operator = result[-1] not in OPERATORS
                else:
                    last_operator = True
                #если последнее и текущее значения - операторы, то текущий символ это
                #часть отрицательного числа
                if expression[i] in OPERATORS and last_operator:
                    result.append(expression[i])
                    continue

                #символьные операторы
                if expression[i].isalpha():
                    """
                    выражение с использованием символьных операторов
                    вида operator(a, b) транслируются в итоговый лист
                    в виде [..., a, operator, b, ...] для упрощения
                    перевода в обратную польскую нотацию
                    """
                    if expression[i:i+3] == 'log':
                        #поиск закрывающей скобки символьного оператора
                        last_symbol = expression[i:].find(')') + i + 1
                        log_expr = expression[i:last_symbol]
                        #очистка выражения по паттерну через re
                        values = re.search(pattern=pattern,string=log_expr).group(1)
                        values = values.split(',')
                        #проверка получившегося листа значений
                        #если длина 1 - добавляем e (натуральный логарифм)
                        if len(values) == 1:
                            values.append('log')
                            values.append(str(e))
                        elif len(values) == 2:
                            values.insert(1, 'log')
                        else:
                            return False

                        result.extend(values)
                        continue

                try:
                    #отлов ексепшена последнего елемента
                    if expression[i+1] in SYMBOLS:
                        number += expression[i]
                        result.append(number)
                        number = ''
                        continue
                except IndexError:
                    number += expression[i]
                    result.append(number)

                number += expression[i]
            return result


        SYMBOLS = {
            '+': 0,
            '-': 0,
            '*': 3,
            '/': 3,
            '(': 2,
            ')': 2,
            '^': 4,
            'log':5
        }

        expression = expression_to_list(expression)
        stack_vals = []
        polish_string = []
        for element in expression:
            #последний елемент в стеке
            if len(stack_vals) > 0:
                last_stack_operand = stack_vals[-1]
            #если елемент не в списке символов - он число
            #запись в польскую строку и переход на следующий елемент
            if element not in SYMBOLS:
                polish_string.append(element)
                continue

            #если стек пустой или последний/текущий елемент стека "("
            #добавляем операнд и переходим к следующему елементу
            if len(stack_vals) == 0 or last_stack_operand == '(' or element == '(':
                stack_vals.append(element)
                continue

            #если закрываюшая скобка
            if element == ')':
                #если открывающая скобка в стеке
                #выкидываем стек в польскую строку
                if '(' in stack_vals:
                    while len(stack_vals) != 0:
                        operand = stack_vals.pop()
                        if operand == '(':
                            break
                        polish_string.append(operand)
                    continue
                #если открывающая скобки нет в стеке
                #выражение неправильно
                else:
                    return False

            #проверка приоритета операнда с последним в стеке
            if SYMBOLS[last_stack_operand] >= SYMBOLS[element]:
                polish_string.append(stack_vals.pop())
                stack_vals.append(element)
            else:
                stack_vals.append(element)

        while len(stack_vals) != 0:
            polish_string.append(stack_vals.pop())

        return polish_string


    def log_func(operand1, operand2):
        return log(operand1, operand2)


    #доступные операторы
    OPERATORS = {
        "+": float.__add__,
        "-": float.__sub__,
        "*": float.__mul__,
        "/": float.__truediv__,
        "^": float.__pow__,
        "log": log_func
    }

    stack = []
    polish_string = translate_to_polish_notation(expr)
    #print(polish_string)
    polish_tree = tree_creator(polish_string)
    while polish_tree.root is not None:
        val = polish_tree.extract()
        try:
            #если нет эксепшена значит перед нами цифра и можно помещать её в стек
            val = float(val)
            stack.append(val)
        except Exception:
            #определяем есть ли полученый из дерева оператор в доступных
            #не понял, нафига тут цикл for...
            #поэтому пока перезагружаю each насильно
            for each in val:
                if each == 'l':
                    each = 'log'
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
