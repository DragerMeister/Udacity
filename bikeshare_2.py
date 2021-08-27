import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
DAYS = ('all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ('chicago', 'new york', 'washington')
    while True:
        city = input("Which city would you like to look at? Chicago, New York, or Washington? \n").lower()

        if city in cities:
            break

    # get user input for month (all, january, february, ... , june)
    months = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
    while True:
        month = (input("Which month would you like to look at? You can choose january through june. Or type 'all' for all of them\n")).lower()

        if month in months:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ('all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')
    while True:
        day = (input("Which day would you like to select? Type in the name of the day or all to select all days. \n")).lower()

        if day in days:
            break

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
    #create the DataFrame
    #I'll be honest, I was struggling with this bit of code so I searched the internet and found what I needed to get started.
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns. New columns are needed for filtering.
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        month =  MONTHS.index(month) + 1
        df = df[ df['month'] == month ]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[ df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df.groupby('Start Time')['month'].mean()
    print('Here is the most common month of travel: ', most_common_month)

    # display the most common day of week
    most_common_day = df.groupby('Start Time')['day'].mean()
    print('Here is the most common day of travel: ', most_common_day)

    # display the most common start hour
    most_common_hour = df.groupby('Start Time')['hour'].mean()
    print('Here is the most common hour of travel: ', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df.groupby('Start Station').sum()
    print('The most common start station is: ', most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df.groupby('End Station').sum()
    print('The most common start station is: ', most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_combo = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('The most common combination of start and end station is: ', most_common_combo)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print("The total time traveled is: ", total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time is: ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby(['User Type']).sum()
    print('The total number of different user types are: \n', user_types)

    # Display counts of gender
    gender = df.groupby(['Gender']).sum()
    print('The total number of different user types are: ', gender)

    # Display earliest, most recent, and most common year of birth
    earliest_birthyear = df['Birth Year'].min()
    print('The first birthyear is: ', earliest_birthyear)

    most_recent_birthyear = df['Birth Year'].max()
    print('The last birthyear is: ', most_recent_birthyear)

    most_common_birthyear = df['Birth Year'].mode()
    print('The most common birthyear is: ', most_common_birthyear)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
