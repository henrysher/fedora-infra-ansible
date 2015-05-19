vcl 4.0;

import directors;

backend wiki {
    .host = "localhost";
    .port = "10001";
    .first_byte_timeout = 120s;
}

backend mirrorlists {
    .host = "localhost";
    .port = "10002";
}

backend pkgdb {
    .host = "localhost";
    .port = "10003";
    .first_byte_timeout = 160s;
}

backend fas01 {
    .host = "fas01";
    .port = "http";
    .probe = {
        .url = "/accounts/";
        .interval = 5s;
        .timeout = 5s;
        .window = 5;
        .threshold = 5;
    }
}

backend fas02 {
    .host = "fas02";
    .port = "http";
    .probe = {
        .url = "/accounts/";
        .interval = 5s;
        .timeout = 5s;
        .window = 5;
        .threshold = 5;
    }
}

backend fas03 {
    .host = "fas03";
    .port = "http";
    .probe = {
        .url = "/accounts/";
        .interval = 5s;
        .timeout = 5s;
        .window = 5;
        .threshold = 5;
    }
}

sub vcl_init {
  new fas = directors.round_robin();
  fas.add_backend(fas01);
  fas.add_backend(fas02);
  fas.add_backend(fas03);
}

backend voting {
    .host = "localhost";
    .port = "10007";
    .first_byte_timeout = 160s;
}

backend mirrormanager {
    .host = "localhost";
    .port = "10008";
}

backend bodhi {
    .host = "localhost";
    .port = "10009";
}

backend freemedia {
    .host = "localhost";
    .port = "10011";
}

backend packages {
    .host = "localhost";
    .port = "10016";
}

backend tagger {
    .host = "localhost";
    .port = "10017";
}

backend askbot {
    .host = "localhost";
    .port = "10021";
}

backend blockerbugs {
    .host = "localhost";
    .port = "10022";
}

backend fedocal {
    .host = "localhost";
    .port = "10023";
}

backend kerneltest {
    .host = "localhost";
    .port = "10038";
}

backend paste {
    .host = "localhost";
    .port = "10027";
}

backend mirrormanager2 {
    .host = "localhost";
    .port = "10039";
}

backend koschei {
    .host = "localhost";
    .port = "10040";
}


acl purge {
    "192.168.1.129"; // wiki01.vpn
    "192.168.1.130"; // wiki02.vpn
    "10.5.126.60"; // wiki01.stg
    "10.5.126.63"; // wiki01
    "10.5.126.73"; // wiki02
    "10.5.126.23"; // lockbox01
    "192.168.1.58"; //lockbox01.vpn
}

sub vcl_recv {
    if (req.method == "PURGE") {
        if (!client.ip ~ purge) {
            return (synth(405, "Not allowed"));
        }
        return(purge);
    }

    if (req.url ~ "^/wiki/") {
        set req.backend_hint = wiki;
    }
    if (req.url ~ "^/w/") {
        set req.backend_hint = wiki;
        if (req.url ~ "^/w/skins/") {
            unset req.http.cookie;
            set req.url = regsub(req.url, "\?.*", "");
        }
    }
    if (req.url ~ "^/mirrorlist/") {
        set req.backend_hint = mirrorlists;
    }
    if (req.url ~ "^/pkgdb") {
        set req.backend_hint = pkgdb;
        if (req.url ~ "^/pkgdb/static/") {
            unset req.http.cookie;
            set req.url = regsub(req.url, "\?.*", "");
        }
    }
    if (req.url ~ "^/accounts/") {
        set req.backend_hint = fas.backend();
        if (req.url ~ "^/accounts/static/") {
            unset req.http.cookie;
            set req.url = regsub(req.url, "\?.*", "");
        }
    }
    if (req.url ~ "^/voting/") {
        set req.backend_hint = voting;
        if (req.url ~ "^/voting/static/") {
            unset req.http.cookie;
            set req.url = regsub(req.url, "\?.*", "");
        }
    }
    if (req.url ~ "^/mirrormanager/") {
        set req.backend_hint = mirrormanager;
        if (req.url ~ "^/mirrormanager/static/") {
            unset req.http.cookie;
            set req.url = regsub(req.url, "\?.*", "");
        }
        if (req.url ~ "^/mirrormanager/mirrors") {
            unset req.http.cookie;
            set req.url = regsub(req.url, "\?.*", "");
        }
    }
    if (req.url ~ "^/mirrormanager2/") {
        set req.backend_hint = mirrormanager2;
    }
    if (req.url ~ "^/updates/") {
        set req.backend_hint = bodhi;
        if (req.url ~ "^/updates/static/") {
            unset req.http.cookie;
            set req.url = regsub(req.url, "\?.*", "");
        }
    }
    if (req.url ~ "^/freemedia/") {
        set req.backend_hint = freemedia;
    }
    if (req.url ~ "^/packages/") {
        set req.backend_hint = packages;
        if (req.url ~ "^/packages/_res/") {
            unset req.http.cookie;
            set req.url = regsub(req.url, "\?.*", "");
        }
        if (req.url ~ "^/packages/css/") {
            unset req.http.cookie;
            set req.url = regsub(req.url, "\?.*", "");
        }
    }
    if (req.url ~ "^/tagger/") {
        set req.backend_hint = tagger;
        if (req.url ~ "^/tagger/ui/static/") {
            unset req.http.cookie;
            set req.url = regsub(req.url, "\?.*", "");
        }
    }
    if (req.url ~ "^/calendar") {
        set req.backend_hint = fedocal;
        if (req.url ~ "^/calendar/static/") {
            unset req.http.cookie;
            set req.url = regsub(req.url, "\?.*", "");
        }
    }
    if (req.url ~ "^/kerneltest") {
        set req.backend_hint = kerneltest;
        if (req.url ~ "^/kerneltest/static/") {
            unset req.http.cookie;
            set req.url = regsub(req.url, "\?.*", "");
        }
    }
    if (req.http.X-Forwarded-Server ~ "^paste.fedoraproject.org") {
        set req.backend_hint = paste;
        if (req.url ~ "^/skins/") {
            unset req.http.cookie;
            set req.url = regsub(req.url, "\?.*", "");
        }
        if (req.url ~ "^/addons/") {
            unset req.http.cookie;
            set req.url = regsub(req.url, "\?.*", "");
        }
    }
    if (req.http.X-Forwarded-Server ~ "^ask.fedoraproject.org") {
        set req.backend_hint = askbot;
        if (req.url ~ "^/m/") {
            unset req.http.cookie;
            set req.url = regsub(req.url, "\?.*", "");
        }
    }
    if (req.url ~ "^/koschei") {
        set req.backend_hint = koschei;
        if (req.url ~ "^/koschei/static/") {
            unset req.http.cookie;
            set req.url = regsub(req.url, "\?.*", "");
        }
    }
    if (req.http.X-Forwarded-Server ~ "^qa.fedoraproject.org") {
        if (req.url ~ "^/blockerbugs") {
             set req.backend_hint = blockerbugs;
            if (req.url ~ "^/blockerbugs/static/") {
                unset req.http.cookie;
                set req.url = regsub(req.url, "\?.*", "");
            }
        }
    }

    # Pass any requests with the "If-None-Match" header directly.
    if (req.http.If-None-Match) {
        return (pass);
    }

    # Force lookup if the request is a no-cache request from the client.
#    if (req.http.Cache-Control ~ "no-cache") {
#        purge_url(req.url);
#    }
#    if (req.http.Accept-Encoding) {
#        if (req.url ~ "\.(jpg|png|gif|gz|tgz|bz2|tbz|mp3|ogg)$") {
#            # No point in compressing these
#            remove req.http.Accept-Encoding;
#        } elsif (req.http.Accept-Encoding ~ "gzip") {
#            # This is currently a bug with ipv6, so we need to nuke it.
#            remove req.http.Accept-Encoding;
#        } elsif (req.http.Accept-Encoding ~ "deflate") {
#            set req.http.Accept-Encoding = "deflate";
#        } else {
#            # unknown algorithm
#            remove req.http.Accept-Encoding;
#        }
#    }
}

# When requesting application icons, don't allow cherrypy to set cookies
#sub vcl_backend_fetch {
#    if (req.url ~ "^/pkgdb/appicon/show/") {
#        unset beresp.http.set-cookie;
#    }
#}


# Make sure mirrormanager/mirrors doesn't set any cookies
# (Setting cookies would make varnish store a HIT-FOR-PASS
#  making it always fetch from backend)
sub vcl_backend_response {
    if (bereq.url ~ "^/mirrormanager/mirrors") {
        unset beresp.http.set-cookie;
    }
}
