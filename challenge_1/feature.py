#!/usr/bin/env python
# coding=utf-8

import os
import sys
import cv2
import json
from align import FaceAligned

# probe feature
PROBE_PATH = os.path.join('..','..','FaceScrub-full')
PROBE_CROP_PATH = os.path.join('..','..','FaceScrub-crop')
PROBE_ALIGN_PATH = os.path.join('..','..','FaceScrub-align')
PROBE_LIST = os.path.join('..','templatelists','facescrub_uncropped_features_list.json')

if not os.path.exists(PROBE_ALIGN_PATH):
  os.makedirs(PROBE_ALIGN_PATH)


class probe():
  def __init__(self):
    self.align = FaceAligned()
    self.logFile = open('./warning.log', 'w+')

  def probe_align(self, probe_path = PROBE_PATH,
                probe_crop_path = PROBE_CROP_PATH,
                path_to_save = PROBE_ALIGN_PATH,
                probe_list = PROBE_LIST):
    with open(probe_list) as fp:
      probeFile = json.load(fp)
      path_list = probeFile["path"]
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
        path_temp = os.path.join(path_to_save, path_list[i])
        p,f = os.path.split(path_temp)
        if not os.path.exists(p):
          os.makedirs(p)
        path_save = os.path.splitext(path_temp)[0] + '.png'
        cv2.imwrite(path_save, im_align)
        

if __name__ == "__main__":
  probeApp = probe()
  probeApp.probe_align()
