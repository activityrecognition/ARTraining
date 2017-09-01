# Thermset
Our goal is to help frail elders to live independently and safe for longer periods of time. To achieve such a goal, it is crucial to develop cost-effective methods to monitor their daily activities is crucial. We propose to automatically detect and track these activities using AI and thermal data. Data is at the core of any AI algorithm. Given the lack of openly available datasets of its kind, we constructed Thermset. Thermset, is the first open for research dataset containing long term thermal videos of seniors living independently at home or nursing homes. 

For more information about this work visit http://activityrecognition.com/thermset
# Download Thermset
Thermset contains raw and labeled data. Before using the data, read the "terms of use" and "License" described below.

## Raw Thermset data
We have collected themal videos of seniors living independently at home and nursing homes. You can download the raw data [Thermset Raw](https://s3-us-west-2.amazonaws.com/thermset/thermset_v1.1.tar), this is ~11 GB. 
 
## Labeled Thermset events
We labeled five important events (1) Lying (2) Sitting (3) Standing (4) People (5) Background. The labeled data can be found in the "dataset" folder.

# Experiment 
We have trained a neural network classifier to detect the labeled events. The results of our experiment can be found in the paper: "Vision-based Approach to Senior Healthcare: Convolutional Neural Networks for Five Clinical States. Zelun Luo, Alisha Rege, Guido Pusiol, Arnold Milstein, Li Fei-Fei, N. Lance Downing. American Medical Informatics Association (AMIA) 2017. Accepted paper."

To reproduce the results of the paper use the scripts: train_tnet5.ipynb and eval_tnet5.ipynb. 

# License
The dataset is available under license Creative Commons Attribution-NonCommercial 4.0 International. 
Cite the Thermset authors as:
"Pusiol G., and Polacov F., and Pusiol P.  2016. Thermset: A thermal database of seniors living independently and in nursing homes."

# Terms of use
Thermset is open for research purposes. Researchers interested in using the dataset must complete the form described below and send it by email to fpolacov@activityrecognition.com. 

------------------------------------- Permission to use Form ------------------------------------------------- 
[RESEARCHER_FULLNAME] (the "Researcher") requests permission to use the Thermset dataset (the "Database") at Activity Recognition Inc. In exchange for such permission, Researcher hereby agrees to the following terms and conditions:
1.	Researcher shall use the Database only for non-commercial research and educational purposes.
2.	Activity Recognition Inc. and Stanford University make no representations or warranties regarding the Database, including but not limited to warranties of non-infringement or fitness for a particular purpose.
3.	Researcher accepts full responsibility for his or her use of the Database and shall defend and indemnify the Thermset team, Activity Recognition Inc. Stanford University, including their employees, Trustees, officers and agents, against any and all claims arising from Researcher's use of the Database, including but not limited to Researcher's use of any copies of copyrighted images and videos that he or she may create from the Database.
4.	Researcher may provide research associates and colleagues with access to the Database provided that they first agree to be bound by these terms and conditions.
5.	Activity Recognition Inc. reserve the right to terminate Researcher's access to the Database at any time.
6.	If Researcher is employed by a for-profit, commercial entity, Researcher's employer shall also be bound by these terms and conditions, and Researcher hereby represents that he or she is fully authorized to enter into this agreement on behalf of such employer.
7.	The law of the State of California shall apply to all disputes under this agreement.
---------------------------------------------------------------------------------------------------------------

# Contact 
fpolacov@activityrecognition.com
ppusiol@activityrecognition.com
guido@cs.stanford.edu
