import os
import sqlite3


def create_db(name_of_db: str):
    with sqlite3.connect(name_of_db) as conn:
        conn.execute("""
        create table house (
            house_id        INTEGER PRIMARY KEY,
            address         TEXT not NULL,
            building_year   INTEGER not NULL 
                            );
                    """)

        conn.execute("""    
        create table task (
            task_id          INTEGER PRIMARY KEY,
            count_of_bricks  INTEGER CHECK(count_of_bricks>0) 
                                     CHECK(typeof(count_of_bricks) = 'integer'),
            house_id         INTEGER,
            date             TEXT,
            foreign key(house_id) references house(house_id));
                    """)


name_db = 'house.db'
if os.path.exists(name_db):
    print(f'file {name_db} exists')
else:
    print(f"file {name_db} don't exist")
    create_db(name_db)
