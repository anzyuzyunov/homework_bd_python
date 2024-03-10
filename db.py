import psycopg2

conn = psycopg2.connect(database='test_db', user='postgres')
with conn.cursor() as cur:
    def add_table():
        cur.execute('CREATE TABLE if not exists Client(id serial primary key,name varchar(50) not null,'
                    'surname varchar(50) unique not null, '
                    'email varchar(100) unique not null);')
        cur.execute('create table if not exists Phones('
                    'id serial primary key,'
                    'phone VARCHAR(20) unique,'
                    'id_client integer not null REFERENCES Client(id));')
        conn.commit()

    def add_client(name: str, surnmae: str, email: str, phone=None):
        cur.execute("""
            INSERT INTO Client(name,surname,email) 
            VALUES(%s,%s,%s) RETURNING id, name, surname;
            """, (name, surnmae, email))

        new_client = cur.fetchone()
        print(f'Добавлен клиент {new_client}')
        # conn.commit()
        if phone is not None:
            cur.execute("""
            INSERT INTO Phones(phone, id_client) VALUES(%s,%s);
            """, (phone, new_client[0]))
        conn.commit()

    # Добавить телефон
    def add_phone(phone:int, surname: str):
        cur.execute("""
        (SELECT id from Client
        where surname = %s); """,(surname,))
        id = cur.fetchone()[0]
        cur.execute("""
        INSERT INTO Phones(phone, id_client)
        VALUES(%s,%s);""",(phone,id))
        print('Телефон добавлен')
        conn.commit()



    # Замена данных
    def change_data(email, name=None, surname=None, phone=None):
        if not name and not surname and not email and not phone:
            print("Нет данных для изменения")
        cur.execute("""
        select id from Client where email = %s; """,(email,))
        id = cur.fetchone()[0]
        cur.execute("""
        SELECT id from phones where id_client = %s""",(id,))
        id2 = cur.fetchone()[0]
        if name is not None:
            cur.execute("""
            UPDATE Client SET name = %s where id=%s;""", (name, id))
        if surname is not None:
            cur.execute("""
            UPDATE Client SET surname = %s where id=%s;""", (surname, id))
        if phone is not None:
            cur.execute("""
            UPDATE Phones SET phone = %s where id = %s;""", (phone, id2))
        conn.commit()


    # Замена email как уникальное значение
    def change_email(email_current:str,email_new:str):
        cur.execute("""select id from Client where email = %s; """, (email_current,))
        id = cur.fetchone()[0]
        cur.execute("""UPDATE Client SET email = %s where id=%s;""", (email_new, id))
        conn.commit()

    # Удаление телефона если знаем телефон
    def dell_phone(phone: str):
        cur.execute("""
                SELECT id from phones where phone = %s""", (phone,))
        id = cur.fetchone()[0]
        cur.execute("""
        DELETE from phones where id = %s;""",(id,))
        conn.commit()

    # Удаляем все телефоны клиента по фамилии
    def dell_phone_client(surname:str):
        cur.execute("""
                select id from Client where surname = %s; """, (surname,))
        id = cur.fetchone()[0]
        cur.execute("""
        DELETE from phones where id_client = %s;""", (id,))
        conn.commit()


    # Удалить клиента
    def dell_cllient(surname:str):
        cur.execute("""
        select id from Client where surname = %s; """, (surname,))
        id = cur.fetchone()[0]
        cur.execute("""
        DELETE from phones where id_client = %s;""", (id,))
        cur.execute("""
        DELETE from Client where id = %s;""", (id,))
        conn.commit()

    # Поиск по данным клиента
    def search_by_data(email=None, name=None, surname=None, phones=None):
        data = []
        phone = []
        if email is not None:
            cur.execute("""
            SELECT name, surname, email from Client where email = %s;""",(email,))
            name_surname_email = cur.fetchone()
            if name_surname_email == None:
                print('Нет такого клиента')
            else:
                cur.execute("""
                SELECT phone from phones where id_client = (SELECT id from Client where email = %s);""",(email,))
                phone_client = cur.fetchall()
                for p in phone_client:
                    for pp in p:
                        phone.append(pp)
                for i in name_surname_email:
                    data.append(i)
                print(f'Имя: {data[0]}, Фамилия: {data[1]}, Email: {data[2]}, телефон(ы): {', '.join(phone)}')
        elif name is not None:
            cur.execute("""
            SELECT name, surname, email from Client where name = %s;""", (name,))
            name_surname_email = cur.fetchone()
            if name_surname_email == None:
                print('Нет такого клиента')
            else:
                cur.execute("""
                SELECT phone from phones where id_client = (SELECT id from Client where name = %s);""", (name,))
                phone_client = cur.fetchall()
                for p in phone_client:
                    for pp in p:
                        phone.append(pp)
                for i in name_surname_email:
                    data.append(i)
                print(f'Имя: {data[0]}, Фамилия: {data[1]}, Email: {data[2]}, телефон(ы): {', '.join(phone)}')
        elif surname is not None:
            cur.execute("""
            SELECT name, surname, email from Client where surname = %s;""", (surname,))
            name_surname_email = cur.fetchone()
            if name_surname_email == None:
                print('Нет такого клиента')
            else:
                cur.execute("""
                SELECT phone from phones where id_client = (SELECT id from Client where surname = %s);""", (surname,))
                phone_client = cur.fetchall()
                for p in phone_client:
                    for pp in p:
                        phone.append(pp)
                for i in name_surname_email:
                    data.append(i)
                print(f'Имя: {data[0]}, Фамилия: {data[1]}, Email: {data[2]}, телефон(ы): {', '.join(phone)}')
        elif phones is not None:
            cur.execute("""select name, surname, email from client where id = (select id_client from phones where phone = %s);""",(phones,))

            name_surname_email = cur.fetchone()
            if name_surname_email == None:
                print('Нет такого клиента')
            else:
                cur.execute("""select phone from phones where id_client = (SELECT id_client from phones where phone = %s)""",(phones,))
                phone_client = cur.fetchall()
                for p in phone_client:
                    for pp in p:
                        phone.append(pp)
                for i in name_surname_email:
                    data.append(i)
                print(f'Имя: {data[0]}, Фамилия: {data[1]}, Email: {data[2]}, телефон(ы): {', '.join(phone)}')



conn.close()


