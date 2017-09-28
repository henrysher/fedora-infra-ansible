# gluster/consolidated

Three things to know about this role:

- It consolidates the gluster/server and gluster/client roles.
- It gets gluster working on F25 and F26.
- It requires a ton of open ports on the hosts for `gluster peer probe` to work.
  See `inventory/group_vars/odcs-backend` for an example.

Our older gluster/server and gluster/client roles only seemed to work for el7.
The advice from `#gluster` was to use the `gluster_volume` ansible module
instead of configuring the `.vol` file directly ourselves.  That is what this
role does.
