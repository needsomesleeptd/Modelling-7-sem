import plots as p
menu = '''
    1. Получить графики закона и плотности равномерного распределения
    2. Получить графики закона и плотности распределения Пуассона
    3. Выход
'''

def main_loop():
    choice = -1
    while choice != 3:
        print(menu)
        choice = int(input('Введите номер действия: '))
        if choice == 1:
            l,r = list(map(float,input("Введите  диапазон (l,r) отображения: ").split()))
            l_p,r_p = list(map(float,input("Введите параметры равномерного распределения (a,b): ").split()))
            p.draw_uniform_graph_subplot(l,r,l_p,r_p)
        elif choice == 2:
            l,r = list(map(float,input("Введите  диапазон (l,r) отображения: ").split()))
            lambda_st =input("Введите параметры пуассоновского распределения (lambda):")
            lambda_ = int(lambda_st)
            p.draw_poisson_graph_suplot(l,r,lambda_)
        elif choice == 3:
            break
main_loop()