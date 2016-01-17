from cas import *

import unittest

class CASTest(unittest.TestCase):

    def test_add(self):
        term1 = Multiply([N(2), Var('x'), Var('y')])
        term2 = Multiply([N(3), Var('x'), Var('x')])
        term3 = Multiply([N(4), Var('y'), Var('x')])
        total = Add([term1, term2, term3])
        expected_ans = Add([
            Multiply([N(6), Var('x'), Var('y')]),
            Multiply([N(3), VarExponent('x', 2)])
        ])
        self.assertEqual(total, expected_ans)

    def test_distribute(self):
        term1 = Add([N(2), Var('x')])
        term2 = Add([N(3), Var('x')])
        total = Multiply([term1, term2])
        expected_ans = Add([
            VarExponent('x', 2),
            Multiply([N(5), Var('x'),]),
            N(6),
        ])
        self.assertEqual(total, expected_ans)

    def test_derivative(self):
        d_x = Var('x').derivative('x')
        self.assertEqual(d_x, N(1))

        d_xy = Var('x').derivative('y')
        self.assertEqual(d_xy, N(0))

        d_x2 = VarExponent('x', 2).derivative('x')
        self.assertEqual(d_x2, Multiply([N(2), Var('x')]))

        fn = Add([
            Multiply([Var('x'), VarExponent('y', 2), N(5)]),
            Multiply([VarExponent('x', 3), Var('y'), N(2)])
        ])
        expected_ans = Add([
            Multiply([VarExponent('y', 2), N(5)]),
            Multiply([VarExponent('x', 2), Var('y'), N(6)])
        ])
        # print(fn.derivative('x'))
        # print(expected_ans)
        self.assertEqual(fn.derivative('x'), expected_ans)

if __name__ == '__main__':
    unittest.main()