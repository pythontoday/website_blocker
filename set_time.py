import json
from tkinter.filedialog import askopenfilename


def user_block_time(settings_file, start_time, stop_time, b_list):
    """ Saveing received data from user to settings  """
    with open(settings_file, 'w') as f_obj:
        user_data = [
            {
                'start_hours': int(start_time[:2]),
                'start_minutes': int(start_time[3:]),
                'stop_hours': int(stop_time[:2]),
                'stop_minutes': int(stop_time[3:]),
                'blocklist': str(b_list)
            }
        ]
        json.dump(user_data, f_obj, sort_keys=True, indent=4)


def format_user_time(user_input):
    """ Сonvert the entered time to the desired format """
    if len(user_input) < 5:
        user_time_set = '0' + user_input
        return user_time_set
    elif len(user_input) > 5:
        print('Wrong time format. Enter the time in the format: \n HOURS:MINUTES ')
        exit()
    else:
        return user_input


def main():
    """ Get data from user """
    start_time = input('What time will the lock start? \n -> ')
    stop_time = input('What time will the lock stop? \n -> ')
    f_start_time = format_user_time(start_time)
    f_stop_time = format_user_time(stop_time)
    input('Press "Enter" to select a file with a list of sites to block')
    try:
        blocklist = askopenfilename()
    except Exception:
        print('Error opening file. "bloc.txt" from directory will be used')
        blocklist = ('block.txt')
    user_block_time('settings.json', f_start_time, f_stop_time, blocklist)


if __name__ == '__main__':
    main()
