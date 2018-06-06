from sklearn import preprocessing
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# X_str = [ 'media_attached', 'mature', 'mature_image', 'mature_video','image']
# X_str.append('test')
X_str = ([[ 'media_attached'], ['mature'], ['mature_image'], ['mature_video'],['image']])
X_str.append(['test'])
X_str = np.array([['a', 'dog', 'red'], ['b', 'cat', 'green'], ['test', 2, '2']])
X_str = np.array(X_str)

#X_str = np.array([['1', 'media_attached', 'True'], ['2', 'mature_image', 'True']])
X_int = LabelEncoder().fit_transform(X_str.ravel()).reshape(*X_str.shape)
X_bin = OneHotEncoder().fit_transform(X_int).toarray()

print(X_bin)

import pandas as pd
s = pd.Series(list('abca'))
print(pd.get_dummies(pd.Series(X_str)))
