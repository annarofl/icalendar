from .match import Match
import pytest

class TestMatch:
###########################################################################################
#  H O M E
###########################################################################################
    @pytest.fixture(scope='class')
    def home_match(self) -> Match:
        return Match("FALLSA", "FALLSA", "Falls A", 6, "OLDLA", "Old Bleach A", 1, "2018-06-05_18:30", "location", "", 3)

    def test_home_match_description(self, home_match):
        assert(home_match.description() == "Falls A (6) v (1) Old Bleach A on 2018-06-05@18:30")

    def test_home_match_print_description(self, home_match):
        assert(home_match.print_description() == "Falls A         (  6) v (  1) Old Bleach A    on 2018-06-05@18:30 FALLSA-2018-06-05-18-30-OLDLA@mc-williams.co.uk")

    def test_home_match_id(self, home_match):
        assert(home_match.id() == "FALLSA-2018-06-05-18-30-OLDLA@mc-williams.co.uk")

###########################################################################################
# H O M E   N E W   D A T E
###########################################################################################
    @pytest.fixture(scope='class')
    def home_match_newdate(self) -> Match:
        return Match("FALLSA", "FALLSA", "Falls A", 6, "OLDLA", "Old Bleach A", 1, "2018-06-05_18:30", "location", "", 3, new_date="2018-06-06_14:00")

    def test_home_match_newdate_description(self, home_match_newdate):
        assert(home_match_newdate.description() == "Falls A (6) v (1) Old Bleach A on 2018-06-06@14:00")

    def test_home_match_newdate_print_description(self, home_match_newdate):
        assert(home_match_newdate.print_description() == "Falls A         (  6) v (  1) Old Bleach A    on 2018-06-06@14:00 FALLSA-2018-06-05-18-30-OLDLA@mc-williams.co.uk")

    def test_home_match_newdate_id(self, home_match_newdate):
        assert(home_match_newdate.id() == "FALLSA-2018-06-05-18-30-OLDLA@mc-williams.co.uk")

###########################################################################################
#  A W A Y
###########################################################################################
    @pytest.fixture(scope='class')
    def away_match(self) -> Match:
        return Match("FALLSA", "DUNBA", "Dunbarton", 7, "FALLSA", "Falls A", 0, "2018-05-29_14:00", "location", "", 3)

    def test_at_away_description(self, away_match):
        assert(away_match.description() == "Dunbarton (7) v (0) Falls A on 2018-05-29@14:00")

    def test_at_away_id(self, away_match):
        assert(away_match.id() == "FALLSA-2018-05-29-14-00-DUNBA@mc-williams.co.uk")

    def test_at_away_print_description(self, away_match):
        assert(away_match.print_description() == "Dunbarton       (  7) v (  0) Falls A         on 2018-05-29@14:00 FALLSA-2018-05-29-14-00-DUNBA@mc-williams.co.uk")

###########################################################################################
#  C U P
###########################################################################################
    @pytest.fixture(scope='class')
    def cup_home_match(self) -> Match:
        return Match("FALLSA", "FALLSA", "Falls A", 96, "Limavady", "Limavady", 71, "2018-06-02_14:00", "location", "****", 3, "Irish Cup")

    def test_cup_home_match_description(self, cup_home_match):
        assert(cup_home_match.description() == "Falls A (96) v (71) Limavady on 2018-06-02@14:00 Irish Cup")

    def test_cup_home_match_print_description(self, cup_home_match):
        assert(cup_home_match.print_description() == "Falls A         ( 96) v ( 71) Limavady        on 2018-06-02@14:00 FALLSA-2018-06-02-14-00-Limavady@mc-williams.co.uk Irish Cup ****")
