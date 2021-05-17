import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    while True:
        city = input('\nPlease enter one of the following cities: chicago, new york city, washington:')
        city = city.lower()
        if city not in CITY_DATA:
            print('\nYou have entered an invalid city name, please enter one of the cities (example: chicago):')
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nPlease type "All" to view all months or enter a specific month from january to june: ')
        month = month.lower()
        months = ['january','february','march','april','may','june']
        if month != 'all' and month not in months:
            print('\nPlease enter a valid month (example: january) or enter All to view all months')
        else:
            break


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nPlease type "All" to view all days of the week or enter a specific day from sunday to saturday: ')
        day = day.lower()
        week_days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
        if day != 'all' and day not in week_days:
            print('\nPlease enter a valid week day (example: sunday) or enter All to view all week days')
        else:
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nWe are now calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0] #this will return month number
    print('\nThe most common month is: ', calendar.month_name[common_month]) #get the month name from month number using calendar


    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('\nThe most common day of the week is: ',common_day)

    # display the most common start hour
    #need to extract hour from the start time to create hour column
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]

    print('\nThe most common Start Hour is: ', common_hour, 'H00')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('\nThe most commonly used start station is: ', common_start_station)


    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('\nThe most commonly used end station is: ', common_end_station)


    # display most frequent combination of start station and end station trip
    df["Combined_stations"] = df["Start Station"] +' and ' + df["End Station"]
    frequent_combined_stations = df["Combined_stations"].mode()[0]
    print('\nThe most frequent combination of Start Station and End Station trip: ', frequent_combined_stations )


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('\nThe total travel time is ', total_time/3600, ' hours')


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nThe mean travel time is ', mean_travel_time/3600, ' hours')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_raw_data(df):
    """
    Displays raw data upon request by the user as required on the Project Rubric

    Args:
    Pandas dataframe containing city data

    """
    i=0
    raw_data_reply = input('Would you like to view the first first 5 rows of the raw data? Yes/No: ')
    while True:

        if raw_data_reply.lower() == 'no':
            break
        print(df[i:i+5])
        #print(df.head(i))
        raw_data_reply = input('Would you like to view the next first 5 rows of the raw data? Yes/No: ').lower()
        i+=5




def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].value_counts().to_frame()
    print('\nCounts of user types is:\n', user_count)


    # Display counts of gender
    # Due to washington data not having 'Gender' column, an if check needs to be done first
    if 'Gender' in df:
        gender_count = df['Gender'].value_counts().to_frame()
        print('\nThe gender count is:\n', gender_count)
    else:
        print('\nThe data does not contain Gender column')


    # Display earliest, most recent, and most common year of birth
    # Due to washington data not having 'Birth Year' column, an if check needs to be done first
    if 'Birth Year' in df:
        earliest_birth_year = int(df['Birth Year'].min())
        print('\nThe earliest birth year is: ', earliest_birth_year)
        most_recent_birth_year = int(df['Birth Year'].max())
        print('\nThe most recent birth year is: ', most_recent_birth_year)
        most_common_birth_year = int(df['Birth Year'].mode())
        print('\nThe most common birth year is: ', most_common_birth_year)
    else:
        print('\nThe data does not contain Birth Year column')



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        view_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
