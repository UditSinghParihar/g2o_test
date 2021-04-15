# g2o_test #


1. `Nomenclature` for `tf_label_opt.txt` and `tf_label_unopt.txt`
	`1st col` : x cord. of a robot`(= l1)`   
 	`2nd col` : y cord. of a robot`(= b1)`  
 	`3rd col` : theta orientation of robot 
 	`4th col` : label of a node  

2. EVO command:  
	`evo_traj kitti opt.kitti --ref ground_truth.kitti -a --n_to_align 1 --plot --plot_mode xy --save_as_kitti`