import assertize


def test_assertequal():
    src = """self.assertEqual(a, b)"""
    res = assertize.rewrite_module(src)
    assert res == "assert a == b"


def test_assertnotequal():
    src = """self.assertNotEqual(a, b)"""
    res = assertize.rewrite_module(src)
    assert res == "assert a != b"


def test_asserttrue():
    src = """self.assertTrue(xxx)"""
    res = assertize.rewrite_module(src)
    assert res == "assert xxx"


def test_assertisnone():
    src = """self.assertIsNone(xxx)"""
    res = assertize.rewrite_module(src)
    assert res == "assert xxx is None"


def test_assertisnotnone():
    src = """self.assertIsNotNone(xxx)"""
    res = assertize.rewrite_module(src)
    assert res == "assert xxx is not None"
