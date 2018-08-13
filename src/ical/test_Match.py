from .match import Match
import pytest

class TestMatch:
########################################################################################### H O M E
    @pytest.fixture(scope='class')
    def match_at_home(self) -> Match:
        return Match("FALLSA", "FALLSA", "Falls A", 6, "OLDLA", "Old Bleach A", 1, "2018-06-05_18:30", "location", "", 3)

    def test_at_home_description(self, match_at_home):
        assert(match_at_home.description() == "Falls A (6) v (1) Old Bleach A on 2018-06-05@18:30")

    def test_at_home_print_description(self, match_at_home):
        assert(match_at_home.print_description() == "Falls A         (  6) v (  1) Old Bleach A    on 2018-06-05@18:30 FALLSA-2018-06-05-18-30-OLDLA@mc-williams.co.uk")

    def test_at_home_id(self, match_at_home):
        assert(match_at_home.id() == "FALLSA-2018-06-05-18-30-OLDLA@mc-williams.co.uk")

########################################################################################### H O M E
    @pytest.fixture(scope='class')
    def match_at_home_newdate(self) -> Match:
        return Match("FALLSA", "FALLSA", "Falls A", 6, "OLDLA", "Old Bleach A", 1, "2018-06-05_18:30", "location", "", 3, new_date="2018-06-06_14:00")

    def test_at_home_newdate_description(self, match_at_home_newdate):
        assert(match_at_home_newdate.description() == "Falls A (6) v (1) Old Bleach A on 2018-06-06@14:00")

    def test_at_home_newdate_print_description(self, match_at_home_newdate):
        assert(match_at_home_newdate.print_description() == "Falls A         (  6) v (  1) Old Bleach A    on 2018-06-06@14:00 FALLSA-2018-06-05-18-30-OLDLA@mc-williams.co.uk")

    def test_at_home_newdate_id(self, match_at_home_newdate):
        assert(match_at_home_newdate.id() == "FALLSA-2018-06-05-18-30-OLDLA@mc-williams.co.uk")

########################################################################################### A W A Y
    @pytest.fixture(scope='class')
    def match_at_away(self) -> Match:
        return Match("FALLSA", "DUNBA", "Dunbarton", 7, "FALLSA", "Falls A", 0, "2018-05-29_14:00", "location", "", 3)

    def test_at_away_description(self, match_at_away):
        assert(match_at_away.description() == "Dunbarton (7) v (0) Falls A on 2018-05-29@14:00")

    def test_at_away_id(self, match_at_away):
        assert(match_at_away.id() == "FALLSA-2018-05-29-14-00-DUNBA@mc-williams.co.uk")

    def test_at_away_print_description(self, match_at_away):
        assert(match_at_away.print_description() == "Dunbarton       (  7) v (  0) Falls A         on 2018-05-29@14:00 FALLSA-2018-05-29-14-00-DUNBA@mc-williams.co.uk")

########################################################################################### C U P
    @pytest.fixture(scope='class')
    def cup_match_at_home(self) -> Match:
        return Match("FALLSA", "FALLSA", "Falls A", 96, "Limavady", "Limavady", 71, "2018-06-02_14:00", "location", "****", 3, "Irish Cup")

    def test_cup_at_home_description(self, cup_match_at_home):
        assert(cup_match_at_home.description() == "Falls A (96) v (71) Limavady on 2018-06-02@14:00 Irish Cup")

    def test_cup_at_home_print_description(self, cup_match_at_home):
        assert(cup_match_at_home.print_description() == "Falls A         ( 96) v ( 71) Limavady        on 2018-06-02@14:00 FALLSA-2018-06-02-14-00-Limavady@mc-williams.co.uk Irish Cup ****")
