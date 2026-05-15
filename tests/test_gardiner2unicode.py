import pytest

from gardiner2unicode import GardinerToUnicodeMap


@pytest.fixture(scope="module")
def g2u():
    return GardinerToUnicodeMap()


def test_map_is_non_trivial(g2u):
    assert len(g2u.gardiner2unicode) > 1000


def test_map_is_a_bijection(g2u):
    assert len(g2u.gardiner2unicode) == len(g2u.unicode2gardiner)


def test_a1_forward_lookups(g2u):
    assert g2u.to_unicode_hex("A1") == "00013000"
    assert g2u.to_unicode_int("A1") == 77824
    assert g2u.to_unicode_char("A1") == "𓀀"


def test_a1_reverse_lookups(g2u):
    assert g2u.to_gardiner_from_hex("00013000") == "A1"
    assert g2u.to_gardiner_from_int(77824) == "A1"
    assert g2u.to_gardiner_from_chr("𓀀") == "A1"


def test_reverse_hex_is_case_insensitive(g2u):
    assert g2u.to_gardiner_from_hex("00013000".lower()) == "A1"


def test_unknown_code_returns_none(g2u):
    assert g2u.to_unicode_hex("NOT_A_CODE") is None
    assert g2u.to_unicode_int("NOT_A_CODE") is None
    assert g2u.to_unicode_char("NOT_A_CODE") is None
    assert g2u.to_gardiner_from_hex("FFFFFFFF") is None


def test_full_unicode_block_is_covered(g2u):
    """ Every code point in the Egyptian Hieroglyphs block (U+13000..U+1342E)
        must be present in the parsed map. """
    for uid in range(int("13000", 16), int("1342F", 16)):
        unic = "000" + hex(uid)[2:].upper()
        assert unic in g2u.unicode2gardiner, f"{chr(uid)} ({unic}) missing from the map"


def test_roundtrip_for_all_codes(g2u):
    for code in g2u.gardiner2unicode:
        assert g2u.to_gardiner_from_int(g2u.to_unicode_int(code)) == code


def test_reverse_hex_accepts_hex_code_kwarg(g2u):
    # The keyword was renamed from `hex` to `hex_code` in 1.0.0.
    assert g2u.to_gardiner_from_hex(hex_code="00013000") == "A1"
