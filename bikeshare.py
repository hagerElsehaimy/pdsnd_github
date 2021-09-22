#import required packages

# insert comment for refactoring branch
import time
import pandas as pd
from datetime import datetime, timedelta
from calendar import day_name, month_name
from os import system

CITY_DATA = {'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv'}


def get_city_user_input():
    """
    get User Input for one the city name saved in CITY_DATA
    Returns:
        (str) city name entered by user after validation
    """
    try:
        # get city name from user
        city = input("Enter city name you wanna get statistics about \n{}\n>>>".format(list(CITY_DATA.keys()))).lower()

        # check city existence in the list of cities that we've as keys of CITY_DATA
        while city not in CITY_DATA.keys():
            city = input("Enter a valid input \n{}\n>>>".format(list(CITY_DATA.keys()))).lower()
        return city  # return the first valid city input entered by user

    # handle user input in case user stopped the program or killed the process
    except KeyboardInterrupt as error:
        system('clear')     # clear the terminal and print a simple quit message
        error.message = "****you've quit the program.\nBye!****"
        print(error.message)
        exit(0)  # exit the program properly


def get_month_user_input():
    """
    get User Input for one the month name
       Returns:
           (str) month name entered by user after validation
       """
    # prepare a list contains [All,January,February,...etc]
    month_list = [month_name[month_no] for month_no in range(1, 7)]
    month_list.insert(0, "All")
    try:
        # get user input in titled format to mach month_list elements
        month = input("Enter month name from Jan to Jun or type All to skip filtering\n{}\n>>>".format(month_list))\
            .title()
        month_flag = True

        while month_flag:
            if month in month_list:
                month_flag = False
            else:
                month = input("Enter a valid input\n{}\n>>>".format(month_list)).title()
        return month
        # handle user input in case user stopped the program or killed the process
    except KeyboardInterrupt as error:
        system('clear')  # clear the terminal and print a simple quit message
        error.message = "****you've quit the program.\nBye!****"
        print(error.message)
        exit(0)  # exit the program properly


def get_day_user_input():
    """
    get User Input for one the day name
           Returns:
               (str) day name entered by user after validation
           """
    days_list = list(day_name)
    days_list.insert(0, "All")

    try:
        day_flag = True
        day = input("Enter a valid week day or type all to skip filtering\n{}\n>>>".format(days_list)).title()
        while day_flag:
            if day in days_list:
                day_flag = False
            else:
                day = input("Enter a valid input\n{}\n>>>".format(days_list)).title()
        return day

    except KeyboardInterrupt as error:
        system('clear')
        error.message = "****you've quit the program.\nBye!****"
        print(error.message)
        exit(0)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    It only calls the 3 functions get {cit,month,day} user input.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bike share data!')

    # get user input for city (chicago, new york, washington). HINT: Use a while loop to handle invalid inputs
    city = get_city_user_input()

    # get user input for month (All, January, February, ... , June)
    month = get_month_user_input()

    # get user input for day of week (All, Monday, Tuesday, ... Sunday)
    day = get_day_user_input()

    print('-'*40)

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # read the whole file mapped to entered cit name
    df = pd.read_csv(CITY_DATA[city])

    # Cast Start time into datetime format to extract Months, Days and Hours from
    df['Start Time'] = pd.to_datetime(df['Start Time'], format="%Y-%m-%d %H:%M:%S")

    df['Month'] = df['Start Time'].dt.strftime('%B')

    df['Day'] = df['Start Time'].dt.strftime('%A')

    df['Hour'] = df['Start Time'].dt.strftime('%H')

    df['Stations'] = df['Start Station'] + " " + df['End Station']

    # dataframe preprocessing to replace spaces in coloumn names by _ for easy manipulation
    df.columns = [c.replace(' ', '_') for c in df.columns]

    # filter data frame by month
    if month != "All":
        df = df[df.Month.eq(month)]

    # filter data frame by day
    if day != "All":
        df = df[df.Day.eq(day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month of travel is: {} ".format(df.Month.mode()[0]))

    # display the most common day of week
    print("The most common day of travel is: {} ".format(df.Day.mode()[0]))

    # display the  most common start hour
    print("The most common hour of travel is: {} ".format(df.Hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')

    start_time = time.time()

    # display most commonly used start station
    print("The most common used start station is: {} ".format(df.Start_Station.mode()[0]))

    # display most commonly used end station
    print("The most common used stop station is: {} ".format(df.End_Station.mode()[0]))

    # display most frequent combination of start station and end station trip
    print("The most common used combination of start station and end station are: {} ".format(df.Stations.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time: {} ".format(str(timedelta(seconds=int(df.Trip_Duration.sum())))))

    # display mean travel time
    print("Time average: {} " .format(str(timedelta(seconds=int(df.Trip_Duration.mean())))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Number of Subscribers: {} ".format(df.query('User_Type == "Subscriber"').User_Type.count()))
    print("Number of Customers: {}".format(df.query('User_Type == "Customer"').User_Type.count()))

    # Display counts of gender
    try:
        print("Number of Males: {} ".format(df.query('Gender == "Male"').Gender.count()))
        print("Number of Females: {} ".format(df.query('Gender == "Female"').Gender.count()))

    except Exception as error:
        error.message = "washington doesn't have gender classification\n "
        print(error.message)

    # Display earliest, most recent, and most common year of birth
    try:
        print("The earliest year is: {} ".format(int(df.Birth_Year.min())))
        print("The most recent year is: {} ".format(int(df.Birth_Year.max())))
        print("The most common year is: {} ".format(int(df.Birth_Year.mode()[0])))
    except Exception as error:

        error.message = "washington doesn't have DOB "
        print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """
    Asks if the user would like to see some lines of data from the filtered dataset.
    Displays 5 (show_rows) lines, then asks if they would like to see 5 more.
    Continues asking until they say stop.
    """
    try:
        # start and end counters that holds the bulk should be shown
        start, end = 0, 4

        read_chunks = input(
            "May you want to have a look on more raw data? Type yes to continue or press any button to quit\n >>>") \
            .lower()

        while read_chunks == "yes":
            print(df.loc[start:end, :])
            read_chunks = input(
                "May you want to have a look on more raw data? Type yes to continue or press any button to quit\n >>>")\
                .lower()

            # increment by 5 to show the next 5 rows
            start = end + 1
            end += 5
    except KeyboardInterrupt as error:
        system('clear')
        error.message = "you've quit the program.\nBye!"
        print(error.message)
        exit(0)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
