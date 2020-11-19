"""Utilities related to Quil based symbolic expressions."""
from functools import singledispatch
import operator
from numbers import Number
import pyquil
from pyquil import quilatom
from .expressions import ExpressionDialect


@singledispatch
def expression_from_pyquil(expression):
    raise NotImplementedError(
        f"Expression {expression} of type {type(expression)} is currently not supported"
    )


@expression_from_pyquil.register
def identity(number: Number):
    return number


# Dialect defining conversion of intermediate expression tree to
# the expression based on quil functions/parameters.
# This is intended to be passed by a `dialect` argument of `translate_expression`.
QUIL_DIALECT = ExpressionDialect(
    symbol_factory=lambda symbol: pyquil.quil.Parameter(symbol.name),
    number_factory=lambda number: number,
    known_functions={
        "add": operator.add,
        "mul": operator.mul,
        "div": operator.truediv,
        "sub": operator.sub,
        "pow": operator.pow,
        "cos": quilatom.quil_cos,
        "sin": quilatom.quil_sin,
        "exp": quilatom.quil_exp,
        "sqrt": quilatom.quil_sqrt,
        "tan": lambda arg: quilatom.quil_sin(arg) / quilatom.quil_cos(arg),
    },
)
