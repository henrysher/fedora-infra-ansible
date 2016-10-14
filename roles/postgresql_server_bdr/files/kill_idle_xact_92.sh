#!/bin/bash

# please configure by setting the folloiwng shell variables

# REQUIRED: set location of log file for logging killed transactions
LOGFILE=/var/lib/pgsql/kill_idle.log

# REQUIRED: set timelimit for oldest idle transaction, in minutes
IDLETIME=30

# REQUIRED: set time limit for the oldest lock wait, in minutes
LOCKWAIT=30

# REQUIRED: set time limit for the oldest active transaction, in minutes
XACTTIME=120

# REQUIRED: set users to be ignored and not kill idle transactions
# generally you want to omit the postgres superuser and the user
# pg_dump runs as from being killed
# if you have no users like this, just set both to XXXXX
SUPERUSER=postgres
BACKUPUSER=XXXXX

# REQUIRED: path to psql, since cron often lacks search paths
PSQL=/bin/psql

# OPTIONAL: set these connection variables.  if you are running as the
# postgres user on the local machine with passwordless login, you will
# not needto set any of these
PGHOST=
PGUSER=postgres
PGPORT=
PGPASSWORD=
PGDATABASE=koji

# you should not need to change code below this line
####################################################

export PGHOST
export PGUSER
export PGPORT
export PGPASSWORD
export PGDATABASE
exec >> $LOGFILE 2>&1

date

$PSQL -q -t -c "SELECT lock_monitor.log_table_locks()"
$PSQL -q -t -c "SELECT lock_monitor.log_txn_locks()"

KILLQUERY="WITH idles AS (
SELECT now() as ts, datname, pid, usename, application_name,
    client_addr, backend_start, xact_start, state_change,
    waiting, query, pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE
  -- avoid system users
  usename != '${SUPERUSER}'
  AND usename != '${BACKUPUSER}'
  AND (
  -- terminate idle txns
    ( state = 'idle in transaction' AND ( now() - state_change ) > '${IDLETIME} minutes' )
    -- terminate lock waits
    OR
    ( state = 'active' AND waiting AND ( now() - state_change ) > '${LOCKWAIT} minutes' )
    -- terminate old txns
    OR
    ( state = 'active' AND ( now() - xact_start ) > '${XACTTIME} minutes' )
  )
)
INSERT INTO lock_monitor.activity
SELECT * FROM idles;"

$PSQL -q -t -c "${KILLQUERY}"

exit 0
