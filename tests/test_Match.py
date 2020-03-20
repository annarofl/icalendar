from .context import Match
from .context import TeamData

# from ical.match import Match
import pytest
from .test_utils import fallsa_test_data
from ical.teamdata import instance_load


class TestMatch:
    ###########################################################################
    #  H O M E
    ###########################################################################
    @pytest.fixture(scope="class")
    def home_match(self) -> Match:
        instance_load(fallsa_test_data())
        return Match(
            home_team_id="FALLSA",
            home_score=6,
            away_team_id="OLDLA",
            away_score=1,
            date="2018-06-05",
            time="18:30",
            duration=3,
        )

    def test_home_match_won_description(self, home_match):
        assert (
            home_match.description()
            == "W Falls A (6) v (1) Old Bleach A 2018-06-05@18:30"
        )
        assert (
            home_match.print_description()
            == "W Falls A         (  6) v (  1) Old Bleach A    "
            "2018-06-05@18:30"
        )

    def test_home_match_location(self, home_match):
        assert (home_match.location == "FallsA location")

    def test_home_match_ical_id(self, home_match):
        assert home_match.id() == "FALLSA-2018-06-05-OLDLA@mc-williams.co.uk"

    ###########################################################################
    #  H O M E   A W A Y   N O T   K N O W N
    ###########################################################################
    @pytest.fixture(scope="class")
    def home_awaynotknown(self) -> Match:
        instance_load(fallsa_test_data())
        return Match(
            home_team_id="FALLSA",
            home_score=6,
            away_team_id="OLDXX",
            away_score=1,
            date="2018-06-05",
            time="18:30",
            duration=3,
        )

    def test_home_awaynotknown_won_description(self, home_awaynotknown):
        assert (
            home_awaynotknown.print_description()
            == "W Falls A         (  6) v (  1) OLDXX           "
            "2018-06-05@18:30 ****"
        )

    def test_home_awaynotknown_location(self, home_awaynotknown):
        assert (home_awaynotknown.location == "FallsA location")

    ###########################################################################
    #  A W A Y   H O M E   N O T   K N O W N
    ###########################################################################
    @pytest.fixture(scope="class")
    def away_homenotknown(self) -> Match:
        instance_load(fallsa_test_data())
        return Match(
            home_team_id="OLDXX",
            home_score=6,
            away_team_id="FALLSA",
            away_score=1,
            date="2018-06-05",
            time="18:30",
            duration=3,
        )

    def test_away_homenotknown_won_description(self, away_homenotknown):
        assert (
            away_homenotknown.print_description()
            == "L OLDXX           (  6) v (  1) Falls A         "
            "2018-06-05@18:30 ****"
        )

    def test_away_homenotknown_location(self, away_homenotknown):
        assert (away_homenotknown.location == "OLDXX")

    ###########################################################################
    #  A W A Y   W I T H   L O C A T I O N    H O M E   N O T   K N O W N
    ###########################################################################
    @pytest.fixture(scope="class")
    def away_loc_homenotknown(self) -> Match:
        instance_load(fallsa_test_data())
        return Match(
            home_team_id="OLDXX",
            home_score=6,
            away_team_id="FALLSA",
            away_score=1,
            date="2018-06-05",
            time="18:30",
            duration=3,
            location="Where OLDXX play",
        )

    def test_away_loc_homenotknown_won_description(self, away_loc_homenotknown):
        assert (
            away_loc_homenotknown.print_description()
            == "L OLDXX           (  6) v (  1) Falls A         "
            "2018-06-05@18:30 ****"
        )

    def test_away_loc_homenotknown_location(self, away_loc_homenotknown):
        assert (away_loc_homenotknown.location == "Where OLDXX play")

    ###########################################################################
    # H O M E   N E W   D A T E
    ###########################################################################
    @pytest.fixture(scope="class")
    def home_match_newdate(self) -> Match:
        instance_load(fallsa_test_data())
        return Match(
            home_team_id="FALLSA",
            home_score=6,
            away_team_id="OLDLA",
            away_score=1,
            date="2018-06-05",
            time="18:30",
            duration=3,
            new_date="2018-06-06",
        )

    def test_home_match_newdate_won_description(self, home_match_newdate):
        assert (
            home_match_newdate.description()
            == "W Falls A (6) v (1) Old Bleach A 2018-06-06@18:30"
        )
        assert (
            home_match_newdate.print_description()
            == "W Falls A         (  6) v (  1) Old Bleach A    "
            "2018-06-06@18:30"
        )

    def test_home_match_newdate_ical_id(self, home_match_newdate):
        assert home_match_newdate.id() == 'FALLSA-2018-06-05-OLDLA@' \
            'mc-williams.co.uk'

    ###########################################################################
    # H O M E   N E W   D A T E   A N D   T I M E
    ###########################################################################
    @pytest.fixture(scope="class")
    def home_newdatetime(self) -> Match:
        instance_load(fallsa_test_data())
        return Match(
            home_team_id="FALLSA",
            home_score=6,
            away_team_id="OLDLA",
            away_score=1,
            date="2018-06-05",
            time="18:30",
            duration=3,
            new_date="2018-06-06",
            new_time="14:00",
        )

    def test_home_newdatetime_description(self, home_newdatetime):
        assert (
            home_newdatetime.description()
            == "W Falls A (6) v (1) Old Bleach A 2018-06-06@14:00"
        )
        assert (
            home_newdatetime.print_description()
            == "W Falls A         (  6) v (  1) Old Bleach A    "
            "2018-06-06@14:00"
        )

    def test_home_match_newdatetime_ical_id(self, home_newdatetime):
        assert home_newdatetime.id() == "FALLSA-2018-06-05-OLDLA@" \
            "mc-williams.co.uk"

    ###########################################################################
    # H O M E   N E W   D A T E   N O T   K N O W N
    ###########################################################################
    @pytest.fixture(scope="class")
    def home_newdateunknwon(self) -> Match:
        instance_load(fallsa_test_data())
        return Match(
            home_team_id="FALLSA",
            home_score=6,
            away_team_id="OLDLA",
            away_score=1,
            date="2018-06-05",
            time="18:30",
            duration=3,
            new_date="",
        )

    def test_home_newdateunknwon_description(self, home_newdateunknwon):
        assert (
            home_newdateunknwon.description()
            == "W Falls A (6) v (1) Old Bleach A 2018-06-05@18:30 "
            "****-TBD-****"
        )

    def test_home_newdateunknwon_print_description(self, home_newdateunknwon):
        assert (
            home_newdateunknwon.print_description()
            == "W Falls A         (  6) v (  1) Old Bleach A    "
            "2018-06-05@18:30 ****-TBD-****"
        )

    def test_home_newdateunknwon_id(self, home_newdateunknwon):
        assert home_newdateunknwon.id() == "FALLSA-2018-06-05-OLDLA@" \
            "mc-williams.co.uk"

    ###########################################################################
    #  A W A Y
    ###########################################################################
    @pytest.fixture(scope="class")
    def away_match(self) -> Match:
        instance_load(fallsa_test_data())
        return Match(
            home_team_id="DUNBA",
            home_score=7,
            away_team_id="FALLSA",
            away_score=0,
            date="2018-05-29",
            time="14:00",
            duration=3,
        )

    def test_at_away_description(self, away_match):
        assert (
            away_match.description()
            == "L Dunbarton (7) v (0) Falls A 2018-05-29@14:00"
        )

    def test_at_away_id(self, away_match):
        assert away_match.id() == "FALLSA-2018-05-29-DUNBA@mc-williams.co.uk"

    def test_at_away_print_description(self, away_match):
        assert (
            away_match.print_description()
            == "L Dunbarton       (  7) v (  0) Falls A         "
            "2018-05-29@14:00"
        )

    def test_away_location(self, away_match):
        assert (away_match.location == "DUNBA location")

    ###########################################################################
    #  C U P   H O M E
    ###########################################################################
    @pytest.fixture(scope="class")
    def cup_home_match(self) -> Match:
        instance_load(fallsa_test_data())
        return Match(
            home_team_id="FALLSA",
            home_score=96,
            away_team_id="Limavady",
            away_score=71,
            date="2018-06-02",
            time="14:00",
            location="location",
            duration=3,
            label="Irish Cup",
        )

    def test_cup_home_match_description(self, cup_home_match):
        assert (
            cup_home_match.description()
            == "W Falls A (96) v (71) Limavady 2018-06-02@14:00 Irish Cup ****"
        )

    def test_cup_home_match_print_description(self, cup_home_match):
        assert (
            cup_home_match.print_description()
            == "W Falls A         ( 96) v ( 71) Limavady        "
            "2018-06-02@14:00 Irish Cup ****"
        )

    ###########################################################################
    #  C U P   A W A y
    ###########################################################################
    @pytest.fixture(scope="class")
    def cup_away_match(self) -> Match:
        instance_load(fallsa_test_data())
        return Match(
            home_team_id="Limavady",
            home_score=96,
            away_team_id="FALLSA",
            away_score=71,
            date="2018-06-02",
            time="14:00",
            location="Limavady loc",
            duration=3,
            label="Irish Cup",
        )

    def test_cup_away_match_description(self, cup_away_match):
        assert (
            cup_away_match.description()
            == "L Limavady (96) v (71) Falls A 2018-06-02@14:00 Irish Cup ****"
        )

    def test_cup_away_match_location(self, cup_away_match):
        assert (cup_away_match.location == "Limavady loc")

    ###########################################################################
    #  N O T   Y E T   P L A Y E D
    ###########################################################################
    @pytest.fixture(scope="class")
    def notyet_home_match(self) -> Match:
        instance_load(fallsa_test_data())
        return Match(
            home_team_id="FALLSA",
            home_score=0,
            away_team_id="Limavady",
            away_score=0,
            date="2018-06-02",
            time="14:00",
            location="location",
            duration=3
        )

    def test_description_starts_with_dot(self, notyet_home_match):
        assert (
            notyet_home_match.description()
            == ". Falls A (0) v (0) Limavady 2018-06-02@14:00 ****"
        )
        assert (
            notyet_home_match.print_description()
            == ". Falls A         (  0) v (  0) Limavady        "
            "2018-06-02@14:00 ****"
        )
