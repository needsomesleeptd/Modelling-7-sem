import distirbutions as dst
import matplotlib.pyplot as plt

def get_table_floats(l: float, r: float, f, steps: int, f_hyperparams: list[float]) -> list:
    step_dst = (r - l) / steps
    cur_pos = l
    xs = []
    ys = []
    for i in range(steps):
        y_val = f(cur_pos, *f_hyperparams)
        xs.append(cur_pos)
        ys.append(y_val)
        cur_pos += step_dst
    return xs, ys



def get_table_ints(l: int, r: int, f, f_hyperparams: list[float]) -> list:
    cur_pos = l
    l = int(l)
    r = int(r)
    xs = []
    ys = []
    for cur_pos in range(l,r+1):
        y_val = f(cur_pos, *f_hyperparams)
        xs.append(cur_pos)
        ys.append(y_val)
        #cur_pos += step_dst
    return xs, ys



def draw_uniform_graph(l,r,steps_cnt = 10000):
    legend_dems = 'Равномерное распределение: R[' + str(l) + ';' + str(r) + ']'
    plt.title(legend_dems)
    xs, ys = get_table_floats(l,r, dst.UniformDistribution, steps_cnt, f_hyperparams=[l,r])
    plt.plot(xs,ys,label="Равномерное распределение")
    
    xs_dens,ys_dens  = get_table_floats(l,r,dst.UniformDistributionDensity,steps_cnt,f_hyperparams=[l,r])
    plt.plot(xs_dens,ys_dens,label = "Плотность равномерного распределения")
    plt.grid()
    plt.legend()
    plt.show()
        


def draw_poisson_graph(l,r,lambda_,steps_cnt = 10000):
    legend_dems = 'Пуассоновское распределение: P[' + str(lambda_) +  ']'
    plt.title(legend_dems)
    xs, ys = get_table_ints(l,r, dst.PoissonDistribution, [lambda_])
    plt.plot(xs,ys,label="Пуассоновское распределение")
    
    xs_dens,ys_dens  = get_table_ints(l,r,dst.PoissonDistributionDensity,[lambda_])
    plt.plot(xs_dens,ys_dens,label = "Плотность пуассоновского распределения")
    plt.grid()
    plt.legend()
    plt.show()
    
def draw_uniform_graph_subplot(l, r,l_p,r_p, steps_cnt=10000):
    """
    Draw a graph with uniform distribution and its density.

    Parameters:
    l (float): Lower bound of the uniform distribution.
    r (float): Upper bound of the uniform distribution.
    steps_cnt (int): Number of steps for the graph. Default is 10000.
    """
    fig, axs = plt.subplots(2, figsize=(8, 6))

    legend_dems = 'Равномерное распределение: R[' + str(l_p) + ';' + str(r_p) + ']'
    axs[0].set_title(legend_dems)
    xs, ys = get_table_floats(l, r, dst.UniformDistribution, steps_cnt, f_hyperparams=[l_p, r_p])
    axs[0].plot(xs, ys, label="Равномерное распределение")
    axs[0].grid()
    axs[0].legend()

    xs_dens, ys_dens = get_table_floats(l, r, dst.UniformDistributionDensity, steps_cnt, f_hyperparams=[l_p, r_p])
    axs[1].plot(xs_dens, ys_dens, label="Плотность равномерного распределения")
    axs[1].set_title("Плотность равномерного распределения")
    axs[1].grid()
    axs[1].legend()
    plt.subplots_adjust(hspace=0.5)  # Increase space between rows
    plt.savefig("uniform.png")
    #plt.tight_layout()
    plt.show()


def draw_poisson_graph_suplot(l, r, lambda_, steps_cnt=10000):
    """
    Draw a graph with Poisson distribution and its density.

    Parameters:
    l (int): Lower bound of the Poisson distribution.
    r (int): Upper bound of the Poisson distribution.
    lambda_ (float): Lambda parameter of the Poisson distribution.
    steps_cnt (int): Number of steps for the graph. Default is 10000.
    """
    fig, axs = plt.subplots(2, figsize=(8, 6))

    legend_dems = 'Пуассоновское распределение: P[' + str(lambda_) + ']'
    axs[0].set_title(legend_dems)
    xs, ys = get_table_ints(l, r, dst.PoissonDistribution, [lambda_])
    axs[0].plot(xs, ys, label="Пуассоновское распределение")
    axs[0].grid()
    axs[0].legend()

    xs_dens, ys_dens = get_table_ints(l, r, dst.PoissonDistributionDensity, [lambda_])
    axs[1].plot(xs_dens, ys_dens, label="Плотность пуассоновского распределения")
    axs[1].set_title("Плотность пуассоновского распределения")
    axs[1].grid()
    axs[1].legend()
    plt.subplots_adjust(hspace=0.5)  # Increase space between rows
    plt.savefig("poisson.png")
    #plt.tight_layout()
    plt.show()