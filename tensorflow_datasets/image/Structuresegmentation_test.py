# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b6KmHiUca5z73tQ-lYcGGHjpTpn8MCMb
"""

import tensorflow as tf
from tensorflow_datasets import Structuresegmentation
import tensorflow_datasets.testing as tfds_test


class MyDatasetTest(tfds_test.DatasetBuilderTestCase):
  DATASET_CLASS = Structuresegmentation.Structuresegmentation
  SPLITS = {  # Expected number of examples on each split from fake example.
      "train": 7200,
  }
  # If dataset `download_and_extract`s more than one resource:
  DL_EXTRACT_RESULT = {
      "name1": "/content/HaN_OAR"  # Relative to fake_examples/my_dataset dir.
  }

if __name__ == "__main__":
  tfds_test.test_main()