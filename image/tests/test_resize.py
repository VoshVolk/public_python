import pytest
import os
import sys
from PIL import Image
from decimal import Decimal, getcontext, FloatOperation, ROUND_HALF_UP

getcontext().traps[FloatOperation] = True
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from resize import (
    adapt_size,
    ref_width,
    ref_height,
    get_size,
    percent,
    round_halfup,
)


def pytest_sessionstart():
    pass

def pytest_sessionfinish():
    pass


@pytest.fixture(scope='session')
def img1() -> Image:
    return Image.new("RGB", (512, 512), (128, 128, 128))

@pytest.fixture(scope='session')
def img2() -> Image:
    return Image.new("RGB", (999, 999), (128, 128, 128))

@pytest.fixture(scope='session')
def img3() -> Image:
    return Image.new("RGB", (1920, 1080), (128, 128, 128))

@pytest.mark.parametrize(('size_opt', 'expected'), [
    ("100x100", (100, 56)),
    ("200x300", (200, 113)),
    ("300x200", (300, 169)),
    ("500x200", (356, 200)),
    ("500x300", (500, 281)),
    ("1000x500", (889, 500)),
    ("500x1000", (500, 281)),
    ("2500x1500", (2500, 1406)),
    ("3000x1500", (2667, 1500)),
    ("500x200>", (356, 200)),
    ("500x300>", (500, 281)),
    ("1000x500>", (889, 500)),
    ("500x1000>", (500, 281)),
    ("2500x1500>", (2500, 1406)),
    ("3000x1500>", (2667, 1500)),
    ("500x200<", (356, 200)),
    ("500x300<", (500, 281)),
    ("1000x500<", (889, 500)),
    ("500x1000<", (500, 281)),
    ("2500x1500<", (2500, 1406)),
    ("3000x1500<", (2667, 1500)),
    ("200x300*", (200, 113)),
    ("200x300****", (200, 113)),
    ("***200x300**", (200, 113)),
    ("**200**x**300***", (200, 113)),
    ("**300**x**200***", (300, 169)),
    ("200x300!", (200, 113)),
    ("10%x10%", (192, 108)),
    ("20%x30%", (384, 216)),
    ("30%x20%", (384, 216)),
    ("100%x100%", (1920, 1080)),
    ("200%x300%", (3840, 2160)),
    ("300%x200%", (3840, 2160)),
    ("10%x10%>", (192, 108)),
    ("20%x30%>", (384, 216)),
    ("30%x20%>", (384, 216)),
    ("100%x100%>", (1920, 1080)),
    ("200%x300%>", (3840, 2160)),
    ("300%x200%>", (3840, 2160)),
    ("10%x10%<", (192, 108)),
    ("20%x30%<", (384, 216)),
    ("30%x20%<", (384, 216)),
    ("33.3333%x33.3333%<", (640, 360)),
    ("100%x100%<", (1920, 1080)),
    ("200%x300%<", (3840, 2160)),
    ("300%x200%<", (3840, 2160)),
    ("200x300%*", (200, 113)),
    ("200x300%****", (200, 113)),
    ("***200x300%**", (200, 113)),
    ("**200**x$$$300%***", (200, 113)),
    ("**300**x**200%***", (300, 169)),
    ("**3000**x**300.5%***", (3000, 1688)),
    ("**200.5%**x**300.5%***", (3850, 2166)),
    ("**400.5%**x**300.5%***", (5769, 3245)),
    ("200x300%!", (200, 113)),
    ("200xx300%!", (200, 113)),
    ("20x0xx300%!", (20, 11)),
    ("200xx30x0%!", (200, 113)),
    # ("abc", (200, 113)),
])
def test_adapt_size(img3, size_opt, expected):
    assert adapt_size(size_opt, img3) == expected

@pytest.mark.parametrize(('w_spec', 'expected'), [
    ("100", (100, 100)),
    ("512", (512, 512)),
    ("1024", (1024, 1024)),
])
def test_ref_width(img1, w_spec, expected):
    assert ref_width(Decimal(w_spec), img1) == expected 

@pytest.mark.parametrize(('h_spec', 'expected'), [
    ("100", (100, 100)),
    ("512", (512, 512)),
    ("1024", (1024, 1024)),
])
def test_ref_height(img1, h_spec, expected):
    assert ref_height(Decimal(h_spec), img1) == expected 

@pytest.mark.parametrize(('size_str', 'source_size', 'expected'), [
    ("100", 100, 100),
    ("512", 512, 512),
    ("1024", 1024, 1024),
    # ("abcd", 1024, 1024),
    ("a;jkgag;lgas10000fsa;ldkg9", 1000, 100009),
    ("a;jkgag;lgas100fsa;ldk%g9", 1000, 1000),
    ("a;jkgag;lgas100fsa;ldk%%g9", 1000, 1000),
    #("a;j%kgag;lgas100fsa;ldk%%g9", 1000, 1000),
])
def test_get_size(size_str, source_size, expected):
    assert get_size(size_str, source_size) == expected 

@pytest.mark.parametrize(('s', 'expected'), [
    ("100", None),
    ("512", None),
    ("1024", None),
    ("a;jkgag;lgas10000fsa;ldkg9", None),
    ("a;jkgag;lgas100fsa;ldk%g9", "a;jkgag;lgas100fsa;ldk"),
    ("a;jkgag;lgas100fsa;ldk%%g9", "a;jkgag;lgas100fsa;ldk"),
    ("a;j%kgag;lgas100fsa;ldk%%g9", "a;j"),
])
def test_percent(s, expected):
    assert percent(s) == expected 

@pytest.mark.parametrize(('num', 'expected'), [
    ("100.001", 100),
    ("512.01", 512),
    ("1024.1", 1024),
    ("1.25346436", 1),
    ("2.3455426", 2),
    ("3.44985345", 3),
    ("4.5453543631", 5),
    ("5.63446", 6),
    ("6.79466", 7),
    ("7.846889", 8),
    ("8.97575332", 9),
    ("9.095967443", 9),
])
def test_percent(num, expected):
    assert round_halfup(Decimal(num)) == expected 



