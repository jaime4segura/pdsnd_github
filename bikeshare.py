
import time
import pandas as pd
import numpy as np

#Defining parameters
city_data = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

keys = { 'c': 'Chicago',
         'n': 'New York City',
         'w': 'Washington' }

key_months={'1':'january','2':'february','3':'march',
            '4':'april','5': 'may','6':'june','all':'all months'}

months=['1','2','3','4','5','6','all']

dow={'0': 'monday', '1':'tuesday', '2':'wednesday',
     '3':'thursday', '4':'friday','5':'saturday', '6':'sunday', 'all':'all days'}

days=['0','1','2','3','4','5','6','all']

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
    global city
    try:
        city=str(input("Enter the first letter of the city of interest: c for chicago, n for New York or w for Washington: "))
        city=city.lower()
        while city!='c' and city!="n" and city!="w":
            print("That's not a valid city press c for chicago, n for New York or w for Washington")
            city=str(input("Enter the first letter of the city of interest: c for chicago, n for New York or w for Washington: "))
            city=city.lower()
    except ValueError:
        print("That's not a valid city press c for chicago, n for New York or w for Washington")
    finally:
        print("Let's work with data from "+keys[city])

    # get user input for month (all, january, february, ... , june)
    month="all"
    check=str(input("Do you want to see data from "+keys[city]+" for all available months? y/n: "))
    check=check.lower()
    while check!='y' and check!="n":
        print("Sorry, that is not a valid answer please try again")
        check=str(input("Do you want to see data from "+keys[city]+" for all available months? y/n: "))
        check=check.lower()
    if check=="n":
        month=str(input("There is data available from january to june, Which month do you want? (enter numbers from 1 to 6)"))
        while month not in months:
            print("Sorry that is not a valid month, try again")
            month=str(input("There is data available from january to june, Which month do you want? (enter numbers from 1 to 6)"))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day="all"
    check=str(input("Do you want to see data from "+keys[city]+" for all available days? y/n: "))
    check=check.lower()
    while check!='y' and check!="n":
        print("Sorry, that is not a valid answer please try again")
        check=str(input("Do you want to see data from "+keys[city]+" for all available days? y/n: "))
        check=check.lower()
    if check=="n":
        day=str(input("Which day do you want? (enter numbers from 0 to 6, 0 being monday)"))
        while day not in days:
            print("Sorry that is not a valid day, try again")
            day=str(input("Which day do you want? (enter numbers from 0 to 6, 0 being monday)"))
    print("Calculating statistics for {} in {}, specifically for {} ".format(key_months[month], keys[city], dow[day]))
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
    df=pd.read_csv(city_data[keys[city]])
    df=df.fillna('No info')
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['month']=df['Start Time'].dt.month
    df['day']=df['Start Time'].dt.dayofweek
    df['hour']=df['Start Time'].dt.hour
    df['trip']=df['Start Station']+' - '+df['End Station']
    if month !='all':
        df=df[df.month==int(month)]
    if day !='all':
        df=df[df.day==int(day)]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    com_month=df['month'].mode()
    print('   The most common month for the trips was {}'.format(key_months[str(com_month[0])]))
    # display the most common day of week
    com_day=df['day'].mode()
    print('   The most common day for the trips was {}'.format(dow[str(com_day[0])]))
    # display the most common start hour
    hour=df['hour'].mode()
    print('   The most common hour for the trips was {}'.format(hour[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    start=df['Start Station'].mode()
    end=df['End Station'].mode()
    trip=df['trip'].mode()
    # display most commonly used start station
    print('   The most common start station was {}'.format(start[0]))
    # display most commonly used end station
    print('   The most common end station was {}'.format(end[0]))
    # display most frequent combination of start station and end station trip
    print('   The most common trip was {}'.format(trip[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    avg_trip=df['Trip Duration'].mean()/60
    sum_trips=df['Trip Duration'].sum()/60
    # display total travel time
    print('   The total travel time in minutes was {}'.format(sum_trips))
    # display mean travel time
    print('   The average travel time in minutes was {}'.format(avg_trip))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types, counts of gender and earliest, most recent, and most common year of birth
    if city=='w':
        print(df.groupby(['User Type'])[['trip']].count())
        print('There is no user info for gender and date of birth in {}'.format(keys[city]))
    else:
        print(df.groupby(['User Type', 'Gender'])[['trip']].count())
        df=df[df['Birth Year']!='No info']
        min_year=df['Birth Year'].min()
        max_year=df['Birth Year'].max()
        mode_year=df['Birth Year'].mode()
        print('   The earliest year of birth was {}'.format(min_year))
        print('   The most recent year of birth was {}'.format(max_year))
        print('   The most common year of birth was {}'.format(mode_year[0]))
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def rawdata(df):
    """Ask user if he/she wants to see 5 lines of raw data"""
    check=str(input("Would you like to see 5 lines of raw data? y/n "))
    check=check.lower()
    while check!='y' and check!="n":
        print("Sorry, that is not a valid answer please try again")
        check=str(input("Would you like to see 5 lines of raw data? y/n "))
        check=check.lower()
    if check=="y":
        print(df.head())

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        rawdata(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()