import psycopg2


class Model:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='KiriloZaliznitsya',
            user='postgres',
            password='q123w456',
            host='localhost',
            port=8080
        )
        self.create_table_train()
        self.create_table_station()
        self.create_table_transit()
        self.create_table_ticket()

    def get_all_attr_table(self, tblnm):
        c = self.conn.cursor()
        c.execute(f'SELECT * FROM {tblnm}')
        return c.fetchall()

    def create_table_train(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS "Train" (
                "Number" SERIAL PRIMARY KEY,
                "Seats amount" integer NOT NULL
            )
        ''')

        # Check if the table exists
        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'Train')")
        table_exists = c.fetchone()[0]

        if not table_exists:
            # Table does not exist, so create it
            c.execute('''
                CREATE TABLE "Train" (
                    "Number" SERIAL PRIMARY KEY,
                    "Seats amount" TEXT NOT NULL
                )
            ''')

        self.conn.commit()

    def add_train(self, stsam):
        c = self.conn.cursor()
        c.execute('INSERT INTO "Train" ("Seats amount") VALUES (%s)', (stsam,))
        self.conn.commit()

    def update_train(self, num, stsam):
        c = self.conn.cursor()
        c.execute(f'SELECT EXISTS(SELECT "Number" FROM "Train" WHERE "Number" = {num})')
        num_exists = c.fetchone()[0]
        if num_exists:
            c.execute('UPDATE "Train" SET "Seats amount"=%s WHERE "Number"=%s', (stsam, num))
            self.conn.commit()
            return 0
        else:
            return 1

    def delete_train(self, num):
        c = self.conn.cursor()
        c.execute(f'SELECT EXISTS(SELECT "Number" FROM "Train" WHERE "Number" = {num})')
        num_exists = c.fetchone()[0]
        if num_exists:
            c.execute('DELETE FROM "Train" WHERE "Number"=%s', (num,))
            self.conn.commit()
            return 0
        else:
            return 1

    def create_table_ticket(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS "Ticket" (
                    "ID" SERIAL PRIMARY KEY,
                    "Price" integer NOT NULL,
                    "Transit_id" integer NOT NULL,
                    "Pas_full_name" character varying(50) NOT NULL
            )
        ''')

        # Check if the table exists
        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'Ticket')")
        table_exists = c.fetchone()[0]

        if not table_exists:
            # Table does not exist, so create it
            c.execute('''
                CREATE TABLE "Train" (
                        "ID" SERIAL PRIMARY KEY,
                        "Price" integer NOT NULL,
                        "Transit_id" integer NOT NULL,
                        "Pas_full_name" character varying(50) NOT NULL
                )
            ''')

        self.conn.commit()

    def add_ticket(self, prc, trs_id, pas_nm):
        c = self.conn.cursor()
        c.execute(f'SELECT EXISTS(SELECT "Tab_id" FROM "Transit" WHERE "Tab_id" = {trs_id})')
        trs_id_exists = c.fetchone()[0]
        if trs_id_exists:
            c.execute('INSERT INTO "Ticket" ("Price","Transit_id","Pas_full_name") VALUES (%s,%s,%s)',
                  (prc, trs_id, pas_nm, ))
            self.conn.commit()
            return 0
        else:
            return 1

    def update_ticket(self, idd, prc, trs_id, pas_nm):
        c = self.conn.cursor()
        c.execute(f'SELECT EXISTS(SELECT "Tab_id" FROM "Transit" WHERE "Tab_id" = {trs_id})')
        trs_id_exists = c.fetchone()[0]
        c.execute(f'SELECT EXISTS(SELECT "ID" FROM "Ticket" WHERE "ID" = {idd})')
        idd_exists = c.fetchone()[0]
        if trs_id_exists and idd_exists:
            c.execute('UPDATE "Ticket" SET "Price"=%s, "Transit_id"=%s, "Pas_full_name"=%s WHERE "ID"=%s',
                  (prc, trs_id, pas_nm, idd, ))
            self.conn.commit()
            return 0
        else:
            return 1

    def delete_ticket(self, idd):
        c = self.conn.cursor()
        c.execute(f'SELECT EXISTS(SELECT "ID" FROM "Ticket" WHERE "ID" = {idd})')
        idd_exists = c.fetchone()[0]
        if idd_exists:
            c.execute('DELETE FROM "Ticket" WHERE "ID"=%s', (idd, ))
            self.conn.commit()
            return 0
        else:
            return 1

    def create_table_station(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS "Station" (
                "ID" SERIAL PRIMARY KEY,
                "name" character varying(50) NOT NULL
            )
        ''')

        # Check if the table exists
        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'Station')")
        table_exists = c.fetchone()[0]

        if not table_exists:
            # Table does not exist, so create it
            c.execute('''
                CREATE TABLE "Station" (
                    "ID" SERIAL PRIMARY KEY,
                    "name" character varying(50) NOT NULL
                )
            ''')

        self.conn.commit()

    def add_station(self, name):
        c = self.conn.cursor()
        c.execute('INSERT INTO "Station" ("name") VALUES (%s)',
                  (name, ))
        self.conn.commit()

    def update_station(self, idd, name):
        c = self.conn.cursor()
        c.execute(f'SELECT EXISTS(SELECT "ID" FROM "Station" WHERE "ID" = {idd})')
        idd_exists = c.fetchone()[0]
        if idd_exists:
            c.execute('UPDATE "Station" SET "name"=%s WHERE "ID"=%s',
                  (name, idd, ))
            self.conn.commit()
            return 0
        else:
            return 1

    def delete_station(self, idd):
        c = self.conn.cursor()
        c.execute(f'SELECT EXISTS(SELECT "ID" FROM "Station" WHERE "ID" = {idd})')
        idd_exists = c.fetchone()[0]
        if idd_exists:
            c.execute('DELETE FROM "Station" WHERE "ID"=%s', (idd, ))
            self.conn.commit()
            return 0
        else:
            return 1

    def create_table_transit(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS "Transit" (
                    "Train_num" integer NOT NULL,
                    "Station_id" integer NOT NULL,
                    "Tab_id" SERIAL PRIMARY KEY,
                    "Date" date NOT NULL
            )
        ''')

        # Check if the table exists
        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'Transit')")
        table_exists = c.fetchone()[0]

        if not table_exists:
            # Table does not exist, so create it
            c.execute('''
                CREATE TABLE "Transit" (
                        "Train_num" integer NOT NULL,
                        "Station_id" integer NOT NULL,
                        "Tab_id" SERIAL PRIMARY KEY,
                        "Date" date NOT NULL
                )
            ''')

        self.conn.commit()

    def add_transit(self, tr_num, st_id, date):
        c = self.conn.cursor()
        c.execute(f'SELECT EXISTS(SELECT "Number" FROM "Train" WHERE "Number" = {tr_num})')
        tr_num_exists = c.fetchone()[0]
        c.execute(f'SELECT EXISTS(SELECT "ID" FROM "Station" WHERE "ID" = {st_id})')
        st_id_exists = c.fetchone()[0]
        if tr_num_exists and st_id_exists:
            c.execute('INSERT INTO "Transit" ("Train_num","Station_id","Date") VALUES (%s,%s,%s)',
                  (tr_num, st_id, date, ))
            self.conn.commit()
            return 0
        else:
            return 1

    def update_transit(self, tr_num, st_id, date, trs_id):
        c = self.conn.cursor()
        c.execute(f'SELECT EXISTS(SELECT "Number" FROM "Train" WHERE "Number" = {tr_num})')
        tr_num_exists = c.fetchone()[0]
        c.execute(f'SELECT EXISTS(SELECT "ID" FROM "Station" WHERE "ID" = {st_id})')
        st_id_exists = c.fetchone()[0]
        c.execute(f'SELECT EXISTS(SELECT "Tab_id" FROM "Transit" WHERE "Tab_id" = {trs_id})')
        trs_id_exists = c.fetchone()[0]
        if trs_id_exists and tr_num_exists and st_id_exists:
            c.execute('UPDATE "Transit" SET "Train_num"=%s, "Station_id"=%s, "Date"=%s WHERE "Tab_id"=%s',
                  (tr_num, st_id, date, trs_id, ))
            self.conn.commit()
            return 0
        else:
            return 1

    def delete_transit(self, trs_id):
        c = self.conn.cursor()
        c.execute(f'SELECT EXISTS(SELECT "Tab_id" FROM "Transit" WHERE "Tab_id" = {trs_id})')
        trs_id_exists = c.fetchone()[0]
        if trs_id_exists:
            c.execute('DELETE FROM "Transit" WHERE "Tab_id"=%s', (trs_id, ))
            self.conn.commit()
            return 0
        else:
            return 1

    def generate_data_train(self, count):
        c = self.conn.cursor()
        c.execute('INSERT INTO "Train" ("Seats amount") SELECT ((RANDOM() * 1000 + 1000)::INT) '
                  'FROM generate_series(1,%s)', (count,))
        self.conn.commit()

    def generate_data_station(self, count):
        c = self.conn.cursor()
        for i in range(count):
            c.execute('INSERT INTO "Station" (name) SELECT random_names.name '
                      'FROM unnest(ARRAY[\'Kiyv\', \'Chernihiv\', \'Nizhyn\','
                      ' \'Novoselivka\', \'Sumy\', \'Studenyky\']) AS random_names(name) '
                      'ORDER BY random() '
                      'LIMIT 1;', (count,))
        self.conn.commit()

    def generate_data_transit(self, count):
        c = self.conn.cursor()
        c.execute('INSERT INTO "Transit" ("Train_num","Station_id","Date") SELECT '
                  'T1."Number" AS "Train_num",'
                  'S1."ID" AS "Station_id",'
                  'current_timestamp - random() * interval \'365 days\' AS "Date" '
                  'FROM '
                  '"Train" T1 '
                  'CROSS JOIN "Station" S1 '
                  'WHERE RANDOM() < 1 '
                  'LIMIT %s;', (count,))
        self.conn.commit()

    def generate_data_ticket(self, count):
        c = self.conn.cursor()
        c.execute('INSERT INTO "Ticket" ("Price", "Transit_id", "Pas_full_name")'
                  'SELECT'
                  'random() * 1000 + 1000,  '
                  '"Tab_id" AS "Transit_id",'
                  'unnest(ARRAY[\'Alice\', \'Bob\', \'Charlie\', \'David\', \'Eva\', \'Frank\'] AS "Pas_full_name"'
                  'FROM "Transit")'
                  'ORDER BY random()'
                  'LIMIT 1000;', (count,))
        self.conn.commit()
