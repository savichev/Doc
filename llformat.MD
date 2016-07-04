
Ищем свое устройство (в данном случае это sdb) и удостоверяемся, что оно "не 
заморожено" (not     frozen)
```bash
$sudo hdparm -I /dev/sdb | grep 'Model Number\|Serial Number\|Firmware Revision\|frozen'
```
```
        Model Number:       ST3500514NS                             
        Serial Number:      9WJ0HN29
        Firmware Revision:  SN11    
        not     frozen
```

Если "замороженно", то пока найден один способ "разморозки" устройства, это 
посылка ОС в suspend to ram.

!!! Вывести ОС из этого состояния можно нажатием любой клавиши клавиатуры или 
мышки. !!!

```bash
$ echo mem | sudo tee /sys/power/state
```
```
mem
```
Проверяем состояние "заморозки"

```
$sudo hdparm -I /dev/sdb | grep 'Model Number\|Serial Number\|Firmware Revision\|frozen'
```

```
        Model Number:       ST3500514NS                             
        Serial Number:      9WJ0HN29
        Firmware Revision:  SN11    
        **not**     **frozen**
```
Смотрим количество используемых/доступных блоков
```
$sudo hdparm -N /dev/sdb

/dev/sdb:
 max sectors   = 976773168/976773168, HPA is disabled
```
Количество блоков 976773168. Пробуем установить 777777777 блоков.
```
$sudo hdparm -N777777777 /dev/sdb

/dev/sdb:
 setting max visible sectors to 777777777 (temporary)
Use of -Nnnnnn is VERY DANGEROUS.
You have requested reducing the apparent size of the drive.
This is a BAD idea, and can easily destroy all of the drive's contents.
Please supply the --yes-i-know-what-i-am-doing flag if you really want this.
Program aborted.
```
Упс! Необходим ключ --yes-i-know-what-i-am-doing

```
$sudo hdparm -N777777777 --yes-i-know-what-i-am-doing /dev/sdb

/dev/sdb:
 setting max visible sectors to 777777777 (temporary)
 max sectors   = 777777777/976773168, HPA is enabled
```
Отлично! Устройство поддерживает установку параметра! Ставим параметр на 
постоянный режим.
```
$sudo hdparm -Np777777777 --yes-i-know-what-i-am-doing /dev/sdb
```


!!! Low Level Format !!!


Необходимо установит временный мастер пароль(в течении сессии) отличный от NULL 
(default). В данном случае это будет llformat
```
$sudo hdparm --user-master u --security-set-pass llformat 
/dev/sdb
security_password="llformat"

/dev/sdb:
 Issuing SECURITY_SET_PASS command, password="llformat", user=user, mode=high

```
Проверяем, что режим Security стал доступен (Security level high) 
```
$sudo hdparm -I /dev/sdb | grep 'Security:\|Security level\|SECURITY ERASE 
UNIT.'
Security:
        Security level high
        78min for SECURITY ERASE UNIT. 78min for ENHANCED SECURITY ERASE UNIT.

```
78min займет форматирование Вашего устройства.
```
$sudo hdparm --user-master u --security-erase llformat 

/dev/sdb
security_password="llformat"

/dev/sdb:
 Issuing SECURITY_ERASE command, password="llformat", user=user
```
Ожидаем завершения операции

Проверьте, что флаг security возвращает "не включен". 
```
$ sudo hdparm -I /dev/sdb | grep 'Security:\|Security level'
Security:
```

Теперь Вы можете разметить и отформатировать Ваше устройство.