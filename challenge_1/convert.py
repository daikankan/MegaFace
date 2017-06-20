#!/usr/bin/env python
# coding=utf-8

# Convert megaface and probe feature for FALCONN

import os
import sys
import json
import struct
import numpy as np
from matio import *

PROBE_FEATURE_PATH = os.path.join('..','..','FaceScrub-feature')
PROBE_LIST_BASE = os.path.join('..','resultlists','facescrub_aligned_list.json')
MEGAFACE_FEATURE_PATH = os.path.join('..','..','MegaFace-feature')
MEGAFACE_LIST_BASE = os.path.join('..','resultlists','megaface_aligned_list.json_1000000_1')
FILE_ENDING = '_cnn_face_deploy2_best4.bin'
RESULT_PATH = os.path.join('..','dataset')

if not os.path.exists(RESULT_PATH):
  os.makedirs(RESULT_PATH)

def convert(feature_path, listname_base, result_path, dataset, file_ending):
  with open(listname_base) as fp:
    with open(os.path.join(result_path, dataset), 'wb') as ouf:
      counter = 0
      probeFile = json.load(fp)
      path_list = probeFile["path"]
      for i in range(len(path_list)):
        path = os.path.join(feature_path, path_list[i] + file_ending)
        mat = load_mat(path)
        mat = mat.reshape(mat.shape[0])
        # print mat.shape
        mat_list_float32 = mat.tolist()
        mat_list = [float(x) for x in mat_list_float32]
        assert len(mat_list) == 512
        ouf.write(struct.pack('i', len(mat_list)))
        ouf.write(struct.pack('%sf' % len(mat_list), *mat_list))
        counter += 1
        if counter % 100 == 0:
          sys.stdout.write('%d points processed...\n' % counter)
      sys.stdout.write('%d points processed...\n' % counter)


if __name__ == '__main__':
  # convert probe feature for FALCONN
  convert(PROBE_FEATURE_PATH, PROBE_LIST_BASE,
          RESULT_PATH, 'probe.dat', FILE_ENDING)
  # convert megaface feature for FALCONN
  convert(MEGAFACE_FEATURE_PATH, MEGAFACE_LIST_BASE,
          RESULT_PATH, 'megaface.dat', FILE_ENDING)
  '''
  #inf = open('/home/dkk/projects/FALCONN-1.2.2/src/examples/glove/dataset/glove.840B.300d.dat', 'rb')
  inf = open(os.path.join(RESULT_DATASET,'probe.dat'), 'rb')
  length = struct.unpack('i', inf.read(4))
  mat_list = struct.unpack('%sf' % 512, inf.read(512 * 4))
  print len(mat_list)
  print length
  print mat_list
  '''
  '''
  b = np.random.rand(512)
  a = np.float32(b)
  print len(a.shape)
  print a.dtype

  save_mat(os.path.join('..','dataset','mat.bin'), a)
  b = load_mat(os.path.join('..','dataset','mat.bin'))
  print b.shape
  print b.dtype
  print b
  '''
