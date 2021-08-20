#!/usr/bin/env python

import sys
from typing import Callable, List, Tuple

import libcst as cst
import libcst.matchers as m


class TestTransformer(m.MatcherDecoratableTransformer):
    def leave_Call(
        self, original_node: cst.Call, updated_node: cst.BaseExpression
    ) -> cst.BaseExpression:

        call = original_node
        args = call.args

        matchers: List[Tuple[m.Call, int, Callable]] = [
            # assertEqual
            (
                m.Call(
                    func=m.Attribute(value=m.Name("self"), attr=m.Name("assertEqual"))
                ),
                2,
                lambda: cst.Assert(
                    cst.Comparison(
                        args[0].value,
                        [cst.ComparisonTarget(cst.Equal(), args[1].value)],
                    )
                ),
            ),
            (
                m.Call(
                    func=m.Attribute(value=m.Name("self"), attr=m.Name("assertEqual"))
                ),
                3,
                lambda: cst.Assert(
                    cst.Comparison(
                        args[0].value,
                        [cst.ComparisonTarget(cst.Equal(), args[1].value)],
                    ),
                    args[2].value,
                ),
            ),
            # assertNotEqual
            (
                m.Call(
                    func=m.Attribute(
                        value=m.Name("self"), attr=m.Name("assertNotEqual")
                    )
                ),
                2,
                lambda: cst.Assert(
                    cst.Comparison(
                        args[0].value,
                        [cst.ComparisonTarget(cst.NotEqual(), args[1].value)],
                    )
                ),
            ),
            (
                m.Call(
                    func=m.Attribute(
                        value=m.Name("self"), attr=m.Name("assertNotEqual")
                    )
                ),
                3,
                lambda: cst.Assert(
                    cst.Comparison(
                        args[0].value,
                        [cst.ComparisonTarget(cst.NotEqual(), args[1].value)],
                    ),
                    args[2].value,
                ),
            ),
            # assertTrue
            (
                m.Call(
                    func=m.Attribute(value=m.Name("self"), attr=m.Name("assertTrue"))
                ),
                1,
                lambda: cst.Assert(args[0].value),
            ),
            (
                m.Call(
                    func=m.Attribute(value=m.Name("self"), attr=m.Name("assertTrue"))
                ),
                2,
                lambda: cst.Assert(args[0].value, args[1].value),
            ),
            # assertIsNone
            (
                m.Call(
                    func=m.Attribute(value=m.Name("self"), attr=m.Name("assertIsNone"))
                ),
                1,
                lambda: cst.Assert(
                    cst.Comparison(
                        args[0].value,
                        [cst.ComparisonTarget(cst.Is(), cst.Name("None"))],
                    )
                ),
            ),
            (
                m.Call(
                    func=m.Attribute(value=m.Name("self"), attr=m.Name("assertIsNone"))
                ),
                2,
                lambda: cst.Assert(
                    cst.Comparison(
                        args[0].value,
                        [cst.ComparisonTarget(cst.Is(), cst.Name("None"))],
                    ),
                    args[1].value,
                ),
            ),
            # assertIsNotNone
            (
                m.Call(
                    func=m.Attribute(
                        value=m.Name("self"), attr=m.Name("assertIsNotNone")
                    )
                ),
                1,
                lambda: cst.Assert(
                    cst.Comparison(
                        args[0].value,
                        [
                            cst.ComparisonTarget(
                                cst.Is(), cst.parse_expression("not None")
                            )
                        ],
                    )
                ),
            ),
            (
                m.Call(
                    func=m.Attribute(
                        value=m.Name("self"), attr=m.Name("assertIsNotNone")
                    )
                ),
                2,
                lambda: cst.Assert(
                    cst.Comparison(
                        args[0].value,
                        [
                            cst.ComparisonTarget(
                                cst.Is(), cst.parse_expression("not None")
                            )
                        ],
                    ),
                    args[1].value,
                ),
            ),
        ]

        for matcher, arity, replacement in matchers:
            if m.matches(call, matcher):
                if len(args) == arity:
                    return replacement()

        return updated_node


def rewrite_module(code: str) -> str:
    tree = cst.parse_module(code)

    transformer = TestTransformer()
    modified_tree = tree.visit(transformer)

    return modified_tree.code


def main():
    for filename in sys.argv[1:]:
        print(filename)
        with open(filename) as fd:
            old_code = fd.read()
            new_code = rewrite_module(old_code)

        with open(filename, "w") as fd:
            fd.write(new_code)


if __name__ == "__main__":
    main()
