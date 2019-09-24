# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12e1QmM9MGfPcYlweDqmNrscUWvo8AvC8
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

import tensorflow_datasets.public_api as tfds

import os
import glob
import nibabel as nib
import re 


import tensorflow_datasets.public_api as tfds

_DESCRIPTION = """\
The dataset is used to evaluate automatic algorithms on segmentation of organs-at-risk (OAR)

is to set up tasks for evaluating automatic algorithms on segmentation of organs-at-risk (OAR) and gross target volume (GTV) of tumors of two types of cancers, nasopharynx cancer and lung cancer, for radiation therapy planning. There are four tasks for evaluating the performance of the algorithms. Participants can choose to join one or all tasks according to their interests. 
"""
_BASE_URL = """https://structseg2019.grand-challenge.org/"""
_CITATION = """  XXXX """



class Structuresegmentation(tfds.core.GeneratorBasedBuilder):
  """Short description of my dataset."""

  SKIP_REGISTERING = True  
  VERSION = tfds.core.Version("1.0.0",
                              experiments={tfds.core.Experiment.S3: False})
  SUPPORTED_VERSIONS = [
      tfds.core.Version("2.0.0"),
  ]
    
  
  def _info(self):
    # Specifies the tfds.core.DatasetInfo object
    return tfds.core.DatasetInfo(
      builder=self,
      description=_DESCRIPTION,
      features=tfds.features.FeaturesDict({
          "image": tfds.features.Image(shape=(512, 512, 1)),
          "label": tfds.features.Image(shape=(512, 512, 1)),
      }),
      supervised_keys=("image", "label"),
      urls=[_BASE_URL],
      citation=_CITATION,
    )
  

  def _split_generators(self, dl_manager):
    # Equivalent to dl_manager.extract(dl_manager.download(urls))
    #file_name = download.dl_manager.download_and_extract('/content/drive/My Drive/Task1_HaN_OAR.zip')
    path = os.path.join(dl_manager.manual_dir, 'HaN_OAR') 

    if not tf.io.gfile.exists(path):
      raise AssertionError('You must download the dataset manually from {}, ''extract it, and place it in {}.'.format( _BASE_URL, dl_manager.manual_dir)) 
    # There is no predefined train/val/test split for this dataset.
    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            num_shards=1,
            gen_kwargs=dict(filepath = path)), #zip file location
    ]  

  
  
  
  def _generate_examples(self,filepath):
    """Generate examples for the StructSeg dataset.
    Args:
      filepath: path to the StructSeg file.
    Yields:
      Dictionaries with images and labels.
    """
    #the path is /folder/folder/file   e.g./content/HaN_OAR/1/data.nii.gz
    #    archive_path = "/content/drive/My Drive/Task1_HaN_OAR.zip"

    #     with zipfile.ZipFile(filepath, 'r') as zip: 
    #       zip.extractall() 
    file_path = filepath  #hard-code, need change
    
    
    dirs = get_all_file_paths(file_path)

    label_dirs = []
    data_dirs = []

    #separte the directory paths into label subdir and data subdir

    for dir in dirs:
        if dir.endswith("/label.nii.gz"): 
          label_dirs.append(dir)
        else:
          data_dirs.append(dir)

    #get index_list from label_dirs
    index_list = []

    for dir_name in label_dirs:
      index_ = re.search("(?<=HaN_OAR\/)(\d+)\/",dir_name)
      index_list.append(index_.group(1))


    for index,label_dir, data_dir in zip(index_list,label_dirs, data_dirs) :
      label_temp = nib.load(label_dir)
      data_temp = nib.load(data_dir)
      label_array = label_temp.get_fdata()
      data_array = data_temp.get_fdata()

      for slice in range(144):
        new_index = index *144 +slice
        record = {
            "image": data_array[:,:,slice],
            "label": label_array[:,:,slice]
        }
    yield new_index, record    
    
    

  def get_all_file_paths(directory): 

      # initializing empty file paths list 
      file_paths = [] 

      # crawling through directory and subdirectories 
      for root, directories, files in os.walk(directory): 
          for filename in files: 
              # join the two strings in order to form the full filepath. 
              filepath = os.path.join(root, filename) 
              file_paths.append(filepath) 

      # returning all file paths 
      return file_paths
