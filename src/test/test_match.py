from ical.Match import Match
import pytest

class TestMatch:

    @pytest.fixture(scope='class')
    def match(self) -> Match:
        return Match("me", "home", 1, "away", 0, "2018-06-19_14:00", "location", 3)

    def test_description(self, match):
#        match = Match("me", "home", 1, "away", 0, "2018-06-19_14:00", "location", 3)
        assert(match.description() == "home (1) v (0) away on 2018-06-19@14:00")

#if __name__ == '__main__':
#    unittest.main()
