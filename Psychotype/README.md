# Описание проекта
В данном репозитории представлены две прогностические модели для определения психотипа по методике MBTI.
Данные были взяты с сайта [www.kaggle.com](https://www.kaggle.com/). 
1. Работа [Psychotypes_Prediction142questions](https://github.com/Playmen998/Data_Analysis/blob/master/Psychotype/Psychotypes_Prediction142questions.ipynb) 
представляет собой анализ ответов респондентов на тест MBTI собранных на сайте [KeyHabits](https://keyhabits.ru/). 
Особенностью датасета является **большое кол-во колонок с вопросами 142**, а также **кол-во наблюдений 21 846**.
Данный датасет можно найти по этой [ссылке](https://www.kaggle.com/datasets/pmenshih/kpmi-mbti-mod-test)
2. В работе [Psychotypes_Prediction60questions](https://github.com/Playmen998/Data_Analysis/blob/master/Psychotype/Psychotypes_Prediction60questions.ipynb) 
был проведен анализ ответов респондетов на измененный от оригинального тест (MBTI) под названием KPMI. Ответы были собраны на сайте [kpmi.ru](https://kpmi.ru/)
Особенностью датасета является **умеренное кол-во колонок с вопросами 60**, а также **кол-во наблюдений 100 000**.
Данный датасет можно найти по этой [ссылке](https://www.kaggle.com/datasets/pmenshih/kpmiru-questionnaires-data)

Модель будет использована в проекте телеграмм бота [Psychotype_Bot](https://github.com/Playmen998/Psychotype_Bot). 
Этот бот является тестом на определение психотипа. В результате которого, модель в зависимости от полученных ответов от респондентов будет предсказывать психотип и давать к нему описание.
# Особенности проекта
Главной особенностью проекта является использование мультиклассовой классификации при построение прогностической модели определения психотипа. 
По методологии теста MBTI существует 16 различных психотипов, которые мне необходимо предсказать. 

Использованный стек технологий:
Pandas, Numpy, Seaborn, Matplotlib, Sklearn, Catboost, Hyperopt, Hvplot

Также стоит сказать о ключевых/сложных написаных методов: 
+ по подсчету average_precision_score для каждого класса
+ обработка данных и отображение графиков average_precision_score для каждого класса (*к сожалению в репозитории GitHub они не отображаются*)
+ построение матрицы ошибок для мультиклассовой классификации

# Задачи проекта
1. Анализ и первичная обработка данных
2. Построение прогностической модели для обоих датасетов
3. Определить разницу в полученных результатах

# Результаты
Для данного проекта я выбрал ключевую метрику **Precision** т.к. мне важно, чтобы модель предсказывала *как можно точно* психотипы.
В качестве вспомогательных метрик были использованы: Accuracy, F1, average_precision_score.
Для финальных моделей в 60 вопросов [Psychotypes_Prediction60questions](https://github.com/Playmen998/Data_Analysis/blob/master/Psychotype/Psychotypes_Prediction60questions.ipynb) 
и 142 вопроса [Psychotypes_Prediction142questions](https://github.com/Playmen998/Data_Analysis/blob/master/Psychotype/Psychotypes_Prediction142questions.ipynb) был
получен средний Precision по всем классам **равным 87%**, причем для всех остальных метрик для каждой модели значения практически одинаковы.
Т.к. в точности предсказания нет разницы, то для проекта телеграмм бота [Psychotype_Bot](https://github.com/Playmen998/Psychotype_Bot) я возьму модель в которой 60 вопросов, потому что
для пользователей это является оптимальным кол-во вопросов, чтобы они завершили тест (*142 вопроса слишком много, не все пользователи пройдут тест до конца*)
Однако, мы терям в робастности нашего теста т.к. в случае неоднозначного выбора ответа на вопрос
>Какое слово в паре «факты - идеи» тебе больше нравится по смыслу?
>
>A) факты
>
>B) идеи
>>В данном вопросе проблематично  выбрать понравившиеся слово

Модель может предсказать разные психотипы в зависимости от ответа на один вопрос. В случае модели на 142 вопроса, чтобы модель явно предсказывала ожидаемый психотип 
надо выбрать несколько определенных ответов на вопросы, чтобы получить ожидаемый предсказанный психотип

# Используемые технологии
*pandas*, *numpy*, *seaborn*, *matplotlib*, *sklearn-learn*, *catboost*, *hyperopt*, *hvplot*
