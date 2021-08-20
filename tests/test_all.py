import assertize


def test_assertequal():
    src = """self.assertEqual(a, b)"""
    res = assertize.rewrite_module(src)
    assert res == "assert a == b"


def test_assertequal_with_message():
    src = """self.assertEqual(a, b, msg)"""
    res = assertize.rewrite_module(src)
    assert res == "assert a == b, msg"


def test_assertnotequal():
    src = """self.assertNotEqual(a, b)"""
    res = assertize.rewrite_module(src)
    assert res == "assert a != b"


def test_assertnotequal_with_message():
    src = """self.assertNotEqual(a, b, msg)"""
    res = assertize.rewrite_module(src)
    assert res == "assert a != b, msg"


def test_asserttrue():
    src = """self.assertTrue(xxx)"""
    res = assertize.rewrite_module(src)
    assert res == "assert xxx"


def test_asserttrue_with_message():
    src = """self.assertTrue(xxx, msg)"""
    res = assertize.rewrite_module(src)
    assert res == "assert xxx, msg"


def test_assertisnone():
    src = """self.assertIsNone(xxx)"""
    res = assertize.rewrite_module(src)
    assert res == "assert xxx is None"


def test_assertisnone_with_message():
    src = """self.assertIsNone(xxx, msg)"""
    res = assertize.rewrite_module(src)
    assert res == "assert xxx is None, msg"


def test_assertisnotnone_with_message():
    src = """self.assertIsNotNone(xxx, msg)"""
    res = assertize.rewrite_module(src)
    assert res == "assert xxx is not None, msg"
