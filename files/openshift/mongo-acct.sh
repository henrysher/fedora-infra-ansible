#!/bin/bash
mongo stickshift_broker_dev --eval 'db.addUser("stickshift", "mooo")'
mongo stickshift_broker_dev --eval 'db.auth_user.update({"_id":"admin"}, {"_id":"admin","user":"admin","password":"2a8462d93a13e51387a5e607cbd1139f"} , true)'
echo "Acct setup done on `date`" > /etc/mongo-acct-setup

        
        