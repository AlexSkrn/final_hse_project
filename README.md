# Проект по компьютерной лингвистике для Вышки

## Программа для упражнений по переводу с английского на русский

Идея состоит в том, чтобы попытаться придать интерактивности пассивным учебным
материалам -- например, можно отсканировать из учебника примеры на перевод, загрузить
их в компьютерную программу и получать обратную связь в виде подсказок и оценок
соответствия между переводом, предложенным пользователем, и переводом-ориентиром
из учебника.

В рамках этого проекта я беру корпус параллельных предложений, кластеризую их
на темы и загружаю в написанную для этого компьютерную программу.
```
    Пользователь           +--------------------------------+
    выбирает тему          | Список тем                     |
    из имеющихся           |                                |
    в программе            +--------------------------------+

    Программа              +--------------------------------+
    выдает предложение     | Sentence to translate.         |
    на перевод             +--------------------------------+

    Пользователь           +--------------------------------+
    вписывает              | Мой перевод предложения.       |
    свой перевод           +--------------------------------+

    Программа оценивает    +--------------------------------+    Одно слово лишнее,
    % совпадений и         | (46%) Предложение --- перевода.|    одно не угадано,
    дает подсказку         +--------------------------------+    неправильный порядок
```
## Корпус параллельных предложений

- Корпус параллельных предложений WikiMatrix. Состоит из автоматически выровненных
предложений из статей Википедии. ~500 тыс. предложений


- Удаление строк, содержащих шрифты, отличные от кириллицы и латиницы.
Корпус уменьшился с ~500 тыс. предложений до ~440 тыс.
```
最弱と呼ばれても...岩谷麻優、いつか見つける青い鳥.
最弱と呼ばれても...岩谷麻優、いつか見つける青い鳥 (яп.) (недоступная ссылка).

ם becomes מ when it is not the final letter.
ם становится מ, когда это не последняя буква.

ניפגש בכיכר .
Экспозиция на площадке.

תשתו משהו?
Будешь пить?
```

- Удаление непереведенных или почти непереведенных предложений с помощью функции
__сходства Джаро__ из библиотеки __NLTK__. Для следующего примера сходство Джаро 0.87.
Корпус уменьшился с ~440 тыс. предложений до ~340 тыс.
```
""Aphrodite" finally hits stores in the US today!".
«Aphrodite» finally hits stores in the US today! (англ.) (недоступная ссылка).
```
## Кластеризация корпуса

- Дальше я попытался кластеризовать англоязычную часть корпуса с помощью метода
__KMeans__ из библиотеки __sklearn__

- Для этого:
  (1) лемматизировал корпус с помощью библиотеки __Spacy__. При этом я
оставил только следующие части речи -- ['PROPN', 'VERB', 'NOUN', 'ADJ']
  (2) использовал стоп-слова из NLTK
  (3) TfidfVectorizer c би-граммами и три-граммами

- Кластеризация приводит к тому, что почти все предложения помещаются в один
огромный кластер, а остальные предложения образуют большое количество
очень мелких кластеров

- Выбрал несколько осмысленных кластеров
```
World Wars      1550  
Russia           845 (объединил из кластеров 'USSR' и 'Russia, Saint-Petersburg')
Human rights     381
Politics         284
Copyright        231 (включает кластер 'Intellectual Property')
Arab world       212
Medical           88 (включает кластер 'Human genome')
Vatican           54
```

- Ключевые n-граммы из первого и последнего кластеров

```
world war, war ii, world war ii, second world war, second world,
first world, first world war, united states, end world war, end world,
outbreak world, outbreak world war, follow world war, follow world,
start world, end second world, end second, beginning world war,
beginning world, civil war, german occupation, end first, war world war,
war world, war break, prisoner war, united kingdom, post war, use world, soviet union

pope john, john paul, paul ii, john paul ii, pope john paul, cultural center,
united states, catholic church, remain loyal, make similar, pope benedict xvi,
benedict xvi, pope benedict, france italy, need new, new generation,
northern france, lose position, new delhi, roman curia, serious threat,
film festival, publish article, make official, become close, different country,
work complete, ukrainian greek, great importance, year perform
```
## Программа для оценки перевода и выдачи подсказок

Оценка соответствия перевода пользователя переводу-ориентиру -- коэффициентом __BLEU-2__.
Коэффициент BLEU-2 определяется с помощью функции из библиотеки NLTK. Оценка учитывает
порядок слов (совпадение биграмм) и длину перевода. Форма слова и пунктуация на оценку не влияет.
Перевод, предложенный пользователем, и перевод-ориентир лемматизируются с помощью __pymystem3__.

![Screenshot](/images/Screenshot.png)

## Как установить программу на своем компьютере

В командной строке на Маке:
```
$ git clone https://github.com/AlexSkrn/final_hse_project.git
$ python -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install final_hse_project/packages/question_game/
(.venv) $ pip install final_hse_project/packages/app_question_game/
(.venv) $ cd final_hse_project/packages/app_question_game/app_question_game
(.venv) $ flask run
```
Наберите в браузере: ```http://127.0.0.1:5000/```

Чтобы остановить сервер, в командной строке: ```CTRL+C```

Деактивировать виртуальное окружение: ```(.venv) $ deactivate```

## Как все это удалить

В терминале сначала вернитесь в директорию, в которую клонирован
этот проект из Гитхаба, а затем:
```
$ ls -a                      # убедитесь, что Вы в нужной директории
.			final_hse_project      # содержимое должно быть примерно таким
..			.venv

$ rm -rf .venv
$ rm -rf final_hse_project
```

## Для Windows

То же самое, если предварительно установлен терминал Git Bash.

Но, вместо $ source .venv/bin/activate должно быть $ source .venv/Scripts/activate

## pymystem3

Один из используемых пакетов, pymystem3, при первом использовании сохраняет
файл mystem.exe вот здесь: ```C:/Users/username/.local/bin/mystem.exe```

В Маке это можно найти тут: ```~/.local/bin/mystem```
