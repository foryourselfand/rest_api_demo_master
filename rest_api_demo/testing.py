import datetime

from pytz import timezone


def main():
    now = datetime.datetime.now()
    
    first_timezone = timezone('Europe/Moscow')
    second_timezone = timezone('Asia/Yekaterinburg')
    # second_timezone = timezone('US/Eastern')
    
    first_localize = first_timezone.localize(now)
    second_localize = second_timezone.localize(now)
    
    print(f'{first_localize=}')
    print(f'{second_localize=}')

    time_diff = int((first_localize - second_localize).total_seconds() / 3600)
    print(f'{time_diff=}')
    
    


if __name__ == '__main__':
    main()
