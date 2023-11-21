from jams.library import get_available_jams


def test_library():
    availabled_jams = get_available_jams()
    sample_flow_jam = None
    for jam in availabled_jams:
        if jam["name"] == "Sample Flow Jam":
            sample_flow_jam = jam
            break
    assert sample_flow_jam is not None
