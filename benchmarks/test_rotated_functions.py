import unittest

from benchmarks.base_functions import sphere as base_sphere
from benchmarks.rotated_functions import *
from benchmarks.rotated_functions import _load_rotation_matrix
from test_cases import *


# helper function
def _check_rotation_matrix(x, error=1e-6):
    x = np.mat(x)
    if x.shape[0] != x.shape[1]:
        raise TypeError('rotation matrix should be a square matrix.')
    a = np.abs(np.matmul(x, x.transpose()) - np.eye(x.shape[0])) < error
    b = np.abs(np.matmul(x.transpose(), x) - np.eye(x.shape[0])) < error
    c = np.abs(np.sum(np.power(x, 2), 0) - 1) < error
    d = np.abs(np.sum(np.power(x, 2), 1) - 1) < error
    e = np.linalg.matrix_rank(x) == x.shape[0]
    return np.all(a) and np.all(b) and np.all(c) and np.all(d) and e


class Test(unittest.TestCase):
    def test_generate_rotation_matrix(self):
        func, ndim, seed = 'sphere', 100, 0
        x = generate_rotation_matrix(func, ndim, seed)
        self.assertTrue(_check_rotation_matrix(x))
        data_folder = 'pypop_benchmarks_input_data'
        data_path = os.path.join(data_folder, 'rotation_matrix_' + func + '_dim_' + str(ndim) + '.txt')
        x = np.loadtxt(data_path)
        self.assertTrue(_check_rotation_matrix(x))

    def test_load_rotation_matrix(self):
        func, ndim, seed = base_sphere, 2, 1
        generate_rotation_matrix(func, ndim, seed)
        rotation_matrix = [[7.227690004350708630e-01, 6.910896989610599839e-01],
                           [6.910896989610598729e-01, -7.227690004350709740e-01]]
        self.assertTrue(np.allclose(_load_rotation_matrix(func, np.ones(ndim,)), rotation_matrix))
        rotation_matrix = np.eye(ndim)
        self.assertTrue(np.allclose(_load_rotation_matrix(func, np.ones(ndim,), rotation_matrix), rotation_matrix))

    def test_sphere(self):
        sample = TestCases(is_rotated=True)
        for func in [sphere, Sphere()]:
            for ndim in range(1, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_sphere(ndim - 1)))
            self.assertTrue(sample.check_origin(func))

    def test_cigar(self):
        sample = TestCases(is_rotated=True)
        for func in [cigar, Cigar()]:
            for ndim in range(2, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_cigar(ndim - 2)))
            with self.assertRaisesRegex(TypeError, 'The size should > 1+'):
                sample.compare(func, 1, np.empty((5,)))
            self.assertTrue(sample.check_origin(func))

    def test_discus(self):
        sample = TestCases(is_rotated=True)
        for func in [discus, Discus()]:
            for ndim in range(2, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_discus(ndim - 2)))
            with self.assertRaisesRegex(TypeError, 'The size should > 1+'):
                sample.compare(func, 1, np.empty((5,)))
            self.assertTrue(sample.check_origin(func))

    def test_cigar_discus(self):
        sample = TestCases(is_rotated=True)
        for func in [cigar_discus, CigarDiscus()]:
            for ndim in range(2, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_cigar_discus(ndim - 2)))
            with self.assertRaisesRegex(TypeError, 'The size should > 1+'):
                sample.compare(func, 1, np.empty((5,)))
            self.assertTrue(sample.check_origin(func))

    def test_ellipsoid(self):
        sample = TestCases(is_rotated=True)
        for func in [ellipsoid, Ellipsoid()]:
            for ndim in range(2, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_ellipsoid(ndim - 2)))
            with self.assertRaisesRegex(TypeError, 'The size should > 1+'):
                sample.compare(func, 1, np.empty((5,)))
            self.assertTrue(sample.check_origin(func))

    def test_different_powers(self):
        sample = TestCases(is_rotated=True)
        for func in [different_powers, DifferentPowers()]:
            for ndim in range(2, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_different_powers(ndim - 2), atol=0.1))
            with self.assertRaisesRegex(TypeError, 'The size should > 1+'):
                sample.compare(func, 1, np.empty((5,)))
            self.assertTrue(sample.check_origin(func))

    def test_schwefel221(self):
        sample = TestCases(is_rotated=True)
        for func in [schwefel221, Schwefel221()]:
            for ndim in range(1, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_schwefel221(ndim - 1)))
            self.assertTrue(sample.check_origin(func))

    def test_step(self):
        sample = TestCases(is_rotated=True)
        for func in [step, Step()]:
            for ndim in range(1, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_step(ndim - 1)))
            self.assertTrue(sample.check_origin(func))

    def test_schwefel222(self):
        sample = TestCases(is_rotated=True)
        for func in [schwefel222, Schwefel222()]:
            for ndim in range(1, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_schwefel222(ndim - 1)))
            self.assertTrue(sample.check_origin(func))

    def test_rosenbrock(self):
        sample = TestCases(is_rotated=True)
        for func in [rosenbrock, Rosenbrock()]:
            for ndim in range(2, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_rosenbrock(ndim - 2)))
            with self.assertRaisesRegex(TypeError, 'The size should > 1+'):
                sample.compare(func, 1, np.empty((5,)))

    def test_schwefel12(self):
        sample = TestCases(is_rotated=True)
        for func in [schwefel12, Schwefel12()]:
            for ndim in range(2, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_schwefel12(ndim - 2)))
            with self.assertRaisesRegex(TypeError, 'The size should > 1+'):
                sample.compare(func, 1, np.empty((5,)))
            self.assertTrue(sample.check_origin(func))

    def test_griewank(self):
        sample = TestCases(is_rotated=True)
        for func in [griewank, Griewank()]:
            for ndim in range(2, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_griewank(ndim - 2), atol=0.001))
            self.assertTrue(sample.check_origin(func))

    def test_ackley(self):
        sample = TestCases(is_rotated=True)
        for func in [ackley, Ackley()]:
            for ndim in range(2, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_ackley(ndim - 2), atol=0.001))
            self.assertTrue(sample.check_origin(func))

    def test_rastrigin(self):
        sample = TestCases(is_rotated=True)
        for func in [rastrigin, Rastrigin()]:
            for ndim in range(2, 8):
                self.assertTrue(sample.compare(func, ndim, get_y_rastrigin(ndim - 2)))
            self.assertTrue(sample.check_origin(func))


if __name__ == '__main__':
    unittest.main()
