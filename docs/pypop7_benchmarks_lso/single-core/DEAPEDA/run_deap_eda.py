# Taken directly from https://github.com/DEAP/deap/blob/master/examples/eda/emna.py
#    with slight modifications for comparisons (Here EMNA is a specific EDA version)
#
# Please first install deap (http://deap.readthedocs.org/):
#    $ pip install deap
import time
import pickle
import argparse
from operator import attrgetter

import numpy as np
from deap import base, creator
import pypop7.benchmarks.continuous_functions as cf  # for rotated and shifted benchmarking functions


def sphere(x):
    return cf.sphere(x),


def cigar(x):
    return cf.cigar(x),


def discus(x):
    return cf.discus(x),


def cigar_discus(x):
    return cf.cigar_discus(x),


def ellipsoid(x):
    return cf.ellipsoid(x),


def different_powers(x):
    return cf.different_powers(x),


def schwefel221(x):
    return cf.schwefel221(x),


def step(x):
    return cf.step(x),


def rosenbrock(x):
    return cf.rosenbrock(x),


def schwefel12(x):
    return cf.schwefel12(x),


class EMNA(object):  # Here EMNA is a specific EDA version (in fact)
    def __init__(self):
        self.dim = 2000
        self.centroid = np.random.uniform(-10.0, 10.0, size=(self.dim,))
        self.sigma = 2.0

    def generate(self, ind_init):
        arz = self.centroid + self.sigma*np.random.randn(200, self.dim)
        return list(map(ind_init, arz))

    def update(self, population):
        sorted_pop = sorted(population, key=attrgetter("fitness"), reverse=True)
        z = sorted_pop[:100] - self.centroid
        avg = np.mean(z, axis=0)
        self.sigma = np.sqrt(np.sum(np.sum((z - avg)**2, axis=1))/(100*self.dim))
        self.centroid += avg


def ea_generate_update(toolbox, start_time, ii):
    n_fe = 0  # number of function evaluations
    # to store a list of sampled function evaluations and best-so-far fitness
    fe, fitness = [], []

    while (time.time() - start_time) < (60*60*3):  # 3 hours
        population = toolbox.generate()
        fitnesses = toolbox.map(toolbox.evaluate, population)
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit
            n_fe += 1  # current number of function evaluations
            fe.append(n_fe)
            if len(fitness) == 0 or fitness[-1] > fit[0]:
                fitness.append(fit[0])
            else:
                fitness.append(fitness[-1])
        toolbox.update(population)

    fitness = np.vstack((fe, fitness)).T
    results = {'best_so_far_y': fitness[-1],
               'n_function_evaluations': n_fe,
               'runtime': time.time() - start_time,
               'fitness': fitness}
    filename = 'Algo-DEAPEDA_Func-{}_Dim-2000_Exp-{}.pickle'.format(f.__name__, ii)
    with open(filename, 'wb') as handle:
        pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print('*** runtime (seconds) ***:', time.time() - start_time)


def main(ff, ii):
    start_time = time.time()

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMin)
    strategy = EMNA()
    toolbox = base.Toolbox()
    toolbox.register("evaluate", ff)
    toolbox.register("generate", strategy.generate, creator.Individual)
    toolbox.register("update", strategy.update)
    ea_generate_update(toolbox, start_time, ii)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', '-i', type=int)  # experiment index
    args = parser.parse_args()
    params = vars(args)
    for f in [sphere, cigar, discus, cigar_discus, ellipsoid,
              different_powers, schwefel221, step, rosenbrock, schwefel12]:
        main(f, params['index'])
