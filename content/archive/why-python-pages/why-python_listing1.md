```
Listing 1. fetchmail Configuration File
set postmaster "esr"
set daemon 300
poll imap.ccil.org with proto IMAP and options no dns
    aka snark.thyrsus.com locke.ccil.org ccil.org
       user esr there is esr here options fetchall dropstatus warnings 3600
poll imap.netaxs.com with proto IMAP
       user "esr" there is esr here options dropstatus warnings 3600
skip imap.21cn.com with proto IMAP
       user esr here is tranxww there options fetchall
skip pop.tems.com with proto POP3:
       user esr here is ed there options fetchall
skip mail.frequentis.com with proto IMAP:
       user esr here is imaptest there with options fetchall
```
