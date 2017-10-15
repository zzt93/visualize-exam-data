import pandas as pd


def get_all_table_names(con):
    names = con.execute("SELECT * FROM sqlite_master WHERE type='table';").fetchall()
    return [t[1] for t in names]


def get_all_information_from_table_as_pd_dataframe(con, table_name):
    return pd.read_sql("select * from {};".format(table_name), con)


def do_sql(con, sql):
    return pd.read_sql(sql, con)
