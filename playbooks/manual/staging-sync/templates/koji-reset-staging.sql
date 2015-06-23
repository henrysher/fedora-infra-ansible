-- The following commands tweak a koji db snapshot for use with the koji test environment
-- In addition to this script, the following actions may also need to be taken (generally afterward)
-- * apply any needed schema upgrades
-- * reset the koji-test fs volume
--
-- Example commands for db reset:
-- % su - postgres
-- % dropdb koji
-- % createdb -O koji koji
-- % pg_restore -c -d koji koji.dmp
-- % psql koji koji < koji-stage-reset.sql
--
-- Alternate example for shorter downtime:
-- % su - postgres
-- restore to a different db first
-- % createdb -O koji koji-new
-- % pg_restore -c -d koji-new koji.dmp
-- % psql koji-new koji < koji-stage-reset.sql
-- [apply db updates if needed]
-- [set kojihub ServerOffline setting]
-- => alter database koji rename to koji_save_YYYYMMDD;
-- => alter database koji-new rename to koji;
-- [reset koji-test fs]
-- [unset kojihub ServerOffline setting]


BEGIN;

-- bump sequences (not strictly needed anymore)
select now() as time, 'bumping sequences' as msg;
alter sequence task_id_seq restart      with 90000000;
alter sequence repo_id_seq restart      with 9000000;
alter sequence imageinfo_id_seq restart with 900000;

-- truncate sessions
select now() as time, 'truncating sessions' as msg;
truncate table sessions;

-- prod volume
select now() as time, 'setting up prod volume' as msg;
insert into volume(name) values('prod');
update build set volume_id=(select id from volume where name='prod') where volume_id=0;

-- cancel any open tasks
select now() as time, 'canceling open tasks' as msg;
update task set state=3 where state in (0,1,4);

-- cancel any builds in progress
select now() as time, 'canceling builds in progress' as msg;
update build set state=4, completion_time=now() where state=0;

-- expire any active buildroots
select now() as time, 'expiring active buildroots' as msg;
update buildroot set state=3, retire_event=get_event() where state=0;

-- enable/disable hosts
update host set enabled=False;

-- fix host_channels
truncate host_channels;

-- expire all the repos
select now() as time, 'expiring repos' as msg;
update repo set state = 3 where state in (0, 1, 2);


COMMIT;


BEGIN;

-- add our staging builders, dynamically pulled from ansible inventory
select now() as time, 'adding extra host(s)' as msg;

{% for host in groups['buildvm-stg'] + groups['koji-stg'] %}
insert into users (name, usertype, status) values ('{{ host }}', 1, 0);
insert into host (user_id, name, arches) values (
    (select id from users where name='{{host}}'), '{{host}}', 'i386 x86_64');
insert into host_channels (host_id, channel_id) values (
    (select id from host where name='{{host}}'), (select id from channels where name='default'));
insert into host_channels (host_id, channel_id) values (
    (select id from host where name='{{host}}'), (select id from channels where name='createrepo'));
{% endfor %}

COMMIT;

VACUUM ANALYZE;
