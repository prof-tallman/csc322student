

def is_leap_year(year):
    year = int(year)
    if year < 0:
        raise ValueError(f"Negative years not allowed, this calendar uses " +\
                         f"years from A.D. 1 onwards (year={year})")
    elif year == 0:
        raise ValueError(f"Year 0 does not exist, the calendar goes " +\
                         f"from B.C. 1 to A.D. 1 (year={year})")
    elif year < 1582:
        raise ValueError(f"Julius Caesar decreed a type of leap year " +\
                         f"in 45 B.C. but the modern leap year system " +\
                         f"started in 1582 with a 10-day leap year to " +\
                         f"get things back on track (year={year})")
    
    elif year == 1582:
        raise ValueError(f"The modern leap year system started in 1582 " +\
                         f"with a 10-day leap year to synchronize the " +\
                         f"Gregorian calendar (year={year})")
    
    else:
        return year % 4 == 0 and year % 100 != 0 or year % 400 == 0
    

if __name__ == '__main__':
    from datetime import date
    current_year = date.today().year
    test_year1 = current_year - 2
    test_year2 = current_year - 1
    test_year3 = current_year
    test_year4 = current_year + 1
    test_year5 = current_year + 2
    print(f"{test_year1} is a leap year: {is_leap_year(test_year1)}")
    print(f"{test_year2} is a leap year: {is_leap_year(test_year2)}")
    print(f"{test_year3} is a leap year: {is_leap_year(test_year3)}")
    print(f"{test_year4} is a leap year: {is_leap_year(test_year4)}")
    print(f"{test_year5} is a leap year: {is_leap_year(test_year5)}")
