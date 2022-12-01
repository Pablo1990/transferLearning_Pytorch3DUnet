# import modules
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import shutil

def raw_parameters(rawFilePath):
    '''Obtain raw image parameters: zSpacing, xResolution and yResolution from TIFF'''
    
    rawImg = tiff.TiffFile(rawFilePath);
    try:
        zSpacing = rawImg.imagej_metadata['spacing'];
    except Exception as e:
        zSpacing = 1;
    
    if rawImg.imagej_metadata['unit'] == 'micron':
        measurementsInMicrons = True;
        
    rawImg = Image.open(rawFilePath)
    
    if TAGS[282] == 'XResolution':
        xResolution = 1/rawImg.tag_v2[282];
        
    if TAGS[283] == 'YResolution':
        yResolution = 1/rawImg.tag_v2[283];
        
    if measurementsInMicrons:
        #To nanometers
        zSpacing=zSpacing*1000;
        xResolution=xResolution*1000;
        yResolution=yResolution*1000;

def load_raw_seg_images(rawFilePath, segFilePath, resize_img=True):
    '''Read segmented image to remove first biggest label and obtain list of cell properties'''
    
    if rawFilePath.endswith('tif') or rawFilePath.endswith('tiff'):
        rawImg = io.imread(rawFilePath)
        segmentedImg = io.imread(segFilePath)
    
    if rawFilePath.endswith('h5'):
        rawImgh5 = h5py.File(rawFilePath, 'r')
        rawImg = np.array(rawImgh5.get('raw'))

        segmentedImgh5 = h5py.File(segFilePath, 'r')
        segmentedImg = np.array(segmentedImgh5.get('label'))
        
    segmentedImg = segmentedImg - 1;
    
    if resize_img == True:
            rawImg = transform.resize(rawImg, (rawImg.shape[0], 512, 512),
                            order=0, preserve_range=True, anti_aliasing=False).astype(np.uint32)
            segmentedImg = transform.resize(segmentedImg, (segmentedImg.shape[0], 512, 512),
                                  order=0, preserve_range=True, anti_aliasing=False).astype(np.uint32)  
    #uniqueIds=np.unique(segmentedImg)
    #maxId = uniqueIds.max()
     
    #props = measure.regionprops(segmentedImg)

    return rawImg, segmentedImg

def save_hdf5(segFilePath):
    '''Saves postprocessed image as HDF5'''
    
    postProcessFilePath = segFilePath.rstrip('predictions_gasp_average.h5') 
    postProcessFilePath += '_postprocessed.h5'
    postProcessFile = h5py.File(postProcessFilePath, "w")
    segmentation = postProcessFile.create_dataset("label", data=watershedImg, dtype='uint16')
    
    #If properties from TIFF (need to add into function argument)
    segmentation.attrs['zSpacing'] = zSpacing
    segmentation.attrs['xResolution'] = [xResolution.numerator,xResolution.denominator]
    segmentation.attrs['yResolution'] = [yResolution.numerator,yResolution.denominator]
    
    postProcessFile.close()

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

try:
    os.mkdir(files_path + 'ImageSequence2D/')
except OSError as exc:
    print('Dir exists')

for currentDir in inputDir:
    print(currentDir)
    for root, subdirs, files in os.walk(currentDir):
        for filename in files:
            if filename.endswith('.tif'):
                img = io.imread(root + '/' + filename)


# Split into validation and test, first
train_data, test_data = train_test_split(allFileNames, test_size=0.2, random_state=1)

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