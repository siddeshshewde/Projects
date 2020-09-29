import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "testtt.db")

print (db_path)
#connection = sqlite3.connect('ads_txt.db')

with sqlite3.connect(db_path) as db:

    #c = connection.cursor()
    insert_stmt = "create table ads_txt_parsed_lines (        row_id integer NOT NULL PRIMARY KEY AUTOINCREMENT, domain_name varchar(100) NOT NULL,        advertiser_domain varchar(100),        publisher_id int(50),        account_type varchar(100),        cert_authority_id varchar(100),        line_number int(10),        is_valid_syntax tinyint(1) DEFAULT 0,        raw_string varchar(200),        creation_date datetime DEFAULT CURRENT_TIMESTAMP,        updation_date datetime DEFAULT CURRENT_TIMESTAMP    );"
    db.execute(insert_stmt)
    check_stmt = "select * from ads_txt_parsed_lines;"
    db.execute(check_stmt)
    db.commit()

db.close()
print ('Database Connection Closed.')   