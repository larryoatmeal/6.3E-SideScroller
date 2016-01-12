class Expr(object):
    '''
    Every possible expression is an instance of Expr.  Subclasses include
    variables (VarExponent), operations (Add), and constants (N).
    '''
    def __init__(self):
        self.const_factor = 1

    def hashstr(self):
        '''
        A unique identifier for the expr, except for any
        constant factors.
        '''
        return str(self)

    def get_const_factor(self):
        '''
        Every expression is responsible for tracking the constant factor that
        it is multiplied by.
        '''
        return self.const_factor

class Add(Expr):
    '''
    Represents the sum of several other Expr's.
    For example: Add([N(5), Add(Var('x'), Var('y))])
    Currently supports the following simplification operations:
    - Grouping variables by hashstr: x + 2x -> 3x
    - Flattening nested Add's: Add(x, Add([y, z])) -> Add([x, y, z])
    '''

    def __init__(self, terms):
        self.terms = terms
        self.simplify()

    def simplify(self):
        # Flatten recursive adds.
        flattened_terms = []
        for term in self.terms:
            if isinstance(term, Add):
                flattened_terms += term.terms
            else:
                flattened_terms.append(term)

        # Group all the terms by their hashstr.
        const_factors = {}
        variables = {}
        for term in self.terms:
            if term.hashstr() in const_factors:
                const_factors[term.hashstr()] += term.get_const_factor()
            else: 
                const_factors[term.hashstr()] = term.get_const_factor()
                variables[term.hashstr()] = term

        # Rebuild the terms.
        new_terms = []
        for hashstr, const in const_factors.items():
            new_terms.append(variables[hashstr])
            new_terms[-1].const_factor = const

        # Check for zeroes
        newer_terms = []
        for i in new_terms:
            if i.const_factor != 0:
                newer_terms.append(i)

        self.terms = newer_terms

    def __str__(self):
        # Combine the terms with a + symbol.  This is good for hashstr as well.
        term_strings = []
        for term in self.terms:
            term_strings.append(str(term))
        term_strings.sort()
        return '+'.join(term_strings)

class Multiply(Expr):
    '''
    Represents the product of some Expr's.
    Simplification supports the following operations:
    - Flattening nested Multiply's.
    - Combining variables together into powers: x * x^2 -> x^3
    '''

    def __init__(self, terms):
        self.terms = terms
        self.const_factor = 1
        self.simplify()

    def simplify(self):
        new_terms = []
        # Flatten recursive multiplies
        for term in self.terms:
            if isinstance(term, Multiply):
                for t2 in term.terms:
                    new_terms.append(t2)
            else:
                new_terms.append(term)
        self.terms = new_terms

        # Agglomerate variables of same name.
        vars_seen = {}  # name -> power
        self.const_factor = 1.0
        for term in self.terms:
            if isinstance(term, VarExponent):
                if term.name in vars_seen:
                    vars_seen[term.name] += term.power
                else:
                    vars_seen[term.name] = term.power
            elif isinstance(term, N):
                self.const_factor *= term.const_factor
            elif isinstance(term, Add):
                # TODO
                pass

        # Rebuild the terms
        self.terms = []
        for name, power in vars_seen.items():
            new_term = VarExponent(name, power)
            self.terms.append(new_term)

    def __str__(self):
        return str(self.const_factor) + self.hashstr()

    def hashstr(self):
        # Hashing for adding.
        term_strings = []
        for term in self.terms:
            term_strings.append(str(term))
        term_strings.sort()
        return ''.join(term_strings)

class VarExponent(Expr):
    '''
    Represents a single variable to some power: x^3.
    '''
    def __init__(self, name, power):
        super(VarExponent, self).__init__()
        self.name = name
        self.power = power

    def __str__(self):
        out_str = self.name
        if self.power != 1:
            out_str += '^' + str(self.power)
        return out_str

class Var(VarExponent):
    def __init__(self, name):
        super(Var, self).__init__(name, 1)

    def __str__(self):
        return self.name

class N(Expr):
    '''
    Represents a number, like 42.
    '''
    def __init__(self, val):
        self.const_factor = val

    def __str__(self):
        return str(self.const_factor)

    def hashstr(self):
        return '1'


term1 = Multiply([N(2), Var('x'), Var('y')])
term2 = Multiply([N(3), Var('x'), Var('x')])
term3 = Multiply([N(4), Var('y'), Var('x')])
total = Add([term1, term2, term3])
print(total)

# THIS DOESN'T CURRENTLY WORK
term1 = Add([N(2), Var('x')])
term2 = Add([N(3), Var('x')])
total = Multiply([term1, term2])
print(total)

# Test the 0 eliminator
ans = Add([Var('x'), Multiply([N(-1), Var('x')]), N(5)])
print('This should print 5 if the 0 eliminator in the add function works: ' + str(ans))
