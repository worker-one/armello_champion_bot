## Armello Telegram Bot

## Введение

Это документация для бота Armello @armello_bot.

## Управление работой бота

Управление работй бота выполняется через панель http://159.89.3.192:8000/ui/services/armello_bot

- Запуск

- Остановка
  
- Перезапуск
  
- Проверка статуса

Доступ предоставляется через API ключ.

Для администратора доступны следующие команды:

- `/update` : обновить статистику на основе данных матчей.
  
- `/customtitle` : управление кастомными титулами.
  
- `/deny <match_id>` : обнуление матча по его id.

## Управление базой данных

Управление базой данных выполняется через DBeaver. 

### Создание копии базы данных (бэкап)

1. Выбрать базу данных, кликнуть правой кнопкой мыши.

2. Выбрать Tools

3. Выбрать Backup

![image](https://github.com/user-attachments/assets/b3a8d25e-9260-48b5-9d98-e27b7a06999b)

В первом диаологом окне вы выбираете таблицы для экспорта. Во-втором окне вы выбераете расположение на вашем компьютере для сохранения бэкапа.

![image](https://github.com/user-attachments/assets/9a472826-a5a5-4f5f-ae32-942b1b659513)

Как только вы закончили конфигурацию экспорта, вы нажимаете "Start". В случае успеха, копия базы данных сохранится в указанном месте с расширением `.sql`. Далее, вы можете использовать этот файл для восстановления базы данных.

### Установка существующего содержания базы данных (бэкапа)

1. Выбрать базу данных, кликнуть правой кнопкой мыши.

2. Выбрать Tools

3. Выбрать Restore

![image](https://github.com/user-attachments/assets/ca416606-30d2-4602-92f0-b54a1753c40e)

В диалоговом окне выберите расположение вашего файла с бэкапом. Далее нажмите "Start".

![image](https://github.com/user-attachments/assets/93bf64df-9de8-43c9-af43-decc95e9abd1)

После завершения процесса, база данных будет обновлена. Для просмотра новой версии базы данных обновите состояние через кнопку "Refresh"

### Удаление (вайп) базы данных

1. Выделите таблицы, которые нужно вайпнуть (все таблицы отвечающие за статистику: `matches` и `match_participants`)

2. Кликнуть правой кнопкой мыши, выбрать Tools -> Truncate

![image](https://github.com/user-attachments/assets/0fd37394-8a66-431a-b064-a697ea4d46f0)

3. Выделить "Cascade"

4. Нажать Proceed

![image](https://github.com/user-attachments/assets/fdcc4f8c-6bfd-4ed0-b495-8b101e874565)

5. Для построения новых рейтингов и титулов прописать в боте команду `/update`



