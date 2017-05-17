Crop probe and megaface if necessary

Step1: align and generate feature for probe and megaface
> python probe_feature.py
> python megaface_feature.py

Step2: run with our feature:
> python run_experiment.py -s 1000000 -p ../resultlists/facescrub_aligned_list.json ../../MegaFace-feature ../../FaceScrub-feature '_cnn.bin' ../results/

