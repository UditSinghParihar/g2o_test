1. Manhattan generation  
	`python manh_const.py data/rtabmap.kitti data/labels.txt`  
2. Comparing GT and rtabmap  
	`cd data && python ../comp.py gt.kitti rtabmap.kitti`  
3. Saving and aligning in EVO  
	`evo_traj kitti rtabmap.kitti --ref gt.kitti -a --n_to_align 1  --plot --plot_mode xy --save_as_kitti`
4. Visualizing MLP's input and getting in a suitable format:  
	`python ../mlp_read.py mlp_in.txt`