class Expr(object):
    def __init__(self):
        self.const_factor = 1

    def hashstr(self):
        '''
        A unique identifier for the expr, except for any
        constant factors.
        '''
        return str(self)

    def get_const_factor(self):
        return self.const_factor

class Add(Expr):

    def __init__(self, terms):
        self.terms = terms
        self.simplify()

    def simplify(self):
        flattened_terms = []
        for term in self.terms:
            if isinstance(term, Add):
                flattened_terms += term.terms
            else:
                flattened_terms.append(term)

        const_factors = {}
        variables = {}
        for term in self.terms:
            if term.hashstr() in const_factors:
                const_factors[term.hashstr()] += term.get_const_factor()
            else: 
                const_factors[term.hashstr()] = term.get_const_factor()
                variables[term.hashstr()] = term

        new_terms = []
        for hashstr, const in const_factors.items():
            new_terms.append(variables[hashstr])
            new_terms[-1].const_factor = const

        self.terms = new_terms

    def __str__(self):
        string = ''
        for term in self.terms:
            string += str(term) + ' + '
        return string[:-3]

# 5 + 3x + 2y
# Add(5, Add(3x, 2y))  binary
# Add(5, 3x, 2y)       flat

# 4 + 3x + 2y + z + 2x
# Add(4, Add(3x, Add(2y, Add(z, 2x))))

class Multiply(Expr):
    '''
    [Multiply(5, x), Multiply(2, y), x]
    [5, x, 2, y, x]
        -> [10, x^2, y]
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
        string = str(self.const_factor)
        for term in self.terms:
            string += str(term)
        return string

    def hashstr(self):
        # Hashing for adding.
        term_strings = []
        for term in self.terms:
            term_strings.append(str(term))
        term_strings.sort()
        return ''.join(term_strings)

class VarExponent(Expr):
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