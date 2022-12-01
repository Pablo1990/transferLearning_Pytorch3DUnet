# import modules
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import shutil

try:
    shutil.rmtree(train_dir)
except OSError as exc:
    pass

try:
    shutil.rmtree(test_dir)
except OSError as exc:
    pass

os.mkdir(train_dir)
os.mkdir(test_dir)


# Split into test and train, first
train_data, test_data = train_test_split(allFileNames, test_size=0.2, random_state=1)

# Split train into train and validation
train_data, validation_data = train_test_split(train_data, test_size=0.25, random_state=1) # 0.25 x 0.8 = 0.2

# Save files onto different dirs
for train_file in train_data:
    img = io.imread(files_path + 'ImageSequence2D/' + train_file)
    io.imsave(files_path + 'ImageSequence2D_train/' + train_file, img)
    mask = io.imread(files_path + 'ImageSequence2D/' + train_file.replace('_masks', ''))
    io.imsave(files_path + 'ImageSequence2D_train/' + train_file.replace('_masks', ''), mask)
    
# Save files onto different dirs
for test_file in test_data:
    img = io.imread(files_path + 'ImageSequence2D/' + test_file)
    io.imsave(files_path + 'ImageSequence2D_test/' + test_file, img)
    mask = io.imread(files_path + 'ImageSequence2D/' + test_file.replace('_masks', ''))
    io.imsave(files_path + 'ImageSequence2D_test/' + test_file.replace('_masks', ''), mask)