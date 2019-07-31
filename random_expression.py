# /*функция-генератор случайных алгебраических выражений
import random

def random_expression():

    def swithcer():
        """
        случайный генератор скобки
        """
        switcher_dict = {'1': '(', '0': ')'}
        while True:
            if random.randint(0, 1) == 1:
                yield switcher_dict['1']
                switcher_dict = {'1': switcher_dict['0'], '0': switcher_dict['1']}
            else:
                yield ''

    def gen_atom_expression():
        """
        генератор случайного минимального алгебраического выражения
        вида значение - оператор - значение
        """
        #генерация листа случайной длины
        #для создания случайного кол-ва атомарных выражений
        rnd_lst = [''] * random.randint(20, 45)
        bracket = swithcer()
        while len(rnd_lst) != 0:
            operator = random.choice(OPERATORS)
            #если оператор - логарифм или степень
            #ограничение диапазона случайных чисел (избежать больших значений)
            if operator == 'log':
                value1 = round(random.uniform(2, 10), 2)
                value2 = round(random.uniform(0, 10), 2)
                #если второй оператор логарифма меньши либо равен 1
                #берем логарифм по первому оператору (натуральный логарифм)
                if value2 <= 1:
                    yield f'{operator}({value1})'
                else:
                #иначе берем логарифм по второму значению
                    yield f'{operator}({value1},{value2})'

                continue

            if operator == '^':
                value1 = round(random.uniform(-10, 10), 2)
                value2 = round(random.uniform(-10, 10), 2)
            else:
                value1 = round(random.uniform(-100, 1000), 2)
                value2 = round(random.uniform(-100, 1000), 2)

            #рандомная вставка скобки
            s = next(bracket)
            if s == '(':
                yield f'{value1} {operator} {s} {value2}'
            elif s == ')':
                yield f'{value1} {s} {operator} {value2}'

            rnd_lst.pop()


    def remove_bracket(expression_string):
        expression_list = expression_string.split(' ')
        expression_list.reverse()
        s1 = expression_list.index('(')
        s2 = expression_list.index(')')
        if s1 < s2:
            expression_list.remove('(')
        expression_list.reverse()

        return ' '.join(expression_list)

    #операторы для построения выражений
    OPERATORS = [
        '+',
        '-',
        '*',
        '/',
        '^',
        'log'
    ]

    #список атомарных выражений, полученных из генератора
    data = list(gen_atom_expression())
    expr_list = []
    #цикл добавления случайных операторов между атомарными выраженями
    for a in range(0, len(data)):
        if a == len(data)-1:
            expr_list.extend([data[a]])
            break
        expr_list.extend([data[a], ' ', random.choice(['+', '-', '/', '*']), ' '])

    expression_string = ''.join(expr_list)
    #print(expression_string)
    #очистка выражения от лишней скобки
    expression_string = remove_bracket(expression_string)
    return expression_string



print(random_expression())
