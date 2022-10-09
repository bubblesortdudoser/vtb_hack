# #define

### 3 branches 
* Backend
* NLP
* Rec model

## Installation

#### Requires [Python3](https://python.org/) to run.
```.sh
git clone https://github.com/bubblesortdudoser/vtb_hack.git
```

#### Install dependencies
```sh
cd vtb_hack/app
pip install -r requirements.txt
```

#### Choose your version driver of webdriver (googlechrome)
* https://omahaproxy.appspot.com/
* https://chromedriver.storage.googleapis.com/index.html
* https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Linux_x64/Branch Base Position/

#### init Database sqlite3 
```sh
./dbmanager init
```

### How Start App
## 1 - Запуск парсера. Инициализация + скрапинг новостей в полинге. Кеширование статей в бд.
```.sh
python app.py 
```

## 2 - Запуск Бота + Нейронки + Рек модель
```.sh
cd bot/
python main.py
```


