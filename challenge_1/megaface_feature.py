#!/usr/bin/env python
# coding-utf-8

import os
import sys
import cv2
import json
import numpy as np
from align import FaceAligned
from mtcnn import CNN
from matio import *

# generate megaface feature
MEGAFACE_PATH = os.path.join('..','..','MegaFace_dataset')
MEGAFACE_CROP_PATH = os.path.join('..','..','MegaFace-crop')
MEGAFACE_ALIGN_PATH = os.path.join('..','..','MegaFace-align')
MEGAFACE_FEATURE_PATH = os.path.join('..','..','MegaFace-feature')
MEGAFACE_LIST = os.path.join('..','templatelists','megaface_features_list.json_1000_1')
MEGAFACE_ALIGN_LIST = os.path.join('..','resultlists','megaface_aligned_list.json_1000_1')

BATCH_SIZE = 100 # for cnn forward

if not os.path.exists(MEGAFACE_ALIGN_PATH):
  os.makedirs(MEGAFACE_ALIGN_PATH)

if not os.path.exists(MEGAFACE_FEATURE_PATH):
  os.makedirs(MEGAFACE_FEATURE_PATH)

class megaface():
  def __init__(self):
    self.align = FaceAligned()
    self.cnn = CNN()
    self.logFile = open('./megaface_warning.log', 'w+')

  def megaface_align(self, megaface_path = MEGAFACE_PATH,
                     megaface_crop_path = MEGAFACE_CROP_PATH,
                     align_path_to_save = MEGAFACE_ALIGN_PATH,
                     megaface_list = MEGAFACE_LIST,
                     megaface_align_list = MEGAFACE_ALIGN_LIST,
                     save_ext = '.png'):
    with open(megaface_list) as fp:
      megafaceFile = json.load(fp)
      path_list = megafaceFile["path"]
      alignFile = {}
      path_save_list = []
      for i in range(len(path_list)):
        path = os.path.join(megaface_path, path_list[i])
        im_align = self.align.aligned(str(path))
        """
        # if align origin image failed try crop image
        if im_align is None:
          print >> self.logFile, "%s align failed" %(path)
          path_crop = os.path.join(probe_crop_path, path_list[i])
          im_align = self.align.aligned(path_crop)
        """
        # if align crop image failed use resize image
        if im_align is None:
          print >> self.logFile, "%s align failed, use resize image" %(path)
          im = cv2.imread(path)
          im_align = cv2.resize(im, (96, 112))
          print im_align.shape
        path_temp = os.path.join(align_path_to_save, path_list[i])
        p,f = os.path.split(path_temp)
        if not os.path.exists(p):
          os.makedirs(p)
        path_save = os.path.splitext(path_temp)[0] + save_ext
        cv2.imwrite(path_save, im_align)
        path_save_list.append(os.path.splitext(path_list[i])[0] + save_ext)
      # save aligned list file
      alignFile["path"] = path_save_list
      p,f = os.path.split(megaface_align_list)
      if not os.path.exists(p):
        os.makedirs(p)
      json.dump(alignFile, open(megaface_align_list, 'w'),
                sort_keys=True, indent=4)

  def megaface_feature(self, megaface_align_path = MEGAFACE_ALIGN_PATH,
                      feature_path_to_save = MEGAFACE_FEATURE_PATH, 
                      megaface_align_list = MEGAFACE_ALIGN_LIST,
                      file_ending = '_cnn.bin'):
    with open(megaface_align_list) as fp:
      count = 0
      batch_path_list = []
      batch_image_list = []
      megafaceFile = json.load(fp)
      path_list = megafaceFile["path"]
      for i in range(len(path_list)):
        path = os.path.join(megaface_align_path, path_list[i])
        batch_path_list.append(path_list[i])
        image = cv2.imread(path)
        batch_image_list.append(image)
        count += 1
        if (count % BATCH_SIZE == 0 and count > 0):
          assert len(batch_path_list) == len(batch_image_list)
          images = np.array(batch_image_list)
          batch_image_list = []
          print images.shape
          features = self.cnn.run(images, BATCH_SIZE)
          print features.shape
          for j in range(BATCH_SIZE):
            feature_path = os.path.join(feature_path_to_save,
                                        batch_path_list[j] + file_ending)
            p,f = os.path.split(feature_path)
            if not os.path.exists(p):
              os.makedirs(p)
            save_mat(feature_path, features[j])
          batch_path_list = []
          
      # the rest
      batch_size_rest = len(batch_image_list)
      if (batch_size_rest > 0):
        assert batch_size_rest == len(batch_image_list)
        images = np.array(batch_image_list)
        batch_image_list = []
        print images.shape
        features = self.cnn.run(images, batch_size_rest)
        print features.shape
        for j in range(batch_size_rest):
          feature_path = os.path.join(feature_path_to_save,
                                       batch_path_list[j] + file_ending)
          p,f = os.path.split(feature_path)
          if not os.path.exists(p):
            os.makedirs(p)
          save_mat(feature_path, features[j])
        batch_path_list = []
 

if __name__ == "__main__":
  megaface_obj = megaface()
  megaface_obj.megaface_align()
  megaface_obj.megaface_feature()
