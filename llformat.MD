
Ищем свое устройство (в данном случае это sdb) и удостоверяемся, что оно "не 
заморожено" (not     frozen)
```bash
$sudo hdparm -I /dev/sdb | egrep 'Model Number|Serial Number|frozen|LBA48|Sector size'
```

        Model Number:       ST3500514NS                             
        Serial Number:      9WJ0HN29
        LBA48  user addressable sectors:  976773168
        Logical/Physical Sector size:           512 bytes
        not     frozen


Если "замороженно"(`frozen`), то пока найден один способ "разморозки"(`not     frozen`) устройства, это 
посылка ОС в suspend to ram.

**Вывести ОС из этого состояния можно нажатием любой клавиши клавиатуры или мышки.** 

```bash
$ echo mem | sudo tee /sys/power/state
```

Проверяем состояние "заморозки"

```bash
$sudo hdparm -I /dev/sdb | egrep 'Model Number|Serial Number|frozen|LBA48|Sector size'
```

        Model Number:       ST3500514NS                             
        Serial Number:      9WJ0HN29
        LBA48  user addressable sectors:  976773168
        Logical/Physical Sector size:           512 bytes
        not     frozen

Смотрим количество используемых/доступных блоков
```bash
$sudo hdparm -N /dev/sdb
```

        /dev/sdb:
        max sectors   = 976773168/976773168, HPA is disabled

Количество блоков 976773168. Пробуем установить 777777777 блоков.
```bash
$sudo hdparm -N777777777 /dev/sdb
```

        /dev/sdb:
        setting max visible sectors to 777777777 (temporary)
        Use of -Nnnnnn is VERY DANGEROUS.
        You have requested reducing the apparent size of the drive.
        This is a BAD idea, and can easily destroy all of the drive's contents.
        Please supply the --yes-i-know-what-i-am-doing flag if you really want this.
        Program aborted.

Упс! Необходим ключ `--yes-i-know-what-i-am-doing`

```bash
$sudo hdparm -N777777777 --yes-i-know-what-i-am-doing /dev/sdb
```

        /dev/sdb:
        setting max visible sectors to 777777777 (temporary)
        max sectors   = 777777777/976773168, HPA is enabled

Отлично! Устройство поддерживает установку параметра! Ставим параметр на 
постоянный режим(ключ `p`).
```bash
$sudo hdparm -Np777777777 --yes-i-know-what-i-am-doing /dev/sdb
```
После реинициализации устройства или перезагрузки системы, Вы можете разметить и отформатировать Ваше устройство.
```bash
$sudo hdparm -I /dev/sdb | egrep 'Model Number|Serial Number|frozen|LBA48|Sector size'
```

        Model Number:       ST3500514NS                             
        Serial Number:      9WJ0HN29
        LBA48  user addressable sectors:  777777777
        Logical/Physical Sector size:           512 bytes
        not     frozen

**Low Level Format**

Необходимо установить "непустой" мастер пароль (После "безопасного стирания" пароль будет установлен назад в `NULL`). В данном случае это будет `llformat`
```bash
$sudo hdparm --user-master u --security-set-pass llformat 
```

        /dev/sdb
        security_password="llformat"

        /dev/sdb:
         Issuing SECURITY_SET_PASS command, password="llformat", user=user, mode=high


Проверяем, что режим Security стал доступен (Security level high) 
```bash
$sudo hdparm -I /dev/sdb | grep 'Security:\|Security level\|SECURITY ERASE UNIT.'
```

        Security:
                Security level high
                78min for SECURITY ERASE UNIT. 78min for ENHANCED SECURITY ERASE UNIT.


78min займет форматирование Вашего устройства.
```bash
$sudo hdparm --user-master u --security-erase llformat 
```

        /dev/sdb
        security_password="llformat"

        /dev/sdb:
         Issuing SECURITY_ERASE command, password="llformat", user=user

Ожидаем завершения операции

Проверьте, что флаг security возвращает "не включен". 
```bash
$ sudo hdparm -I /dev/sdb | grep 'Security:\|Security level'
```

        Security:


Теперь Вы можете разметить и отформатировать Ваше устройство.
