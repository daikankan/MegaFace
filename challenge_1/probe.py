#!/usr/bin/python

import os
import sys
import json
import Image

PROBE_CROP_PATH = os.path.join('..', '..', 'FaceScrub-crop')
if not os.path.exists(PROBE_CROP_PATH):
  os.makedirs(PROBE_CROP_PATH)
  
PROBE_PATH = os.path.join('..','..','FaceScrub-full')
PROBE_LIST = os.path.join('..','templatelists','facescrub_uncropped_features_list.json')
ACTORS_TXT = os.path.join('..','..','facescrub_actors.txt')
ACTRESSES_TXT = os.path.join('..','..','facescrub_actresses.txt')

def read_probe_txt(actors_txt = ACTORS_TXT,
                   actresses_txt = ACTRESSES_TXT):
  id_bbox = {}
  actorsFile = open(actors_txt, 'r')
  actorsFile.readline() # first line useless
  info = actorsFile.readline()
  while info:
    info_list = info.split('\t')
    id_bbox[info_list[2]] = info_list[4]
    info = actorsFile.readline()
  actorsFile.close()
  actressesFile = open(actresses_txt, 'r')
  actressesFile.readline() # first line useless
  info = actressesFile.readline()
  while info:
    info_list = info.split('\t')
    id_bbox[info_list[2]] = info_list[4]
    info = actressesFile.readline()
  actressesFile.close()
  return id_bbox

def crop_image(path_origin, path_to_save, bbox, ext = '.jpg'):
  if not os.path.isfile(path_origin):
    print path_origin + "is missing"
  else:
    im = Image.open(path_origin)
    im_crop = im.crop(bbox)
    p,f = os.path.split(path_to_save)
    path = os.path.splitext(path_to_save)[0] + ext # avoid gif failure
    if not os.path.exists(p):
      os.makedirs(p)
    im_crop.save(path)

def crop_probe(probe_path = PROBE_PATH,
               probe_crop_path = PROBE_CROP_PATH,
               probe_list = PROBE_LIST):
  id_bbox = read_probe_txt()
  with open(probe_list) as fp:
    probeFile = json.load(fp)
    path_list = probeFile["path"]
    for i in range(len(path_list)):
      id = os.path.splitext(path_list[i].split('_')[-1])[0]
      bbox = id_bbox[id].split(',')
      path_origin = os.path.join(probe_path, path_list[i])
      path_to_save = os.path.join(probe_crop_path, path_list[i])
      crop_image(path_origin, path_to_save, 
                 (int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])))

if __name__ == '__main__':
  crop_probe()
