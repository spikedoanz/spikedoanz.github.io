```
Listing 2. fetchmailrc
fetchmailrc = {
    'poll_interval':300,
    "logfile":None,
    "postmaster":"esr",
    'bouncemail':TRUE,
    "properties":None,
    'invisible':FALSE,
    'syslog':FALSE,
    # List of server entries begins here
    'servers': [
    # Entry for site `imap.ccil.org' begins:
    {
        "pollname":"imap.ccil.org",
        'active':TRUE,
        "via":None,
        "protocol":"IMAP",
        'port':0,
        'timeout':300,
        'dns':FALSE,
        "aka":["snark.thyrsus.com", "locke.ccil.org", "ccil.org"],
        'users': [
        {
            "remote":"esr",
            "password":"Malvern",
            'localnames':["esr"],
            'fetchall':TRUE,
            'keep':FALSE,
            'flush':FALSE,
            "mda":None,
            'limit':0,
            'warnings':3600,
        }
        ,        ]
    }
    ,
    # Entry for site `imap.netaxs.com' begins:
    {
        "pollname":"imap.netaxs.com",
        'active':TRUE,
        "via":None,
        "protocol":"IMAP",
        'port':0,
        'timeout':300,
        'dns':TRUE,
        "aka":None,
        'users': [
        {
            "remote":"esr",
            "password":"d0wnthere",
            'localnames':["esr"],
            'fetchall':FALSE,
            'keep':FALSE,
            'flush':FALSE,
            "mda":None,
            'limit':0,
            'warnings':3600,
        }
        ,        ]
    }
    ,
    # Entry for site `imap.21cn.com' begins:
    {
        "pollname":"imap.21cn.com",
        'active':FALSE,
        "via":None,
        "protocol":"IMAP",
        'port':0,
        'timeout':300,
        'dns':TRUE,
        "aka":None,
        'users': [
        {
            "remote":"tranxww",
            "password":None,
            'localnames':["esr"],
            'fetchall':TRUE,
            'keep':FALSE,
            'flush':FALSE,
            "mda":None,
            'limit':0,
            'warnings':3600,
        }
        ,        ]
    }
    ,
    # Entry for site `pop.tems.com' begins:
    {
        "pollname":"pop.tems.com",
        'active':FALSE,
        "via":None,
        "protocol":"POP3",
        'port':0,
        'timeout':300,
        'dns':TRUE,
        'uidl':FALSE,
        "aka":None,
        'users': [
        {
            "remote":"ed",
            "password":None,
            'localnames':["esr"],
            'fetchall':TRUE,
            'keep':FALSE,
            'flush':FALSE,
            "mda":None,
            'limit':0,
            'warnings':3600,
        }
        ,        ]
    }
    ,
    # Entry for site `mail.frequentis.com' begins:
    {
        "pollname":"mail.frequentis.com",
        'active':FALSE,
        "via":None,
        "protocol":"IMAP",
        'port':0,
        'timeout':300,
        'dns':TRUE,
        "aka":None,
        'users': [
        {
            "remote":"imaptest",
            "password":None,
            'localnames':["esr"],
            'fetchall':TRUE,
            'keep':FALSE,
            'flush':FALSE,
            "mda":None,
            'limit':0,
            'warnings':3600,
        }
        ,        ]
    }
    ]
}
```
