#   Ecem Ilgun
#   CS315 - Fall'16 - HW2

# I assumed the following :
#   - Each x, y, z etc. will be type Var (not the built-in str)
#   - Derivative only consists of the derivative of following : f(x).g(x) , f(x)/g(x), f(x) + g(x) and f(x) - g(x)
#   because we defined only addition, multiplication, subtraction and division
#   -My derivatives do not follow the exact order, for instance I could compute (x*0 + 1*y) as (0*x + 1*y) instead
#   however, since my implementation of derivative always turns out to be the same, I didn't care about the commutativity problem

def main():
    x = Var("x")
    y = Var("y")
    z = Var("z")
    e = 3 + (x + 2 * y) * z;

    print evaluate(x, x=3)
    print evaluate(e, **{"x": 3, "y": 4, "z": 2})
    print evaluate(e, x=3, y=-1, z=4)
    print

    print (((x)+y)*(3+x)).string()
    print (((x)+y)*(3+x)).desc()
    print

    print derivative(x *x*x + 5*x, x).string() # x*0+1*y
    print derivative(2 * x * x + 3 * x + 5, x).string() # 2*x*1+(2*1+0*x)*x+(3*1+0*x)+0
    print derivative(x*y, x).string() # x*0+1*y

    print e.string()
    print e.desc()
    print

    print x.string()
    print x.desc()
    print

    print (x + 3).string()
    print (x + 3).desc()
    print

    print (3 + x).string()
    print (3 + x).desc()
    print

    print (y * (x + 1)).string()
    print (y * (x + 1)).desc()
    print

    print ((x + 1) * y).string()
    print ((x + 1) * y).desc()
    print

    print (x * y + 3).string()
    print (x * y + 3).desc()
    print

    print (x + y + 3).string()
    print (x + y + 3).desc()
    print

    print ((x + y) + 3).string()
    print ((x + y) + 3).desc()
    print

    print (x + (y + 3)).string()
    print (x + (y + 3)).desc()
    print

    print (((x) + y) * (3 + x)).string()
    print (((x) + y) * (3 + x)).desc()
    print

    print ((4 + 3 * x) * 3 + 5).string()
    print ((4 + 3 * x) * 3 + 5).desc()
    print


import operator


def evaluate(expr, **namedValues):
    return expr.eval(namedValues)


def derivative(expr, var2):
    return expr.derv(var2)


class Expr:
    def eval(self, values):
        raise NotImplementedError()

    def desc(self):
        raise NotImplementedError()

    def string(self):
        raise NotImplementedError()

    def derv(self, var2):
        raise NotImplementedError()


class VarExpr(Expr):
    def __init__(self, var):
        self.var = var

    def eval(self, values):
        return values[self.var.getName()]

    def desc(self):
        return "VarExpr(" + self.var.desc() + ")"

    def string(self):
        return self.var.getName()

    def derv(self, var2):
        #if (self.var == var2):
        #    return LiteralExpr(1)
        #else:
        #    return LiteralExpr(0)
        return self.var.derv(var2)


class LiteralExpr(Expr):
    def __init__(self, val):
        self.val = val

    def eval(self, values):
        return self.val

    def desc(self):
        return "LiteralExpr(" + str(self.val) + ")"

    def string(self):
        return str(self.val)

    def derv(self, var):
        return LiteralExpr(0)


def opToSign(op):
    if (op == operator.__add__):
        return "+"
    if (op == operator.__sub__):
        return "-"
    if (op == operator.__mul__):
        return "*"
    if (op == operator.__div__):
        return "/"
    raise NotImplementedError()


def opToPrecedence(op):
    if (op == operator.__add__ or op == operator.__sub__):
        return 0
    if (op == operator.__mul__ or op == operator.__div__):
        return 1
    raise NotImplementedError()


class BinaryExpr(Expr):
    def __init__(self, op, lhs, rhs):
        self.op = op;
        self.lhs = lhs
        self.rhs = rhs

    def __add__(self, val):
        if (isinstance(val, int)):
            return BinaryExpr(operator.__add__, self, LiteralExpr(val))
        elif (isinstance(val, Var)):
            return BinaryExpr(operator.__add__, self, VarExpr(val))
        else:
            return BinaryExpr(operator.__add__, self, val)

    def __radd__(self, val):
        if (isinstance(val, int)):
            return BinaryExpr(operator.__add__, LiteralExpr(val), self)
        elif (isinstance(val, Var)):
            return BinaryExpr(operator.__add__, VarExpr(val), self)
        else:
            return BinaryExpr(operator.__add__, val, self)

    def __sub__(self, val):
        if (isinstance(val, int)):
            return BinaryExpr(operator.__sub__, self, LiteralExpr(val))
        elif (isinstance(val, Var)):
            return BinaryExpr(operator.__sub__, self, VarExpr(val))
        else:
            return BinaryExpr(operator.__sub__, self, val)

    def __rsub__(self, val):
        if (isinstance(val, int)):
            return BinaryExpr(operator.__sub__, LiteralExpr(val), self)
        elif (isinstance(val, Var)):
            return BinaryExpr(operator.__sub__, VarExpr(val), self)
        else:
            return BinaryExpr(operator.__sub__, val, self)

    def __mul__(self, val):
        if (isinstance(val, int)):
            return BinaryExpr(operator.__mul__, self, LiteralExpr(val))
        elif (isinstance(val, Var)):
            return BinaryExpr(operator.__mul__, self, VarExpr(val))
        else:
            return BinaryExpr(operator.__mul__, self, val)

    def __rmul__(self, val):
        if (isinstance(val, int)):
            return BinaryExpr(operator.__mul__, LiteralExpr(val), self)
        elif (isinstance(val, Var)):
            return BinaryExpr(operator.__mul__, VarExpr(val), self)
        else:
            return BinaryExpr(operator.__mul__, val, self);

    def __div__(self, val):
        if (isinstance(val, int)):
            return BinaryExpr(operator.__div__, self, LiteralExpr(val))
        elif (isinstance(val, Var)):
            return BinaryExpr(operator.__div__, self, VarExpr(val))
        else:
            return BinaryExpr(operator.__div__, self, val)

    def __rdiv__(self, val):
        if (isinstance(val, int)):
            return BinaryExpr(operator.__div__, LiteralExpr(val), self)
        elif (isinstance(val, Var)):
            return BinaryExpr(operator.__div__, VarExpr(val), self)
        else:
            return BinaryExpr(operator.__div__, val, self)

    def eval(self, values):
        return self.op(self.lhs.eval(values), self.rhs.eval(values));

    def desc(self):
        return "BinaryExpr(" + self.op.__name__ + "," + self.lhs.desc() + "," + self.rhs.desc() + ")"

    def string(self):
        res = "";
        if (isinstance(self.lhs, BinaryExpr) and
                (opToPrecedence(self.lhs.op) < opToPrecedence(self.op))):
            res += "(" + self.lhs.string() + ")"
        else:
            res += self.lhs.string()
        res += opToSign(self.op)
        if (isinstance(self.rhs, BinaryExpr) and
                (opToPrecedence(self.rhs.op) <= opToPrecedence(self.op))):
            res += "(" + self.rhs.string() + ")"
        else:
            res += self.rhs.string()
        return res

    def derv(self, val):
        if (isinstance(val, int)): #the case of dy/d3
            print "Don't take derivatives with respect to integers."
            return -1
        elif (isinstance(val, Var)): #the case of dy/dx
            if (self.op == operator.__add__ or self.op == operator.__sub__):
                return BinaryExpr(self.op, self.lhs.derv(val), self.rhs.derv(val))
            if (self.op == operator.__mul__):
                return BinaryExpr(operator.__add__, BinaryExpr(self.op, self.rhs.derv(val), self.lhs),
                                  BinaryExpr(self.op, self.lhs.derv(val), self.rhs))
            if (self.op == operator.__div__):
                return BinaryExpr(self.op, BinaryExpr(operator.__add__,
                                                      BinaryExpr(operator.__mul__, self.rhs.derv(val), self.lhs),
                                                      BinaryExpr(operator.__mul__, self.lhs.derv(val), self.rhs)),
                                  BinaryExpr(operator.__mul__, self.rhs, self.rhs))
        else:  # the case that val is not just x or y but is composite like xy (dy/d(xt))
            print "We are not responsible of partial derivatives in this implementation"
            return -1


class Var:
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def __add__(self, val):
        if (isinstance(val, int)):
            return BinaryExpr(operator.__add__, VarExpr(self), LiteralExpr(val))
        elif (isinstance(val, Var)):
            return BinaryExpr(operator.__add__, VarExpr(self), VarExpr(val))
        else:
            return BinaryExpr(operator.__add__, VarExpr(self), val)

    def __radd__(self, val):
        if (isinstance(val, int)):
            return BinaryExpr(operator.__add__, LiteralExpr(val), VarExpr(self))
        elif (isinstance(val, Var)):
            return BinaryExpr(operator.__add__, VarExpr(val), VarExpr(self))
        else:
            return BinaryExpr(operator.__add__, val, VarExpr(self))

    def __mul__(self, val):
        if (isinstance(val, int)):
            return BinaryExpr(operator.__mul__, VarExpr(self), LiteralExpr(val))
        elif (isinstance(val, Var)):
            return BinaryExpr(operator.__mul__, VarExpr(self), VarExpr(val))
        else:
            return BinaryExpr(operator.__mul__, VarExpr(self), val)

    def __rmul__(self, val):
        if (isinstance(val, int)):
            return BinaryExpr(operator.__mul__, LiteralExpr(val), VarExpr(self))
        elif (isinstance(val, Var)):
            return BinaryExpr(operator.__mul__, VarExpr(val), VarExpr(self))
        else:
            return BinaryExpr(operator.__mul__, val, VarExpr(self))

    def __sub__(self, val):
        if (isinstance(val, int)):
            return BinaryExpr(operator.__sub__, VarExpr(self), LiteralExpr(val))
        elif (isinstance(val, Var)):
            return BinaryExpr(operator.__sub__, VarExpr(self), VarExpr(val))
        else:
            return BinaryExpr(operator.__sub__, VarExpr(self), val)

    def __rsub__(self, val):
        if (isinstance(val, int)):
            return BinaryExpr(operator.__rsub__, VarExpr(self), LiteralExpr(val))
        elif (isinstance(val, Var)):
            return BinaryExpr(operator.__rsub__, VarExpr(self), VarExpr(val))
        else:
            return BinaryExpr(operator.__rsub__, VarExpr(self), val)

    def __div__(self, val):
        if (isinstance(val, int)):
            return BinaryExpr(operator.__div__, VarExpr(self), LiteralExpr(val))
        elif (isinstance(val, Var)):
            return BinaryExpr(operator.__div__, VarExpr(self), VarExpr(val))
        else:
            return BinaryExpr(operator.__div__, VarExpr(self), val)

    def __rdiv__(self, val):
        if (isinstance(val, int)):
            return BinaryExpr(operator.__rdiv__, VarExpr(self), LiteralExpr(val))
        elif (isinstance(val, Var)):
            return BinaryExpr(operator.__rdiv__, VarExpr(self), VarExpr(val))
        else:
            return BinaryExpr(operator.__rdiv__, VarExpr(self), val)

    def eval(self, values):
        return values[self.name]

    def desc(self):
        return "Var(" + self.name + ")"

    def string(self):
        return self.name

    def derv(self, val):
        if ( self.name == val.getName() ):
            return LiteralExpr(1)
        else:
            return LiteralExpr(0)


if __name__ == '__main__':
    main()