import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier
from catboost import Pool
from sklearn import metrics

df = pd.read_csv(r'Table/kpmi_ru_data.csv', low_memory=False)

df_pred = df.drop(['e','i', 's', 'n', 't', 'f', 'j', 'p'], axis = 1)
df_pred = df_pred.drop(list(df_pred.filter(regex='t')), axis = 1).copy()
df_pred = df_pred.iloc[:, :60]
df_pred['psychotype'] = df['psychotype']
df_pred = df_pred.replace([1,2],[0,1])


X_train, X_test, y_train, y_test = train_test_split(df_pred.iloc[:,:-1], df_pred.iloc[:,-1],
                                                    test_size=0.2,random_state=42, stratify = df_pred['psychotype'])
X_test, X_val, y_test, y_val = train_test_split(X_test, y_test, train_size=0.5,
                                                random_state=42, stratify = y_test)



X = list(df_pred.iloc[:,:-1].columns)
y = 'psychotype'

train_data = Pool(data=X_train,
                  label=y_train
                 )
val_data = Pool(data = X_val,
               label = y_val)

params = {'verbose' : 200,
              'random_seed':42,
              'depth': 3,
              'l2_leaf_reg': 1,
              'learning_rate': 0.4629992499592749,
              "loss_function" : 'MultiClass'}

X_train_val = pd.concat([X_train,X_val],axis = 0)

y_train_val = pd.concat([y_train,y_val],axis = 0)

train_val_data = Pool(data=X_train_val,
                  label=y_train_val
                 )

model = CatBoostClassifier(**params)

model.fit(train_data, eval_set = val_data)

"____Находим вероятность для каждого психотипа____"

test_pred = model.predict(X_test)
labels = y_test.unique()
cm = metrics.confusion_matrix(y_test, test_pred, labels = list(labels))
precision = np.diag(cm) / np.sum(cm, axis = 0)
precision_finall = []
[precision_finall.append(int(round(i * 100, 0))) for i in list(precision)]


df_precision = pd.DataFrame({'labels':list(labels), 'precision' : precision_finall})

def prediction(result):
    global df_precision
    list_pred = []
    for i in result:
        if i == 'A':
            list_pred.append(0)
        else:
            list_pred.append(1)
    result = model.predict(list_pred)
    precision = df_precision[df_precision['labels'] == result[0]]["precision"].values[0]
    return result, precision
