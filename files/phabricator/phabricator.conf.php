<?php

return array(
  'phabricator.base-uri' => 'http://{{domain}}/',

  'mysql.host' => 'localhost',
  'mysql.user' => 'root',

  'metamta.default-address' => 'phabricator@{{domain}}',
  'metamta.domain'          => '{{domain}}',

  'phabricator.timezone'    => 'America/New_York',
  'pygments.enabled'        => true,

  // NOTE: Check default.conf.php for detailed explanations of all the
  // configuration options, including these.

) + phabricator_read_config_file('production');
