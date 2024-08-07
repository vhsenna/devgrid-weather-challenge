from src.utils.cities import CITIES_ID


def test_cities_id_not_empty():
    assert len(CITIES_ID) > 0, "CITIES_ID list should not be empty."


def test_cities_id_are_integers():
    assert all(isinstance(city_id, int)
               for city_id in CITIES_ID), "All city IDs should be integers."


def test_cities_id_unique():
    assert len(CITIES_ID) == len(set(CITIES_ID)
                                 ), "CITIES_ID list should contain unique IDs."


def test_cities_id_length():
    expected_length = 167
    assert len(
        CITIES_ID) == expected_length, f"CITIES_ID list should contain {expected_length} IDs."
