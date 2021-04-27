"""
Created on Mar 7, 2014

@author: Stephen Theodore
"""
import mGui.styles as styles
import unittest


class MockCtrl(object):
    def __init__(self, key, **kwargs):
        self.key = key


class MockButton(MockCtrl):
    pass


class MockRedButton(MockButton):
    pass


class MockList(MockCtrl):
    pass


class StyledMockCtrl(styles.Styled, MockCtrl):
    def __init__(self, key=None, **kwargs):
        self.key = key
        super(StyledMockCtrl, self).__init__(kwargs)


class StyledMockButton(StyledMockCtrl):
    pass


class StyledMockRedButton(StyledMockButton):
    pass


class StyledMockList(StyledMockCtrl):
    pass


class Test_CSS(unittest.TestCase):
    def test_css_params(self):
        example = styles.CSS(object().__class__, width=10, height=10)
        assert example["width"] == 10
        assert example["height"] == 10

    def test_css_derive_unique(self):
        p = styles.CSS("outer", width=10, height=10)
        c = styles.CSS("inner", p, color="red", height=3)
        assert c["color"] == "red"

    def test_css_derive_inherit(self):
        p = styles.CSS("outer", width=10, height=10)
        c = styles.CSS("inner", p, color="red", height=3)
        assert c["width"] == p["width"]

    def test_css_derive_override(self):
        p = styles.CSS("outer", width=10, height=10)
        c = styles.CSS("inner", p, color="red", height=3)
        assert c["height"] == 3

    def test_css_nesting(self):
        with styles.CSS("outer", width=100, height=100) as outer:
            with styles.CSS("inner", bgc=(1, 0, 0), size=3) as inner:
                q = styles.CSS("innermost", size=4)
            z = styles.CSS("2dlevel", q, bgc=(2, 0, 0))
        assert inner in outer.children
        assert q in inner.children
        assert z in outer.children

    def test_css_nesting_values(self):
        with styles.CSS("outer", width=100, height=100) as outer:
            with styles.CSS("inner", bgc=(1, 0, 0), size=3) as inner:
                q = styles.CSS("innermost", size=4)
        assert q["width"] == outer["width"]
        assert q["bgc"] == inner["bgc"]
        assert q["size"] == 4

    def test_css_nesting_and_manual_values(self):
        with styles.CSS("outer", width=100, height=100) as outer:
            with styles.CSS("inner", bgc=(1, 0, 0), size=3) as inner:
                q = styles.CSS("innermost", size=4)
            z = styles.CSS("upper", q, bgc=(2, 0, 0))
        assert z["bgc"] == (2, 0, 0)

    def test_css_inherit_order(self):
        a = styles.CSS("a", color="red", margin=1)
        b = styles.CSS("b", color="blue", width=128, float="left")
        c = styles.CSS("c", color="green", width=256)
        d = styles.CSS("test", a, b, c)
        assert d["color"] == "green"
        assert d["width"] == 256
        assert d["float"] == "left"
        assert d["margin"] == 1

        e = styles.CSS("test", c, a, b)
        assert e["color"] == "blue"
        assert e["width"] == 128

    def test_style_applies_on_class(self):
        example = MockCtrl("hello")
        style = styles.CSS(MockCtrl, found=1)
        assert style.applies(example)

    def test_style_applies_on_name(self):
        example = MockCtrl("hello")
        style = styles.CSS("hello", found=1)
        assert style.applies(example)

    def test_style_finds_lowest_in_hierarchy(self):
        """
        note as written, this privileges POSITION hierarchy over CLASS hierarchy... is that bad?
        """
        with styles.CSS(MockCtrl, name="outer") as outer:
            with styles.CSS(MockButton, name="middle"):
                styles.CSS(MockRedButton, name="inner")

        test = MockRedButton("mrb")
        assert outer.find(test)["name"] == "inner"

    def test_style_finds_lowest_in_hierarchy_despite_class_hierarchy(self):
        """
        see docs. Style hierarchy position matters, not class hieratchy!
        """
        with styles.CSS(MockCtrl, name="outer") as outer:
            with styles.CSS(MockRedButton, name="middle"):
                styles.CSS(MockButton, name="inner")

        test = MockRedButton("mrb")
        assert outer.find(test)["name"] == "inner"

    def test_CSS_as_style_context(self):
        with styles.CSS(StyledMockCtrl, width=100, height=100, expected=False) as outer:
            with styles.CSS(StyledMockButton, bgc=(1, 0, 0), size=3, expected=None):
                deepest = styles.CSS(StyledMockRedButton, size=4, expected=True)

        with outer:
            test = StyledMockRedButton(key="fred")  # should find 'deepest'
            test2 = StyledMockList(key="barney")  # defaults to outer

        assert test._style == deepest
        assert test2._style == outer


if __name__ == "__main__":
    unittest.main()
