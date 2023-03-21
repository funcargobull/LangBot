from sqlite3 import connect


def language(id, language, set, get):
    db = connect("languages.db")
    sql = db.cursor()
    sql.execute(f"SELECT language FROM languages WHERE id = '{id}'")

    if set and not get:
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO languages VALUES (?, ?)", (id, language))
            db.commit()
        else:
            sql.execute(f"DELETE FROM languages WHERE id = '{id}'")
            sql.execute(f"INSERT INTO languages VALUES (?, ?)", (id, language))
            db.commit()

    elif get and not set:
        for _, lang in sql.execute(f"SELECT * FROM languages WHERE id = '{id}'"):
            return lang
