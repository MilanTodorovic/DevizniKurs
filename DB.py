import sqlite3
import datetime

def create_tables():

    conn = sqlite3.connect('val.db')
    c = conn.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS brValute(numName INTEGER UNIQUE, acroName TEXT UNIQUE, fName TEXT UNIQUE)')
    c.execute('CREATE TABLE IF NOT EXISTS dateId(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT UNIQUE)')
    c.execute('CREATE TABLE IF NOT EXISTS nbsEfektiva(id INTEGER NOT NULL,'
              ' kupovni REAL, prodajni REAL, datum TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS ersteDevize(id INTEGER NOT NULL,'
              ' kupovni REAL, srednji REAL, prodajni REAL, datum TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS ersteEfektiva(id INTEGER NOT NULL, kupovni REAL, prodajni REAL, datum TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS raiffDevize(id INTEGER NOT NULL,'
              ' kupovni REAL, srednji REAL, prodajni REAL, datum TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS raiffEfektiva(id INTEGER NOT NULL, kupovni REAL, prodajni REAL, datum TEXT)')

    c.close()
    conn.close()

def input_db(mode=0, date=str(datetime.date.today().strftime("%Y-%m-%d")), *args, **kwargs):
    conn = sqlite3.connect('val.db')
    c = conn.cursor()

    # date = str(datetime.date.today().strftime("%Y-%m-%d"))

    if mode == 0:
        for arg in args:
            if len(arg)>0:
                c.execute('INSERT OR IGNORE INTO brValute(numName, fName, acroName) VALUES(?,?, ?)', (arg[0],'Null',arg[2]))
                c.execute('SELECT COUNT(*) FROM nbsEfektiva WHERE datum = ? AND id = ? GROUP BY id', (date, arg[0]))
                x = c.fetchone()
                if x==None or x[0]==0:
                    c.execute('INSERT INTO nbsEfektiva(id, kupovni, prodajni, datum) VALUES(?,?,?,?)', (arg[0],
                                                                                                      arg[4].replace(',', '.'),
                                                                                                      arg[5].replace(',', '.'),
                                                                                                      date))
                else:
                    print('Nista nije dodato. NBS')

    elif mode == 1:
        for arg in args:
            if len(arg)>0:
                c.execute('INSERT OR IGNORE INTO brValute(numName, fName, acroName) VALUES(?,?,?)', (arg[0], arg[2],arg[1]))
                c.execute('SELECT COUNT(*) FROM ersteDevize WHERE datum = ? AND id = ? GROUP BY id', (date, arg[0]))
                x = c.fetchone()
                if x==None or x[0]==0:
                    c.execute('INSERT INTO ersteDevize(id, kupovni, srednji, prodajni, datum) VALUES(?,?,?,?,?)',
                              (arg[0], arg[6], arg[7], arg[8], date))
                    c.execute('INSERT INTO ersteEfektiva(id, kupovni, prodajni, datum) VALUES(?,?,?,?)',
                              (arg[0], arg[4], arg[5], date))
                else:
                    print('Nista nije dodato. ERSTE')

    elif mode == 2:
        for arg in args:
            if len(arg)>0:
                if c.execute('SELECT COUNT(*) FROM brValute WHERE numName = ?',(arg[0],)).fetchone()[0]:
                    pass
                else:
                    c.execute('INSERT OR IGNORE INTO brValute(numName,fName, acroName) VALUES(?,?,?)', (arg[0], arg[1],arg[2]))
                c.execute('SELECT COUNT(*) FROM raiffDevize WHERE datum = ? AND id = ? GROUP BY id', (date, arg[0]))
                x = c.fetchone()
                if x==None or x[0]==0:
                    c.execute('INSERT INTO raiffDevize(id, kupovni, srednji, prodajni, datum) VALUES(?,?,?,?,?)',
                              (arg[0], arg[4], arg[5], arg[6], date))
                    c.execute('INSERT INTO raiffEfektiva(id, kupovni, prodajni, datum) VALUES(?,?,?,?)',
                              (arg[0], arg[7], arg[8], date))
                else:
                    print('Nista nije dodato. Raiffeisen')

    conn.commit()
    c.close()
    conn.close()

def read_db():
    conn = sqlite3.connect('val.db')
    c = conn.cursor()

    lst = list()

    # date = str(datetime.date.today().strftime("%Y-%m-%d"))
    # c.execute('SELECT COUNT(*) FROM nbsValute WHERE datum = ? AND id = ? GROUP BY id', (date,'36'))
    # x=c.fetchone()
    # print(x)
    # if x == None:
    #     print(x)
    # else:
    #     print('Test je pao')
    c.execute('SELECT prodajni FROM nbsEfektiva WHERE id=978 ORDER BY datum')
    a = c.fetchall()
    lst.append(a)

    c.execute('SELECT prodajni FROM ersteEfektiva WHERE id=978 ORDER BY datum')
    b = c.fetchall()
    lst.append(b)

    c.execute('SELECT prodajni FROM raiffEfektiva WHERE id=978 ORDER BY datum')
    d = c.fetchall()
    lst.append(d)

    c.execute('SELECT datum FROM nbsefektiva WHERE id=978 ORDER BY datum')
    e = c.fetchall()
    lst.append(e)

    c.close()
    conn.close()

    return lst

def checkDate(date):
    conn = sqlite3.connect('val.db')
    c = conn.cursor()

    c.execute('SELECT id FROM dateId WHERE date=?',(date,))
    try:
        s = c.fetchone()[0]
    except:
        s = 0
    c.close()
    conn.close()
    # print(s)
    return s

def drop_tables():
    conn = sqlite3.connect('val.db')
    c = conn.cursor()

    c.executescript('DROP TABLE IF EXISTS brValute;'
                    'DROP TABLE IF EXISTS dateId;'
                    'DROP TABLE IF EXISTS nbsEfektiva;'
                    'DROP TABLE IF EXISTS ersteValute;'
                    'DROP TABLE IF EXISTS ersteDevize;'
                    'DROP TABLE IF EXISTS ersteEfektiva;'
                    'DROP TABLE IF EXISTS raiffValute;'
                    'DROP TABLE IF EXISTS raiffDevize;'
                    'DROP TABLE IF EXISTS raiffEfektiva;')


    conn.commit()
    c.close()
    conn.close()
