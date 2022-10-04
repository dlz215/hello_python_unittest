import sqlite3

db_url = 'miles.db'

with sqlite3.connect(db_url) as conn:
    conn.execute('CREATE TABLE IF NOT EXISTS miles (vehicle text, total_miles float)')
conn.close()


"""
Before running this code, ensure that miles.db exists and contains the miles table
If not, create expected miles table by running the following SQL on the database, 
create table miles (vehicle text, total_miles float);
"""

class MileageError(Exception):
    pass


def add_miles(vehicle, new_miles):
    """ If the vehicle is in the database, increment the number of miles by new_miles
    If the vehicle is not in the database, add the vehicle and set the number of miles to new_miles
    If the vehicle is None or new_miles is not a positive number, raise MileageError
    """

    if not vehicle:
        raise MileageError('Provide a vehicle name')
    if not isinstance(new_miles, (int, float)) or new_miles < 0:
        raise MileageError('Provide a positive number for new miles')

    vehicle = vehicle.upper().strip() 

    if not vehicle:
        raise MileageError('Provide a vehicle name')
    

    with sqlite3.connect(db_url) as conn:
        # Attempt to update miles
        rows_mod = conn.execute('UPDATE miles SET total_miles = total_miles + ? WHERE vehicle = ?', (new_miles, vehicle))
        if rows_mod.rowcount == 0:
            # If update is not made, vehicle is not yet in DB. Insert new vehicle
            conn.execute('INSERT INTO miles VALUES (?, ?)', (vehicle, new_miles))
    conn.close()


def main():
    while True:
        vehicle = input('Enter vehicle name or enter to quit: ')
        if not vehicle:
            break
        miles = float(input(f'Enter new miles for {vehicle}: ')) ## TODO input validation

        add_miles(vehicle, miles)


if __name__ == '__main__':
    main()
