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


-- wipe obsolete table that only causes problems with the sync, could
-- even be dropped entirely (together with imageinfo table).
select now() as time, 'wiping imageinfo listings' as msg;
delete from imageinfo_listing;

-- bump sequences (not strictly needed anymore)
select now() as time, 'bumping sequences' as msg;
alter sequence task_id_seq restart      with 90000000;
alter sequence repo_id_seq restart      with 9000000;
alter sequence imageinfo_id_seq restart with 900000;

-- truncate sessions
select now() as time, 'truncating sessions' as msg;
truncate table sessions;

-- cancel any open tasks
select now() as time, 'canceling open tasks' as msg;
update task set state=3 where state in (0,1,4);

-- cancel any builds in progress
select now() as time, 'canceling builds in progress' as msg;
update build set state=4, completion_time=now() where state=0;

-- set prod volume - only for complete builds; failed, canceled and
-- deleted ones should stay on default (staging) volume so that when
-- they are resubmitted or imported in staging, koji won't try to put
-- them on prod volume (and fall because of read-only filesystem)
select now() as time, 'setting up prod volume' as msg;
insert into volume(name) values('prod');
update build set volume_id=(select id from volume where name='prod') where volume_id=0 and state=1;

-- delete files from incomplete builds to keep DB in sync with
-- filesystem; these builds are on default (staging) volume and their
-- files are not there; keeping rpminfo's ma
delete from rpminfo where build_id in (select id from build where state<>1);

-- expire any active buildroots
select now() as time, 'expiring active buildroots' as msg;
update standard_buildroot set state=3, retire_event=get_event() where state=0;

-- enable/disable hosts
update host set enabled=False;

-- fix host_channels
truncate host_channels;

-- expire all the repos
select now() as time, 'expiring repos' as msg;
update repo set state = 3 where state in (0, 1, 2);


-- add our staging builders, dynamically pulled from ansible inventory

{% for group in builder_groups %}
{% for host in groups[group.name] %}
select now() as time, 'adding staging host {{ host }}' as msg;
delete from host where name='{{ host }}';
delete from users where name='{{ host }}';
insert into users (name, usertype, krb_principal, status) values ('{{ host }}', 1, 'compile/{{ host }}@STG.FEDORAPROJECT.ORG', 0);
insert into host (user_id, name, arches) values (
    (select id from users where name='{{host}}'), '{{host}}', '{{ group.arches }}');
{% for channel in [ 'default', 'appliance', 'vm', 'secure-boot', 'compose', 'eclipse', 'images', 'image'] + group.extra_channels|default([]) %}
insert into host_channels (host_id, channel_id) values (
    (select id from host where name='{{host}}'), (select id from channels where name='{{channel}}'));
{% endfor %}
{% endfor %}
{% endfor %}

-- Add some people to be admins, only in staging.  Feel free to grow this list..

{% for username in ['modularity', 'mizdebsk', 'psabata', 'jkaluza', 'fivaldi', 'mprahl', 'mbs/mbs.stg.fedoraproject.org'] %}
select now() as time, 'adding staging admin {{username}}' as msg;
insert into users (name, usertype, status) values ('{{username}}', 0, 0) on conflict do nothing;
insert into user_perms (user_id, perm_id, active, creator_id) values (
    (select id from users where name='{{username}}'),
    (select id from permissions where name='admin'),
    True,
    (select id from users where name='{{username}}'));
{% endfor %}

-- Allow some users to use content generators, only in staging.
{% for cg_user in cg_users %}
insert into cg_users (cg_id, user_id, creator_id) values (
    (select id from content_generator where name='{{ gc_user.gc_name }}'),
    (select id from users where name='{{ gc_user.user_name }}'),
    (select id from users where name='{{ gc_user.user_name }}'));
{% endfor %}

-- Fix krb principals for some users
{% for username, principal in [('releng', 'compose/koji.stg.fedoraproject.org'),
                               ('koschei', 'koschei/koschei-backend01.stg.phx2.fedoraproject.org'),
                               ('hotness', 'hotness/hotness01.stg.phx2.fedoraproject.org'),
                               ('containerbuild', 'osbs/osbs.stg.fedoraproject.org'),
                               ('kojira', 'kojira/koji.stg.fedoraproject.org')] %}
update users set krb_principal='{{principal}}@STG.FEDORAPROJECT.ORG' where name='{{username}}';
{% endfor %}
update users set krb_principal=replace(krb_principal, '@FEDORAPROJECT.ORG', '@STG.FEDORAPROJECT.ORG');

-- TODO fix kojipkgs url in external repos
