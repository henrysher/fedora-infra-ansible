#!/usr/bin/python2

from __future__ import unicode_literals, print_function

import os
import sys
import psycopg2

from ConfigParser import ConfigParser
from subprocess import call
from urlparse import urlparse

if not os.getenv("DJANGO_SETTINGS_MODULE"):
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
sys.path.insert(0, "/srv/webui/config")

import django
django.setup()


MAILMAN_TABLES_TO_REPLACE = [
    ("domain", "mail_host"),
    ("mailinglist", "mail_host"),
    ("mailinglist", "list_id"),
    ("ban", "list_id"),
    ("bounceevent", "list_id"),
    ("member", "list_id"),
    ("template", "context"),
    ("acceptablealias", "alias"),
]
DJANGO_TABLES_TO_EMPTY = [
    "account_emailconfirmation",
    "openid_openidnonce",
    "openid_openidstore",
    "social_auth_association",
    "social_auth_nonce",
    "social_auth_usersocialauth",
    "socialaccount_socialtoken",
]

def update_col(connection, table, column, where=None, pk="id"):
    cursor = connection.cursor()
    cursor_2 = connection.cursor()
    query = "SELECT {pk}, {c} FROM {t}".format(t=table, c=column, pk=pk)
    if where:
        query += " WHERE {}".format(where)
    #query += " LIMIT 10000"
    cursor.execute(query)
    print(cursor.query)
    updates = []
    for record_id, value in cursor:
        changed_value = value.replace(
            "lists.fedoraproject.org", "lists.stg.fedoraproject.org"
            ).replace(
            "lists.fedorahosted.org", "lists.stg.fedorahosted.org")
        if value == changed_value:
            continue
        if column == pk:
            # Resilience: if the process is halted, there may be old and new
            # values in the same table.
            cursor_2.execute(
                "SELECT 1 FROM {t} WHERE {pk} = %s".format(t=table, pk=pk),
                [changed_value])
            #result = cursor_2.fetchone()
            #print(repr(result), updates, value, changed_value)
            #IF result:
            if cursor_2.fetchone():
                print("Skipping {v} in {t}".format(t=table, v=changed_value))
                continue
        updates.append([changed_value, record_id])
    cursor_2.close()
    if updates:
        query = "UPDATE {t} SET {c} = %s WHERE {pk} = %s".format(
            t=table, c=column, pk=pk)
        print(query, "with %d params" % len(updates))
        cursor.executemany(query, updates)
    cursor.close()


def do_mailman():
    config = ConfigParser()
    config.read("/etc/mailman.cfg")
    conn = psycopg2.connect(config.get("database", "url"))
    #db_url = urlparse(config.get("database", "url"))
    #conn = psycopg2.connect(
    #    "dbname={scheme} user={username} password={password} host={hostname}".format(db_url)
    #    )

    for table, column in MAILMAN_TABLES_TO_REPLACE:
        update_col(conn, table, column)
    update_col(conn, "pendedkeyvalue", "value",
               """ "key" = 'list_id' OR "key" = '_mod_listid'
                  OR "key" = 'envsender'""")

    cursor = conn.cursor()
    cursor.execute("UPDATE \"user\" SET password = 'INVALID'")
    print(cursor.query)
    cursor.execute("UPDATE \"mailinglist\" SET digests_enabled = FALSE")
    print(cursor.query)
    cursor.close()
    conn.commit()
    conn.close()
    call(["sudo", "-u", "mailman", "mailman3", "aliases"])

def do_django():
    from django.db import connection, transaction
    from django.core.management import call_command
    cursor = connection.cursor()
    cursor.execute("UPDATE auth_user SET password = '!INVALID'")
    print(cursor.query)
    # Empty tables that contain sensitive data
    for table in DJANGO_TABLES_TO_EMPTY:
        cursor.execute("DELETE FROM %s" % table)
        print(cursor.query)
    with transaction.atomic():
        cursor.execute("SET CONSTRAINTS ALL DEFERRED")
        # Replace in tables with prod domains:
        update_col(connection, "django_mailman3_maildomain", "mail_domain")
        update_col(connection, "hyperkitty_mailinglist", "name", pk="name")
        cursor.execute("select name from hyperkitty_mailinglist order by name")
        for row in cursor:
            print(row[0])
        update_col(connection, "hyperkitty_thread", "mailinglist_id")
        update_col(connection, "hyperkitty_email", "mailinglist_id")
        cursor.execute("SET CONSTRAINTS ALL IMMEDIATE")
    cursor.close()
    connection.commit()
    call_command("loaddata", "/srv/webui/config/initial-data.json")


def main():
    call(["systemctl", "stop", "mailman3"])
    call(["systemctl", "stop", "httpd"])
    call(["systemctl", "stop", "crond"])
    do_mailman()
    do_django()
    call(["systemctl", "start", "crond"])
    call(["systemctl", "start", "httpd"])
    call(["systemctl", "start", "mailman3"])


if __name__ == "__main__":
    main()
