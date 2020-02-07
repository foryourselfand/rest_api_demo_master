import datetime

from pytz import timezone


def main():
    now = datetime.datetime.now()
    
    moscow_timezone = timezone('Europe/Moscow')
    eastern_timezone = timezone('US/Eastern')
    
    moscow_localize = moscow_timezone.localize(now)
    eastern_localize = eastern_timezone.localize(now)
    
    print(f'{moscow_localize=}')
    print(f'{eastern_localize=}')

    time_diff = int((moscow_localize - eastern_localize).total_seconds() / 3600)
    print(f'{time_diff=}')
    
    


if __name__ == '__main__':
    main()
