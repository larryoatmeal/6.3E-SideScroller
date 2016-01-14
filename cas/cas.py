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

    def derivative(self, base):
        return N(0)

    def simplify(self):
        return self

    def __eq__(self, other):
        return type(self) == type(other) and str(self) == str(other)

def Add(terms):
    return AddCls(terms).simplify()

class AddCls(Expr):
    '''
    Represents the sum of several other Expr's.
    For example: Add([N(5), Add(Var('x'), Var('y))])
    Currently supports the following simplification operations:
    - Grouping variables by hashstr: x + 2x -> 3x
    - Flattening nested Add's: Add(x, Add([y, z])) -> Add([x, y, z])
    '''

    def __init__(self, terms):
        super(AddCls, self).__init__()
        self.terms = terms

    def simplify(self):
        # Flatten recursive adds.
        flattened_terms = []
        for term in self.terms:
            if isinstance(term, AddCls):
                flattened_terms += term.terms
            else:
                flattened_terms.append(term)

        # Group all the terms by their hashstr.
        const_factors = {}
        variables = {}
        for term in flattened_terms:
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

        return AddCls(newer_terms)

    def __str__(self):
        # Combine the terms with a + symbol.  This is good for hashstr as well.
        term_strings = []
        for term in self.terms:
            term_strings.append(str(term))
        term_strings.sort()
        final_string = ''
        count = 0
        for term in term_strings:
            if count == 0:
                count += 1
                final_string += term
                continue
            if term[0] == "-":
                final_string += "-" + term[1:]
            else:
                final_string += "+" + term
        return final_string

    def derivative(self, base):
        new_terms = []
        for term in self.terms:
            new_terms.append(term.derivative(base))
        return AddCls(new_terms)

def Multiply(terms):
    return MultiplyCls(terms).simplify()

class MultiplyCls(Expr):
    '''
    Represents the product of some Expr's.
    Simplification supports the following operations:
    - Flattening nested Multiply's.
    - Combining variables together into powers: x * x^2 -> x^3
    '''

    def __init__(self, terms):
        super(MultiplyCls, self).__init__()
        self.terms = terms
        self.const_factor = 1

    def simplify(self):
        new_terms = []
        # Flatten recursive multiplies
        for term in self.terms:
            if isinstance(term, MultiplyCls):
                self.const_factor *= term.const_factor
                for t2 in term.terms:
                    new_terms.append(t2)
            else:
                new_terms.append(term)
        self.terms = new_terms

        # Agglomerate variables of same name.
        vars_seen = {}  # name -> power
        for term in self.terms:
            if isinstance(term, VarExponent):
                if term.name in vars_seen:
                    vars_seen[term.name] += term.power
                else:
                    vars_seen[term.name] = term.power
            elif isinstance(term, N):
                self.const_factor *= term.const_factor
            elif isinstance(term, AddCls):
                # TODO
                return mult_add_distribute(self.terms)

        # Rebuild the terms
        new_terms = []
        for name, power in vars_seen.items():
            new_term = VarExponent(name, power)
            new_terms.append(new_term)
        new_mult = MultiplyCls(new_terms)
        # print(self.const_factor)
        new_mult.const_factor = self.const_factor
        # print(new_mult)
        return new_mult


    def __str__(self):
        if self.const_factor != 1:
            const_factor_str = str(self.const_factor)
        else:
            const_factor_str = ''
        return const_factor_str + self.hashstr()

    def hashstr(self):
        # Hashing for adding.
        term_strings = []
        for term in self.terms:
            term_strings.append(str(term))
        term_strings.sort()
        return ''.join(term_strings)

    def derivative(self, base):
        '''
        f(x) * g(x) * h(x) * ...
        Just f and g: f'g + fg'
        f, g, and h: (f'g + fg')h + fgh'
            = f'gh + fg'h + fgh'
        '''
        add_terms = []
        term_prime = []
        for term in self.terms:
            term_prime.append(term.derivative(base))

        for add_term_i in range(len(self.terms)):
            mult_term = []
            for mult_term_i in range(len(self.terms)):
                if add_term_i == mult_term_i:
                    mult_term.append(self.terms[mult_term_i].derivative(base))
                else:
                    mult_term.append(self.terms[mult_term_i])
            mult = Multiply(mult_term)
            mult.const_factor *= self.const_factor
            add_terms.append(mult)
        return Add(add_terms)

def mult_add_distribute(terms):
    for i, term in enumerate(terms):
        if not isinstance(term, AddCls):
            continue
        distributed_terms = []
        for add_term in term.terms:
            this_mult = Multiply(terms[:i] + [add_term] + terms[i+1:])
            distributed_terms.append(this_mult)
        final_add = Add(distributed_terms)
        return final_add
    return Multiply(terms)

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

    def derivative(self, base):
        if self.name != base:
            return N(0)
        if self.power == 1:
            return N(1)
        if self.power == 0:
            return N(0)

        new_var_exp = VarExponent(self.name, self.power-1)
        const_factor = self.power
        return Multiply([N(const_factor), new_var_exp])

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

    def derivative(self, base):
        return N(0)

def Exponent( expression, power):

    terms = [ N(expression.const_factor ** power) ]
    for term in expression.terms:
        multipliedTerm = []
        for i in range( power ):
            multipliedTerm.append( term )
        terms.append( Multiply( multipliedTerm ))
    return Multiply(terms)



# # Test the 0 eliminator
# ans = Add([Var('x'), Multiply([N(-1), Var('x')]), N(5)])
# print('This should print 5 if the 0 eliminator in the add function works: ' + str(ans))

# # Test that negatives format correctly in adds
# print(Add([N(6), Multiply([Var('x'), N(1)])]))

# # Test that full exponentiation works
# print( Exponent( Multiply( [N(2), Exponent( Multiply( [N(2), Var('x') ]), 2 ), Var('y')]) , 3) )
