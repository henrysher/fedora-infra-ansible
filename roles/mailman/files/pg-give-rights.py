#!/usr/bin/env python2
# vim: et ts=4 sw=4 fileencoding=utf-8

"""
Give non-admin rights to the database app user.
"""

CONFFILE = "/etc/mailman-migration.conf"


import site
import re
import yaml
import psycopg2


def give_rights(dbhost, dbuser, dbpasswd, dbname, dbreguser=None):
    if dbreguser is None:
        dbreguser = dbname + "app"
    conn = psycopg2.connect(host=dbhost, user=dbuser, password=dbpasswd,
                            database=dbname)
    cur = conn.cursor()
    # Database permissions
    dbrightsquery = "GRANT CONNECT,TEMP ON DATABASE %s TO %s;" % (dbname, dbreguser)
    print dbrightsquery
    cur.execute(dbrightsquery)
    # Table permissions
    cur.execute("""
        SELECT 'GRANT SELECT,INSERT,UPDATE,DELETE,TRUNCATE ON "' || relname || '" TO %s;'
        FROM pg_class
        JOIN pg_namespace ON pg_namespace.oid = pg_class.relnamespace
        WHERE nspname = 'public' AND relkind IN ('r', 'v');
    """ % dbreguser)
    queries = [ q[0] for q in cur ]
    for query in queries:
        print query
        cur.execute(query)
    # Sequence permissions
    cur.execute("""
        SELECT 'GRANT USAGE,SELECT,UPDATE ON ' || relname || ' TO %s;'
        FROM pg_class
        JOIN pg_namespace ON pg_namespace.oid = pg_class.relnamespace
        WHERE nspname = 'public' AND relkind = 'S';
    """ % dbreguser)
    queries = [ q[0] for q in cur ]
    for query in queries:
        print query
        cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()


def main():
    with open(CONFFILE) as conffile:
        conf = yaml.safe_load(conffile)
    site.addsitedir(conf["confdir"])
    import settings_admin

    ## KittyStore
    #dbspec = re.match("""
    #    postgresql://
    #    (?P<user>[a-z]+)
    #    :
    #    (?P<password>[^@]+)
    #    @
    #    (?P<host>[^/]+)
    #    /
    #    (?P<database>[^/?]+)
    #    """, settings_admin.KITTYSTORE_URL, re.X)
    #give_rights(dbspec.group("host"),
    #            dbspec.group("user"),
    #            dbspec.group("password"),
    #            dbspec.group("database")
    #            )

    # HyperKitty
    give_rights(
        settings_admin.DATABASES["default"]["HOST"],
        settings_admin.DATABASES["default"]["USER"],
        settings_admin.DATABASES["default"]["PASSWORD"],
        settings_admin.DATABASES["default"]["NAME"],
    )


if __name__ == "__main__": main()
