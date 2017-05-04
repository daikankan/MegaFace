1. align and generate features using our models
> python generate_feature.py '../../data/daniel/FlickrFinal2' '../../MegaFace/MegaFace_cropped' '../../MegaFace/MegaFace_CNNFeatures' '../../FaceScrub-full' '../../probe/probe_cropped' '../../probe/probe_CNNFeatures' '_CNN.bin' --sizes=10000 --batchsize=100 


2. generate megaface and probe feature list (json) 
> python my_experiment.py ../../MegaFace/MegaFace_CNNFeatures/10000 ../../probe/probe_CNNFeatures _CNN.bin ./out_root --sizes=10000

3. test on our feature (using list generated from step 2)
> python my_experiment2.py ../../MegaFace/MegaFace_CNNFeatures/10000 ../../probe/probe_CNNFeatures _CNN.bin ../../MegaFace/CNN_results/ --sizes=10000 --probe_list=./out_root/otherFiles/facescrub_features_CNN

