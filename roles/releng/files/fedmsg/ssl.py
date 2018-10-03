
suffix = "phx2.fedoraproject.org"
app_hosts = [
    "app01.phx2.fedoraproject.org",
    "app02.phx2.fedoraproject.org",
    "app03.phx2.fedoraproject.org",
    "app04.phx2.fedoraproject.org",
    "app05.fedoraproject.org",
    "app07.phx2.fedoraproject.org",
    "app08.fedoraproject.org",
]

config = dict(
    sign_messages=True,
    validate_signatures=False,
    ssldir="/etc/pki/fedmsg",

    crl_location="https://fedoraproject.org/fedmsg/crl.pem",
    crl_cache="/var/run/fedmsg/crl.pem",
    crl_cache_expiry=86400,  # Daily

    certnames=dict(
    [
        ("shell.app0%i" % i, "shell-%s" % app_hosts[i-1])
        for i in range(1, len(app_hosts) + 1)
    ] + [
        ("bodhi.app0%i" % i, "bodhi-%s" % app_hosts[i-1])
        for i in range(1, len(app_hosts) + 1)
    ] + [
        ("mediawiki.app0%i" % i, "mediawiki-%s" % app_hosts[i-1])
        for i in range(1, len(app_hosts) + 1)
    ] + [
        ("shell.fas0%i" % i, "shell-fas0%i.%s" % (i, suffix))
        for i in range(1, 4)
    ] + [
        ("fas.fas0%i" % i, "fas-fas0%i.%s" % (i, suffix))
        for i in range(1, 4)
    ] + [
        ("shell.packages0%i" % i, "shell-packages0%i.%s" % (i, suffix))
        for i in range(1, 3)
    ] + [
        ("shell.pkgs0%i" % i, "shell-pkgs0%i.%s" % (i, suffix))
        for i in range(1, 2)
    ] + [
        ("scm.pkgs0%i" % i, "scm-pkgs0%i.%s" % (i, suffix))
        for i in range(1, 2)
    ] + [
        ("shell.relepel01", "shell-relepel01.%s" % suffix),
        ("shell.releng04", "shell-releng04.%s" % suffix),
        ("shell.branched-composer", "shell-releng01.%s" % suffix),
        ("shell.rawhide-composer", "shell-releng02.%s" % suffix),
        ("bodhi.relepel01", "bodhi-relepel01.%s" % suffix),
        ("bodhi.releng04", "bodhi-releng04.%s" % suffix),
        ("bodhi.branched-composer", "bodhi-releng01.%s" % suffix),
        ("bodhi.rawhide-composer", "bodhi-releng02.%s" % suffix),
    ] + [
        ("shell.value01", "shell-value01.%s" % suffix),
        ("shell.value03", "shell-value03.%s" % suffix),
        ("supybot.value03", "supybot-value03.%s" % suffix),
    ])
)

