from data.database import Database

if __name__ == '__main__':
    database = Database()
    database.connect()
    with open('database.sql', 'w') as file:
        for line in database.connection.iterdump():
            file.write(f'{line}\n')
    database.connection.close()
