# Лабораторна робота №7

## Тема

Хмарне розгортання DevOps-сервісу

---

## Мета роботи

- Навчитися виконувати deployment програмного сервісу у хмарному середовищі.

- Ознайомитися з безкоштовними cloud-платформами для DevOps.

- Забезпечити публічний доступ до API-сервісу через HTTPS URL.

- Підготувати основу для наступної лабораторної роботи з DevSecOps та безпеки контейнерів.

---

## Модель

Оптимізація енергоспоживання готелю з використанням генетичних алгоритмів (5 семестр)

---

## Опис роботи

У лабораторній роботі №7 було використано проєкт з лабораторної роботи №6, у якому вже було реалізовано CI/CD pipeline для API-сервісу. Програмний сервіс створено на основі Flask та розміщено у Docker-контейнері.

Для хмарного розгортання було обрано платформу Render. За допомогою Render було виконано deployment Docker-контейнера з API-сервісом, отримано публічний HTTPS URL та перевірено роботу endpoint `/calculate`.

---

## Структура проєкту

Проєкт має таку структуру:

```text
lab7_devops/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── hotel-energy-ga/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
└── README.md
```

<img width="942" height="186" alt="image" src="https://github.com/user-attachments/assets/070c467e-cfd3-4b33-b512-6f084924d2d0" />

---

## Використання проєкту з ЛР6

У якості основи для лабораторної роботи №7 було використано проєкт з ЛР6. У ньому вже був налаштований CI/CD pipeline за допомогою GitHub Actions.

Pipeline виконує такі етапи:

1. клонування репозиторію;
2. налаштування Python 3.11;
3. встановлення залежностей з `requirements.txt`;
4. перевірку синтаксису Python-файлу `app.py`;
5. автоматичну збірку Docker image.

<img width="1314" height="223" alt="image" src="https://github.com/user-attachments/assets/9365d614-ec37-411b-a450-f2e105a7832c" />

<img width="586" height="993" alt="image" src="https://github.com/user-attachments/assets/b74ab688-b99d-48eb-a10a-91a15115c980" />

---

## Файл Dockerfile

Для контейнеризації API-сервісу використано Dockerfile, розміщений у папці `hotel-energy-ga`.

Вміст Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

У цьому файлі використано базовий образ `python:3.11-slim`, створено робочу директорію `/app`, встановлено залежності з `requirements.txt`, скопійовано файл `app.py`, відкрито порт 5000 та задано команду запуску застосунку.

<img width="572" height="470" alt="image" src="https://github.com/user-attachments/assets/8b8aa848-b3e8-427c-b446-ff5748761510" />

---

## Файл requirements.txt

У файлі `requirements.txt` вказано залежність, необхідну для роботи API-сервісу:

```text
flask
```

Flask використовується для створення HTTP API та обробки запитів до endpoint `/calculate`.

<img width="620" height="236" alt="image" src="https://github.com/user-attachments/assets/844810eb-bee8-498e-a109-50dbb439d7d4" />

---

## Опис API-сервісу

API-сервіс реалізовано у файлі `app.py`. У коді описано модель оптимізації енергоспоживання готелю з використанням генетичного алгоритму.

Сервіс працює з набором пристроїв готелю, серед яких:

- освітлення номерів;
- освітлення коридорів;
- кондиціонування;
- кухонне обладнання;
- пральня;
- ліфт;
- серверна;
- мультимедійні системи.

Для кожного пристрою задано потужність, критичність та показник комфорту. Генетичний алгоритм підбирає оптимальний набір увімкнених і вимкнених пристроїв з урахуванням обмеження за максимальною потужністю.

Основний endpoint сервісу:

```text
/calculate
```

Також можна передати параметр `max_power`:

```text
/calculate?max_power=70
```

<img width="577" height="603" alt="image" src="https://github.com/user-attachments/assets/6fc786cd-a747-4dc4-8d6b-503fe87215c8" />

---

## Підготовка сервісу до хмарного розгортання

Для виконання вимог лабораторної роботи сервіс було підготовлено до подальшої перевірки безпеки.

У коді було виконано такі зміни:

* вимкнено debug mode;
* не використовуються паролі або секретні ключі в коді;
* використано environment variables;
* порт застосунку отримується через змінну середовища `PORT`;
* значення `DEFAULT_MAX_POWER` задається через environment variable.

Фрагмент коду:

```python
default_max_power = int(os.environ.get('DEFAULT_MAX_POWER', 70))
max_power = int(request.args.get('max_power', default_max_power))
```

Фрагмент запуску застосунку:

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

---

## Створення Web Service на Render

Для хмарного deployment було використано платформу Render. На платформі було створено новий Web Service.

Під час створення сервісу було обрано:

```text
New → Web Service
```

Після цього було підключено GitHub-репозиторій:

```text
https://github.com/MarselaBiak/lab7_devops.git
```

<img width="434" height="783" alt="image" src="https://github.com/user-attachments/assets/383d0b76-8fc3-445a-b8b5-eda19f6ca640" />

<img width="1894" height="324" alt="image" src="https://github.com/user-attachments/assets/78f831a0-d5e9-4302-9bba-bd9ac5921294" />

---

## Налаштування Web Service

Після підключення репозиторію було виконано налаштування нового Web Service.

Основні параметри:

```text
Name: hotel-energy-ga
Language: Docker
Branch: main
Region: Oregon
Root Directory: hotel-energy-ga
```

---

## Environment Variables

Для виконання вимоги щодо використання environment variables на Render було додано змінну середовища:

```text
DEFAULT_MAX_POWER = 70
```

Ця змінна використовується у коді як значення максимальної потужності за замовчуванням, якщо параметр `max_power` не передано у запиті.

---

## Deployment сервісу

Після налаштування Web Service було запущено deployment. Render автоматично зібрав Docker-контейнер і запустив API-сервіс у хмарному середовищі.

У результаті сервіс отримав статус:

```text
Live
```

Також було отримано публічний HTTPS URL:

```text
https://hotel-energy-ga.onrender.com
```

<img width="712" height="232" alt="image" src="https://github.com/user-attachments/assets/841f52bb-d182-4162-b475-2e61ee1cf635" />

---

## Перевірка роботи endpoint

Для перевірки роботи API-сервісу було відкрито endpoint:

```text
https://hotel-energy-ga.onrender.com/calculate?max_power=70
```

У результаті сервіс успішно повернув JSON-відповідь.

Отримана відповідь підтверджує, що API-сервіс успішно працює у хмарному середовищі. Значення `max_power` дорівнює 70, а знайдене загальне енергоспоживання становить 69, тобто не перевищує задане обмеження.

<img width="556" height="785" alt="image" src="https://github.com/user-attachments/assets/7bd6df3f-4933-4e7a-b03d-f0929b2b4c53" />

---

## Висновок

У ході виконання лабораторної роботи №7 було виконано хмарне розгортання DevOps-сервісу. Для цього використано проєкт з ЛР6, який містить Flask API, Dockerfile та CI/CD pipeline. Сервіс було розгорнуто на платформі Render як Docker Web Service.

Після deployment було отримано публічний HTTPS URL та перевірено роботу endpoint `/calculate`. API успішно повертає JSON-відповідь з результатами оптимізації енергоспоживання готелю. Також сервіс було підготовлено до подальшої перевірки безпеки: debug mode вимкнено, секретні дані в коді не зберігаються, а налаштування винесено в environment variables.
