import time
import pandas as pd
import numpy as np
import calendar as clndr


CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

city = month = day = filtertype = None


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (int) month - index of the month to filter by, or "all" to apply no month filter
        (int) day - index of the day of week to filter by, or "all" to apply no day filter
    """
    global city, month, day, filtertype

    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington).
    while True:
        city = input(
            'Would you like to see data for (chicago, new york, washington)? -> ').lower()
        if city in CITY_DATA.keys():
            break
        # print error message if the user choose wrong city
        print('not available answer. please try again!!')
        print('-' * 40)

    # TO DO: get user input for filter option (all, day, month, both)
    while True:
        option = input(
            'Would you like to filter by (1=day), (2=month), (3=both), or (4=none for no filter option)? -> ')

        # TO DO: get user input for day (all, monday, tuseday, ... , sunday)
        if option == '1' or option.lower() == 'day':
            while True:
                day = input('Which day? (i.e 0=Monday), or all -> ')
                if day in [str(i) for i in range(7)]:
                    day = list(clndr.day_name)[int(day)]
                    break
                elif day.title() in list(clndr.day_name):
                    day = day.title()
                    break
                elif day.lower() == 'all':
                    break
                print('invalid filter day. please try again!!')
                print('-' * 40)
            filtertype = 'By Day'
            break

        # TO DO: get user input for month (all, january, february, ... , june)
        elif option == '2' or option.lower() == 'month':
            while True:
                month = input(
                    'Which month [January-June]? (i.e 1=January), or all -> ')
                if month in [str(i) for i in range(7)]:
                    break
                elif month.title() in list(clndr.month_name)[: 7]:
                    month = list(clndr.month_name).index(month.title())
                    break
                elif month.lower() == 'all':
                    break
                print('invalid filter month. please try again!!')
                print('-' * 40)
            filtertype = 'By Month'
            break

        # TO DO: get user input for day of week (all, monday, tuesday, ..)
        elif option == '3' or option.lower() == 'both':
            # first choose day
            while True:
                day = input(
                    'Which day? (i.e 0=Monday) or all -> ')
                if day in [str(i) for i in range(7)]:
                    day = list(clndr.day_name)[int(day)]
                    break
                elif day.title() in list(clndr.day_name):
                    day = day.title()
                    break
                elif day.lower() == 'all':
                    break
                # error message if the user choose wrong day
                print('invalid filter day. please try again!!')
                print('-' * 40)
            # second check month
            while True:
                month = input(
                    'Which month [January - June]? (i.e 1=January), or all -> ')
                if month in [str(i) for i in range(7)]:
                    break
                elif month.title() in list(clndr.month_name)[: 7]:
                    month = list(clndr.month_name).index(month.title())
                    break
                elif month.lower() == 'all':
                    break
                # error message if the user choose wrong month
                print('invalid filter month. please try again!!')
                print('-' * 40)
            filtertype = 'Both'
            break
        elif option == '4' or option.lower() == 'none':
            filtertype = 'None'
            break
        # print error message
        print('invalid option. please try again!!')
        print('-' * 40)
    print('-' * 40)
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

    # handle data
    df = pd.read_csv(f"datasets/{CITY_DATA[city]}")
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month:
        if month != 'all':
            df = df.loc[df['month'] == int(month)]
    if day:
        if day != 'all':
            df = df.loc[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    global month, day, filtertype

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if not month or month == 'all':
        most_common_month = df['month'].map(
            {i: clndr.month_name[i] for i in range(7)}).describe()
        print(
            f"Most common Month: {most_common_month['top']}, Count: {most_common_month['freq']} Filter: {filtertype}")

    # TO DO: display the most common day of week
    if not day or day == 'all':
        most_common_day = df['day_of_week'].describe()
        print(
            f"Most common Day: {most_common_day['top']}, Count: {most_common_day['freq']} Filter: {filtertype}")

    # TO DO: display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    most_common_hour = df['start_hour'].map(
        {i: str(i) for i in range(24)}).describe()
    print(
        f"Most common Hour in the day: {most_common_hour['top']}, Count: {most_common_hour['freq']} Filter: {filtertype}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most frequent combination of start station and end station trip
    most_common_start = df['Start Station'].describe()
    most_common_end = df['End Station'].describe()
    print(
        f"Start Stattion: {most_common_start['top']}, Count: {most_common_start['freq']} -  End Station: {most_common_end['top']}, Count: {most_common_end['freq']} Filter: {filtertype}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Uses sum method to calculate the total trip duration
    total_duration = df['Trip Duration'].sum()
    # Finds out the duration in minutes and seconds format
    minute, second = divmod(total_duration, 60)
    # Finds out the duration in hour and minutes format
    hour, minute = divmod(minute, 60)
    print(
        f"The total trip duration is {hour} hours, {minute} minutes and {second} seconds.")

    # Calculating the average trip duration using mean method
    average_duration = round(df['Trip Duration'].mean())
    # Finds the average duration in minutes and seconds format
    mins, sec = divmod(average_duration, 60)
    # This filter prints the time in hours, mins, sec format if the mins exceed 60
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(
            f"\nThe average trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(
            f"\nThe average trip duration is {mins} minutes and {sec} seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # The total users are counted using value_counts method
    # They are then displayed by their types (e.g. Subscriber or Customer)
    user_type = df['User Type'].value_counts()

    print(f"The types of users by number are given below:\n\n{user_type}")

    # This try clause is implemented to display the numebr of users by Gender
    # However, not every df may have the Gender column, hence this...
    try:
        gender = df['Gender'].value_counts()
        print(f"\nThe types of users by gender are given below:\n\n{gender}")
    except:
        print("\nThere is no 'Gender' column in this file.")

    # Similarly, this try clause is there to ensure only df containing
    #'Birth Year' column are displayed
    # The earliest birth year, most recent birth year and the most common
    # birth years are displayed
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(
            f"\nThe earliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
    except:
        print("There are no birth year details in this file.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

# Function to display the data frame itself as per user request

def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns: 
        None.
    """
    row = 0
    while True:
        answer = input("Do you wish to view some raw data? (1=yes), (0=no) -> ")
        if answer == '1' or answer.lower() == 'yes':
            try:
                print(df[row: row+5])
                row += 5
                continue
            except:
                print('No more Data to Display.')
                print('-'*40)
                break
        elif answer == '0' or answer.lower() == 'no':
            break

        print('invalid option. please choose right answer')
        print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
