import time
import pandas as pd
import numpy as np

CITY_DATA = { 'c': 'chicago.csv',
              'n': 'new_york_city.csv',
              'w': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    """ City Filter """
    city = input("""Choose a city by typing the first letter of the city name \n
    (c = Chicago, n = New York City, w = Washington):\n""").lower()
    while city not in ('c', 'n', 'w', 'chicago','new york city', 'washington'):
        city = input("""    That city is not in our list. Please try again.
        Choose a city by typing the first letter of the city name or the full name if you feel like typing ;-)

        (c = Chicago, n = New York City, w = Washington):\n""").lower()

    """ Month Filter """
    month = input('\nWhich month would you like to analyze?\nall, january, february, march, april, may or june?\n').lower()
    while month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
        month = input("""    Sorry, I do not know what you mean. Please try again.
        Which month would you like to analyze?

        type: all, january, february, march, april, may or june:\n""").lower()


    """ Day Filter """
    day = input('\nAnd finally, which day would you like to analyze?\nall, monday, tuesday, wednesday, thursday, friday, saturday or sunday?\n').lower()
    while day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
        day = input("""    Sorry, I do not know what you mean. Please try again.
        Which day would you like to analyze?

        type: all, monday, tuesday, wednesday, thursday, friday, saturday or sunday:\n""").lower()

    print('-'*40)
    return city , month, day


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the days list to get the corresponding int
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day) + 1
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    """ Most common month """
    popular_month = df['month'].mode()[0]
    print('\nMost Frequent month:', popular_month)

    """ Most common day """
    popular_day = df['day_of_week'].mode()[0]
    print('\nMost Frequent day of the week:', popular_day)

    """ Most common hour """
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('\nMost Frequent Start Hour:', popular_hour)

    print('-'*40)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    """ Most popular Start point """
    popular_start_station = df['Start Station'].mode()[0]
    print('\nMost popular start station:', popular_start_station)

    """ Most popular End point """
    popular_end_station = df['End Station'].mode()[0]
    print('\nMost popular end station:', popular_end_station)

    """ Most popular Trip """
    df['Trip'] = df['Start Station'] +' to '+ df['End Station']
    popular_trip = df['Trip'].mode()[0]
    print('\nMost popular trip:', popular_trip)

    print('-'*40)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    """ Total travel time """
    trip_time_sec = df['Trip Duration'].sum()

    """ Calc trip time from seconds to hours, minutes and seconds """
    hours = int(trip_time_sec/3600)
    minutes = int((trip_time_sec - (hours*3600))/60)
    seconds = int((trip_time_sec - (hours * 3600) - (minutes * 60)))
    message = "\nTotal trip time over this period is {} hours, {} minutes and {} seconds."
    print(message.format(hours, minutes, seconds))

    """ Average travel time """
    avg_time_sec = df['Trip Duration'].mean()

    """ Calc average trip time from seconds to hours, minutes and seconds """
    hours = int(avg_time_sec/3600)
    minutes = int((avg_time_sec - (hours*3600))/60)
    seconds = int((avg_time_sec - (hours * 3600) - (minutes * 60)))
    message = "\nAverage trip time over this period is {} hours, {} minutes and {} seconds."
    print(message.format(hours, minutes, seconds))
                 
    print('-'*40)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    """ Count per user type, return text if data is missing """
    try:
        user_types = df['User Type'].dropna(axis = 0).value_counts()

        print('Number of trips per user type:\n', user_types)
    except KeyError:
        print('\nUnfortunately there are no user types available in the data set\n')

    """ Count per gender, return text if data is missing """
    try:
        gender = df['Gender'].dropna(axis = 0).value_counts()

        print('\nNumber of trips per gender:\n', gender)
    except KeyError:
        print('\nUnfortunately there is no user data on gender available in the data set\n')

    """ Display earliest, most recent, and most common year of birth, return text if data is missing """
    try:
        earliest_yob = df['Birth Year'].dropna(axis = 0).min()
        recent_yob = df['Birth Year'].dropna(axis = 0).max()
        common_yob = df['Birth Year'].dropna(axis = 0).mode()

        print('\nAnd now some stats on the birth year of our customers:\n')
        print('\nMost senior cyclist born in:', int(earliest_yob))
        print('\nYoungest cyclist born in:', int(recent_yob))
        print('\nMost commom cyclist born in:', int(common_yob))
    except KeyError:
        print('\nUfortunately there is no user data on birth year available in the data set\n')

    print('-'*40)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    """ Display raw data
    Source: https://stackoverflow.com/questions/43772362/how-to-print-a-specific-row-of-a-pandas-dataframe#43772382"""
    answer = input("\nDo you want to see raw data? Type y or yes to see data\n").lower()
    start = 0
    stop = 9
    while answer in('y', 'yes'):
        print(df.shape[0])
        print(df.iloc[start:stop])
        answer = input("\nDo you want to see more data? Type y or yes to see data\n").lower()
        start += 10
        stop += 10
        if start > df.shape[0]:
            print("\There is no more data to show\n")
            break


    print("\nEnding showing raw data\n")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
