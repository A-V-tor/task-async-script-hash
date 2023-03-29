## Тестовое задание:

- Напишите скрипт, асинхронно, в 3 одновременных задачи, скачивающий содержимое HEAD репозитория https://gitea.radium.group/radium/project-configuration во временную папку.
- После выполнения всех асинхронных задач скрипт должен посчитать sha256 хэши от каждого файла.
- Код должен проходить без замечаний проверку линтером wemake-python-styleguide. Конфигурация nitpick - https://gitea.radium.group/radium/project-configuration
- Обязательно 100% покрытие тестами

<h1 align="center">Развертывание проекта</h1>

<h2>Скачать проект</h2>

```
  git clone git@github.com:A-V-tor/task-async-script-hash.git
```

```
  cd task-async-script-hash
```

<h2> Создать виртуальное окружение и установить зависимости</h2>

```
    python3 -m venv venv
    source venv/bin/activate
    
```
`python3 -m pip install -r requirements.txt` </br> </br>
Или в случае использования <b>poetry</b>


```
    poetry shell
    
```

`poetry install`
</br></br>
<h2> Открыть файл main.py</h2>

```
  cd async_script_hash
  python -i main.py
```
<h2>Вызвать функцию</h2>

```
  asyncio.run(main())
```

<h1 align="center">Тесты</h1>
<h2> В корне проекта</h2>

```
  pytest run --cov
```

<img src="https://github.com/A-V-tor/task-async-script-hash/blob/main/image.jpeg">
