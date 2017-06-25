#!/usr/bin/python2

from __future__ import unicode_literals, print_function

import os
import sys
import psycopg2

from ConfigParser import ConfigParser
from subprocess import call
from urlparse import urlparse

if not os.getenv("DJANGO_SETTINGS_MODULE"):
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings_admin"
sys.path.insert(0, "/srv/webui/config")

import django
django.setup()


MAILMAN_TABLES_TO_REPLACE = [
    ("domain", "mail_host"),
    ("mailinglist", "mail_host"),
    ("mailinglist", "list_id"),
    #("ban", "list_id"),
    #("bounceevent", "list_id"),
    #("member", "list_id"),
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
DJANGO_INDICES_TO_RECREATE = [
    ("hyperkitty_thread", "hyperkitty_thread_mailinglist_id", "(mailinglist_id)"),
    ("hyperkitty_thread", "hyperkitty_thread_mailinglist_id_like", "(mailinglist_id varchar_pattern_ops)"),
    ("hyperkitty_email", "hyperkitty_email_mailinglist_id", "(mailinglist_id)"),
    ("hyperkitty_email", "hyperkitty_email_mailinglist_id_like", "(mailinglist_id varchar_pattern_ops)"),
]
DJANGO_CONSTRAINTS_TO_RECREATE = [
    ("hyperkitty_thread", "hyperkitty_thread_mailinglist_id_371b52d98485a593_uniq", "UNIQUE (mailinglist_id, thread_id)"),
    ("hyperkitty_thread", "mailinglist_id_refs_name_3725eec2", "FOREIGN KEY (mailinglist_id) REFERENCES hyperkitty_mailinglist(name) DEFERRABLE INITIALLY DEFERRED"),
    ("hyperkitty_email", "hyperkitty_email_mailinglist_id_57f04aace3f8ee5e_uniq", "UNIQUE (mailinglist_id, message_id)"),
    ("hyperkitty_email", "mailinglist_id_refs_name_654506d3", "FOREIGN KEY (mailinglist_id) REFERENCES hyperkitty_mailinglist(name) DEFERRABLE INITIALLY DEFERRED"),
]


def get_mapping(cursor, table, column):
    ml_mapping = {}
    query = "SELECT {c} FROM {t}".format(c=column, t=table)
    print(query)
    cursor.execute(query)
    for row in cursor:
        value = row[0]
        orig_value = value.replace(
            "lists.stg.fedoraproject.org", "lists.fedoraproject.org"
            ).replace(
            "lists.stg.fedorahosted.org", "lists.fedorahosted.org")
        changed_value = value.replace(
            "lists.fedoraproject.org", "lists.stg.fedoraproject.org"
            ).replace(
            "lists.fedorahosted.org", "lists.stg.fedorahosted.org")
        if orig_value == changed_value:
            continue
        ml_mapping[orig_value] = changed_value
    return ml_mapping


def update_col_1(connection, table, column, where=None, pk="id"):
    cursor = connection.cursor()
    cursor_2 = connection.cursor()
    where = " WHERE {}".format(where) if where is not None else ""
    #query = "SELECT COUNT(*) FROM {t} {w}".format(t=table, w=where)
    #cursor.execute(query)
    #count = cursor.fetchone()[0]
    query = "SELECT {pk}, {c} FROM {t} {w}".format(
        t=table, c=column, pk=pk, w=where)
    #query += " LIMIT 10000"
    print(query)
    #print("{} lines".format(count))
    updates = []
    cursor.execute(query)
    print(cursor.query)
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
            if cursor_2.fetchone():
                print("Skipping {v} in {t}".format(t=table, v=changed_value))
                continue
        updates.append([changed_value, record_id])
    cursor_2.close()
    print("Doing {} updates now".format(len(updates)))
    query = "UPDATE {t} SET {c} = %s WHERE {pk} = %s".format(
        t=table, c=column, pk=pk)
    print(query, "with %d params" % len(updates))
    cursor.executemany(query, updates)


def update_col_2(ml_mapping, cursor, table, column, where=None):
    query_where = " AND {}".format(where) if where is not None else ""
    query = "SELECT COUNT(*) FROM {t} {w}".format(t=table, w=where)
    cursor.execute(query)
    count = cursor.fetchone()[0]
    print("Updating {} rows.".format(count))
    for name_orig, name_new in ml_mapping.items():
        query = "UPDATE {t} SET {c} = %s WHERE {c} = %s {w}".format(
            t=table, c=column, w=query_where)
        params = (name_new, name_orig)
        print(query % params)
        cursor.execute(query, params)


def do_mailman():
    config = ConfigParser()
    config.read("/etc/mailman.cfg")
    conn = psycopg2.connect(config.get("database", "url"))
    #db_url = urlparse(config.get("database", "url"))
    #conn = psycopg2.connect(
    #    "dbname={scheme} user={username} password={password} host={hostname}".format(db_url)
    #    )

    with conn.cursor() as cursor:
        ml_mapping = get_mapping(cursor, "mailinglist", "list_id")
        for table, column in MAILMAN_TABLES_TO_REPLACE:
            update_col_1(conn, table, column)
        update_col_2(ml_mapping, cursor, "ban", "list_id")
        update_col_2(ml_mapping, cursor, "member", "list_id")
        update_col_2(ml_mapping, cursor, "bounceevent", "list_id")
        update_col_1(conn, "pendedkeyvalue", "value",
                     """ "key" = 'list_id' OR "key" = '_mod_listid' """
                     """ OR "key" = 'envsender'""")

        cursor.execute("UPDATE \"user\" SET password = 'INVALID'")
        print(cursor.query)
        cursor.execute("UPDATE \"mailinglist\" SET digests_enabled = FALSE")
        print(cursor.query)
    conn.commit()
    conn.close()
    call(["sudo", "-u", "mailman", "mailman3", "aliases"])


def do_django():
    from django.db import connection, transaction
    from django.core.management import call_command
    with connection.cursor() as cursor:
        cursor.execute("UPDATE auth_user SET password = '!INVALID'")
        print(cursor.query)
        # Empty tables that contain sensitive data
        for table in DJANGO_TABLES_TO_EMPTY:
            cursor.execute("DELETE FROM %s" % table)
            print(cursor.query)
        #for table, name, create in DJANGO_CONSTRAINTS_TO_RECREATE:
        #    cursor.execute(
        #        "ALTER TABLE {t} DROP CONSTRAINT IF EXISTS {n}".format(
        #            t=table, n=name))
        #    print(cursor.query)
        for table, name, column in DJANGO_INDICES_TO_RECREATE:
            cursor.execute("DROP INDEX IF EXISTS {n}".format(t=table, n=name))
            print(cursor.query)
        with transaction.atomic():
            cursor.execute("SET CONSTRAINTS ALL DEFERRED")
            ml_mapping = get_mapping(cursor, "hyperkitty_mailinglist", "name")
            # Replace in tables with prod domains:
            update_col_1(connection, "django_mailman3_maildomain", "mail_domain")
            update_col_1(connection, "hyperkitty_mailinglist", "name", pk="name")
            update_col_2(ml_mapping, cursor, "hyperkitty_thread", "mailinglist_id")
            update_col_2(ml_mapping, cursor, "hyperkitty_email", "mailinglist_id")
            cursor.execute("SET CONSTRAINTS ALL IMMEDIATE")
        for table, name, column in DJANGO_INDICES_TO_RECREATE:
            cursor.execute("CREATE INDEX {n} ON {t} {c}".format(
                           n=name, t=table, c=column))
            print(cursor.query)
        #for table, name, create in DJANGO_CONSTRAINTS_TO_RECREATE:
        #    cursor.execute("ALTER TABLE {t} ADD CONSTRAINT {n} {c}".format(
        #                   n=name, t=table, c=create))
        #    print(cursor.query)
    connection.commit()
    call_command("loaddata", "/srv/webui/config/initial-data.json")


def main():
    call(["systemctl", "stop", "webui-qcluster"])
    call(["systemctl", "stop", "mailman3"])
    call(["systemctl", "stop", "httpd"])
    call(["systemctl", "stop", "crond"])
    do_mailman()
    do_django()
    call(["systemctl", "start", "crond"])
    call(["systemctl", "start", "httpd"])
    call(["systemctl", "start", "mailman3"])
    call(["systemctl", "start", "webui-qcluster"])


if __name__ == "__main__":
    main()
