![Turd-Rex](assets/textures/gif_demo.gif)

Клон игры про динозаврика... но с новыми механиками.

# Запуск

Сделать копию config-example.yml:

```shell
cp config-example.yml config.yml
```

В папке с игрой создать и активировать venv:
```shell
python3 -m venv ./

source ./bin/activate

pip install -r requirements.txt
```

Запустить через main.py:
```shell
python3 main.py
```

# Использование multitool.py для генерации новых объектов и обработчиков

## Объект

```shell
python multitool.py make:object <NAME> [OPTIONS]
```

**Аргументы**
- `<NAME>`: Название нового класса.

Название файла будет сгенерировано в snake_case из названия нового класса. Новый класс будет добавлен в `__init__.py`.

**Опции**
- `--parent <PARENTS>`: Родительский класс (или классы через запятую). По умолчанию `Object`.
- `--handler <HANDLER>`: Название класса обработчика. По умолчанию не подставляется (`None`).
- `--make-handler <PARENT_HANDLERS>`: Создать класс обработчика `КлассОбъекта + Handler`. Через запятую можно перечислить дополнительные родительские классы помимо `ObjectHandler`. 

## Обработчик

```shell
python multitool.py make:handler <TARGET> [OPTIONS]
```

**Аргументы**
- `<TARGET>`: Класс объекта, которым управляет обработчик.

Название файла будет сгенерировано в snake_case из названия нового класса. Новый класс будет добавлен в `__init__.py`.

**Опции**
- `--parent <PARENTS>`: Родительский класс (или классы через запятую). По умолчанию `ObjectHandler`.