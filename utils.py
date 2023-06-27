from exceptions import InvalidYearCupError
from exceptions import NegativeTitlesError
from exceptions import ImpossibleTitlesError
from datetime import datetime

def data_processing (info_teams):
    if info_teams.get("titles") < 0:
        raise NegativeTitlesError("titles cannot be negative")
    
    first_cup = info_teams.get("first_cup")
    first_cup_datetime = datetime.strptime(first_cup, "%Y-%m-%d")
    first_cup_year = int(first_cup_datetime.strftime("%Y"))

    first_cup_ever = int(1930)
    time_now = datetime.now()
    year_now = int(time_now.strftime("%Y"))

    if first_cup_year < first_cup_ever or first_cup_year > year_now:
        raise InvalidYearCupError("there was no world cup this year")
    
    titles_team = int(info_teams.get("titles"))

    if(first_cup_year - first_cup_ever) % 4 != 0:
        raise InvalidYearCupError("there was no world cup this year")
    
    if first_cup_year + (titles_team * 4) > year_now:
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")