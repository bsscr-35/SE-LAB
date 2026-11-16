from hypothesis import given, strategies as st

from processor import process_name, calculate_average, process_age


# Test 1: Fuzz testing process_name()
@given(st.one_of(st.text(), st.none()))
def test_process_name_no_crash(name):
    try:
        process_name(name)
    except Exception as e:
        assert False, f"process_name crashed with input {name!r}: {e}"


# Test 2: Fuzz testing calculate_average()
@given(st.lists(st.integers()))
def test_calculate_average_no_crash(numbers):
    try:
        calculate_average(numbers)
    except Exception as e:
        assert False, f"calculate_average crashed with input {numbers!r}: {e}"


# Test 3: Fuzz testing process_age()
@given(st.one_of(st.text(), st.none()))
def test_process_age_no_crash(age):
    try:
        process_age(age)
    except Exception as e:
        assert False, f"process_age crashed with input {age!r}: {e}"
