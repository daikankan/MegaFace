#!/usr/bin/env python
# coding=utf-8

import os
import sys
import cv2
import json
import numpy as np
from align import FaceAligned
from mtcnn import CNN
from matio import *

# probe feature
PROBE_PATH = os.path.join('..','..','FaceScrub-full')
PROBE_CROP_PATH = os.path.join('..','..','FaceScrub-crop')
PROBE_ALIGN_PATH = os.path.join('..','..','FaceScrub-align')
PROBE_FEATURE_PATH = os.path.join('..','..','FaceScrub-feature')
PROBE_LIST = os.path.join('..','templatelists','facescrub_uncropped_features_list.json')
PROBE_ALIGN_LIST = os.path.join('..','resultlists','facescrub_aligned_list.json')

BATCH_SIZE = 100 # for cnn forward

if not os.path.exists(PROBE_ALIGN_PATH):
  os.makedirs(PROBE_ALIGN_PATH)

if not os.path.exists(PROBE_FEATURE_PATH):
  os.makedirs(PROBE_FEATURE_PATH)

class probe():
  def __init__(self):
    self.align = FaceAligned()
    self.cnn = CNN()
    self.logFile = open('./warning.log', 'w+')

  def probe_align(self, probe_path = PROBE_PATH,
                  probe_crop_path = PROBE_CROP_PATH,
                  align_path_to_save = PROBE_ALIGN_PATH,
                  probe_list = PROBE_LIST,
                  probe_align_list = PROBE_ALIGN_LIST,
                  save_ext = '.png'):
    with open(probe_list) as fp:
      probeFile = json.load(fp)
      path_list = probeFile["path"]
      alignFile = {}
      path_save_list = []
      for i in range(len(path_list)):
        path = os.path.join(probe_path, path_list[i])
        im_align = self.align.aligned(str(path))
        # if align origin image failed try crop image
        if im_align is None:
          print >> self.logFile, "%s align failed" %(path)
          path_crop = os.path.join(probe_crop_path, path_list[i])
          im_align = self.align.aligned(path_crop)
        # if align crop image failed use resize image
        if im_align is None:
          print >> self.logFile, "%s failed, use resize image" %(path_crop)
          im = cv2.imread(path)
          im_align = cv2.resize(im, (96, 112))
        path_temp = os.path.join(align_path_to_save, path_list[i])
        p,f = os.path.split(path_temp)
        if not os.path.exists(p):
          os.makedirs(p)
        path_save = os.path.splitext(path_temp)[0] + save_ext
        cv2.imwrite(path_save, im_align)
        path_save_list.append(os.path.splitext(path_list[i])[0] + save_ext)
      # save aligned list file
      alignFile["path"] = path_save_list
      p,f = os.path.split(probe_align_list)
      if not os.path.exists(p):
        os.makedirs(p)
      json.dump(alignFile, open(probe_align_list, 'w'),
                sort_keys=True, indent=4)

  def probe_feature(self, probe_align_path = PROBE_ALIGN_PATH,
                    feature_path_to_save = PROBE_FEATURE_PATH, 
                    probe_align_list = PROBE_ALIGN_LIST,
                    file_ending = '_cnn.bin'):
    with open(probe_align_list) as fp:
      count = 0
      batch_path_list = []
      batch_image_list = []
      probeFile = json.load(fp)
      path_list = probeFile["path"]
      for i in range(len(path_list)):
        path = os.path.join(probe_align_path, path_list[i])
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
  probeApp = probe()
  #probeApp.probe_align()
  probeApp.probe_feature()
