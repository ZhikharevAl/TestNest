# Тест-кейс: Добавление нового клиента с генерированными данными

## Описание
Проверка функциональности добавления нового клиента в систему XYZ Bank с использованием специально сгенерированных данных для полей Post Code и First Name.

## Предусловия
1. Открыт веб-браузер.
2. Пользователь авторизован в системе XYZ Bank с правами менеджера.
3. Открыта страница "Добавление нового клиента".

## Шаги выполнения
1. Сгенерировать тестовые данные:
    - Post Code: 10-значное число
    - First Name: на основе Post Code (см. алгоритм ниже)
    - Last Name: случайная строка

2. В поле "Post Code" ввести сгенерированный 10-значный номер.

3. В поле "First Name" ввести сгенерированное имя.

4. В поле "Last Name" ввести сгенерированную фамилию.

5. Нажать кнопку "Добавить клиента".

6. Проверить появление всплывающего окна с сообщением об успешном добавлении клиента.

7. Принять всплывающее окно.

## Ожидаемый результат
- Клиент успешно добавлен в систему.
- Отображается сообщение об успешном добавлении клиента.
- Данные клиента соответствуют введенным.

## Алгоритм генерации First Name
1. Разделить Post Code на 5 двузначных чисел.
2. Преобразовать каждое двузначное число в букву английского алфавита:
    - Числа от 0 до 25 соответствуют буквам от 'a' до 'z'.
    - Числа 26 и более преобразуются по модулю 26 (т.е. 26 → 0, 27 → 1, и т.д.).
3. Объединить полученные буквы в одно слово.

### Пример
Post Code: 0001252667
First Name: abzap

## Постусловия
1. Убедиться, что новый клиент отображается в списке клиентов.
2. Проверить, что все данные клиента сохранены корректно.

## Дополнительная информация
- Тест должен быть выполнен для различных комбинаций Post Code, включая граничные значения (например, все нули, все девятки).
- Убедиться, что система корректно обрабатывает Post Code с повторяющимися цифрами и First Name с повторяющимися буквами.

## Критерии приемки
- Тест считается успешным, если клиент добавлен с корректно сгенерированными данными.
- Система должна корректно обрабатывать все возможные комбинации Post Code и генерировать соответствующие First Name.