from pymongo import MongoClient
import datetime
client = MongoClient()
db = client['data_monitor']


def getData_N_Min(t):
	date1 = datetime.datetime.utcnow()-datetime.timedelta(minutes=t)
	cursor=db.data.find({'date':{"$gte": date1}})
	return cursor
date1=datetime.datetime(2016, 3, 7, 23 , 50, 29, 310151)
date2=datetime.datetime(2016, 3, 7, 23, 44, 29, 310151)

cursor=db.data.find({"$and":[{'date':{"$gte": date2}},{'date':{"$lte": date1}}]})

n_times=getData_N_Min(10)
if n_times.count()==0:
	print "No Data"
	exit(1)
data=dict()
t=0
data=[]
#Target only swap space
machine=['compute-2-29', 'compute-2-28', 'compute-9-30', 'compute-9-36', 'compute-9-35','compute-9-34','compute-2-23', 'compute-2-25', 'compute-2-24', 'compute-2-27', 'compute-2-26', 'compute-6-29', 'compute-6-28', 'compute-6-25', 'compute-6-24', 'compute-6-27', 'compute-6-26', 'compute-6-23', 'compute-9-33', 'compute-9-32', 'compute-22-17', 'compute-22-16', 'compute-22-15', 'compute-22-14', 'compute-22-13', 'compute-22-12', 'compute-22-11', 'compute-22-18', 'compute-7-39', 'compute-7-38', 'compute-21-29', 'compute-21-28', 'compute-21-27', 'compute-21-26', 'compute-21-25', 'compute-21-24', 'compute-21-23', 'compute-5-1', 'compute-14-1', 'compute-14-2', 'compute-14-3', 'compute-14-4', 'compute-14-5', 'compute-14-6', 'compute-14-7', 'compute-14-8', 'compute-13-6', 'compute-13-5', 'compute-13-4', 'compute-7-40', 'compute-13-2', 'compute-13-1', 'compute-14-30', 'compute-5-8', 'compute-14-32', 'compute-14-33', 'compute-14-34', 'compute-14-35', 'compute-18-18', 'compute-14-37', 'compute-14-38', 'compute-18-17', 'compute-5-3', 'compute-18-15', 'compute-5-5', 'compute-18-13', 'compute-5-7', 'compute-5-6', 'compute-6-2', 'compute-3-41', 'compute-6-1', 'compute-6-6', 'compute-6-7', 'compute-6-4', 'compute-6-5', 'compute-6-8', 'compute-13-28', 'compute-13-29', 'compute-13-26', 'compute-13-27', 'compute-13-24', 'compute-13-25', 'compute-13-23', 'compute-2-10', 'compute-2-11', 'compute-2-12', 'compute-2-14', 'compute-2-15', 'compute-2-16', 'compute-2-17', 'compute-2-18', 'compute-14-40', 'compute-2-8', 'compute-2-9', 'compute-2-7', 'compute-20-40', 'compute-1-9', 'compute-1-8', 'compute-6-11', 'compute-8-40', 'compute-6-14', 'compute-6-15', 'compute-6-16', 'compute-6-17', 'compute-6-10', 'compute-5-4', 'compute-6-12', 'compute-6-13', 'compute-6-18', 'compute-4-29', 'compute-4-28', 'compute-23-38', 'compute-22-2', 'compute-23-36', 'compute-23-37', 'compute-23-34', 'compute-23-35', 'compute-4-27', 'compute-23-33', 'compute-4-25', 'compute-11-18', 'compute-8-38', 'compute-8-39', 'compute-11-17', 'compute-11-16', 'compute-22-40', 'compute-1-11', 'compute-1-10', 'compute-1-13', 'compute-1-12', 'compute-1-15', 'compute-1-14', 'compute-1-17', 'compute-1-16', 'compute-5-15', 'compute-5-14', 'compute-12-8', 'compute-5-16', 'compute-5-11', 'compute-5-10', 'compute-5-13', 'compute-5-12', 'compute-12-2', 'compute-12-3', 'compute-12-1', 'compute-12-6', 'compute-12-7', 'compute-12-4', 'compute-12-5', 'compute-12-27', 'compute-12-26', 'compute-12-18', 'compute-19-37', 'compute-19-36', 'compute-12-10', 'compute-12-11', 'compute-12-12', 'compute-12-13', 'compute-12-14', 'compute-12-15', 'compute-12-16', 'compute-12-17', 'compute-20-37', 'compute-20-36', 'compute-20-35', 'compute-20-39', 'compute-20-38', 'compute-23-39', 'compute-23-32', 'compute-4-26', 'compute-23-30', 'compute-12-23', 'compute-12-22', 'compute-12-25', 'compute-12-24', 'compute-19-39', 'compute-19-38', 'compute-12-29', 'compute-12-28', 'compute-19-35', 'compute-9-27', 'compute-21-40', 'compute-9-28', 'compute-9-29', 'compute-11-40', 'compute-21-38', 'compute-21-39', 'compute-21-30', 'compute-21-33', 'compute-21-34', 'compute-21-35', 'compute-21-36', 'compute-21-37', 'compute-5-28', 'compute-5-29', 'compute-5-24', 'compute-5-25', 'compute-5-26', 'compute-5-27', 'compute-5-23', 'compute-13-18', 'compute-13-13', 'compute-13-12', 'compute-13-11', 'compute-13-10', 'compute-13-17', 'compute-13-16', 'compute-13-15', 'compute-13-14', 'compute-14-15', 'compute-22-39', 'compute-22-38', 'compute-22-30', 'compute-22-33', 'compute-22-35', 'compute-22-34', 'compute-22-37', 'compute-22-36', 'compute-7-17', 'compute-7-16', 'compute-7-18', 'compute-5-17', 'compute-14-18', 'compute-14-12', 'compute-14-13', 'compute-14-10', 'compute-14-11', 'compute-14-16', 'compute-14-17', 'compute-14-14', 'compute-5-18', 'compute-21-8', 'compute-21-1', 'compute-21-2', 'compute-21-3', 'compute-21-4', 'compute-21-5', 'compute-21-6', 'compute-21-7', 'compute-4-30', 'compute-18-14', 'compute-23-27', 'compute-23-26', 'compute-12-37', 'compute-12-38', 'compute-21-11', 'compute-5-39', 'compute-5-38', 'compute-5-37', 'compute-5-36', 'compute-5-35', 'compute-5-34', 'compute-5-33', 'compute-5-32', 'compute-5-30', 'compute-22-3', 'compute-18-35', 'compute-22-1', 'compute-18-37', 'compute-22-7', 'compute-22-6', 'compute-22-5', 'compute-22-4', 'compute-22-8', 'compute-18-38', 'compute-18-39', 'compute-20-15', 'compute-20-17', 'compute-20-16', 'compute-20-18', 'compute-9-25', 'compute-2-38', 'compute-2-39', 'compute-2-36', 'compute-2-37', 'compute-2-34', 'compute-2-35', 'compute-2-32', 'compute-2-33', 'compute-2-30', 'compute-6-32', 'compute-6-33', 'compute-6-30', 'compute-6-36', 'compute-6-37', 'compute-6-34', 'compute-6-35', 'compute-6-38', 'compute-6-39', 'compute-9-26', 'compute-21-12', 'compute-21-13', 'compute-23-16', 'compute-23-17', 'compute-21-16', 'compute-21-17', 'compute-21-14', 'compute-21-15', 'compute-21-18', 'compute-23-18', 'compute-8-18', 'compute-8-16', 'compute-8-17', 'compute-11-39', 'compute-11-38', 'compute-22-28', 'compute-22-29', 'compute-22-23', 'compute-22-26', 'compute-22-27', 'compute-22-24', 'compute-22-25', 'compute-13-8', 'compute-13-7', 'compute-19-13', 'compute-19-15', 'compute-19-14', 'compute-19-17', 'compute-19-16', 'compute-13-3', 'compute-14-27', 'compute-14-26', 'compute-14-25', 'compute-14-24', 'compute-14-23', 'compute-14-36', 'compute-14-29', 'compute-14-28', 'compute-18-16', 'compute-14-39', 'compute-3-39', 'compute-3-38', 'compute-5-2', 'compute-13-39', 'compute-13-38', 'compute-13-35', 'compute-13-34', 'compute-13-37', 'compute-13-36', 'compute-13-30', 'compute-13-33', 'compute-13-32', 'compute-3-40', 'compute-6-3', 'compute-13-40', 'compute-18-36', 'compute-23-29', 'compute-23-28', 'compute-23-25', 'compute-4-32', 'compute-4-33', 'compute-4-34', 'compute-4-35', 'compute-19-40', 'compute-18-40']
for t1 in n_times:
	devices=t1['data'].keys()
	#data=dict()
#	machine=['compute-4-34','compute-5-35','compute-13-14']
	for d in machine:
		lst=[]
		lst.append(d)
		for x in xrange(0,20):
			lst.append(t1['data'][d][x][1])
		data.append(lst)
		# else:
		# 	data[d][d]=[t1['data'][d][0][0:20]]
	#break
	t=t+1

#print data
#exit(0)
res=['Device','G_Swap_Total', 'G_Swap_Free', 'G_Swap_Used', 'G_Proc_Run', 'G_Cpu_User', 'G_Cpu_Wio', 'G_Load_One', 'G_Load', 'G_Five', 'G_Load_Fifteen', 'G_Mem_Cached', 'G_Mem_Total', 'T_State', 'T_Slots', 'T_SlotsUsed', 'T_AvailMem(MB)', 'T_TotalMem(MB)/Swap', 'T_Time_Last_Rec', 'T_LoadAve', 'T_NetLoad(MB)']
att=['G_Swap_Used','G_Cpu_User', 'G_Cpu_Wio', 'G_Load_One', 'G_Load', 'G_Five', 'G_Load_Fifteen', 'G_Mem_Cached', 'T_AvailMem(MB)', 'T_LoadAve', 'T_NetLoad(MB)']

new_att=['Device','G_Swap_Used', 'G_Proc_Run', 'G_Cpu_User', 'G_Cpu_Wio', 'G_Load_One', 'G_Load', 'G_Five', 'G_Load_Fifteen', 'G_Mem_Cached', 'T_State', 'T_Slots', 'T_SlotsUsed', 'T_AvailMem(MB)', 'T_Time_Last_Rec', 'T_LoadAve', 'T_NetLoad(MB)']
new_index=[]
full_index=[]

for a in att:
    new_index.append(res.index(a))

for i in new_att:
    full_index.append(res.index(i))


new_data=[]

for d in data:
    core_count=int(d[15])
    if core_count!=0:
        for i in new_index:
            d[i]=round(float(d[i])/core_count,2)
            d[i]=unicode(d[i])
    tmp=[]
    tmp=[d[i] for i in full_index]
    new_data.append(tmp)

# for d in data:
#     core_count=int(d[14])
#     if core_count!=0:
#         for i in new_index:
#             d[i]=round(float(d[i])/core_count,2)
#             d[i]=unicode(d[i])            
#     tmp=[]
#     tmp=[d[i] for i in full_index]
#     new_data.append(tmp)

import pandas as pd

df=pd.DataFrame(new_data)
print df

df.columns=['Device','G_Swap_Used', 'G_Proc_Run', 'G_Cpu_User', 'G_Cpu_Wio', 'G_Load_One', 'G_Load', 'G_Five', 'G_Load_Fifteen', 'G_Mem_Cached', 'T_State', 'T_Slots', 'T_SlotsUsed', 'T_AvailMem(MB)', 'T_Time_Last_Rec', 'T_LoadAve', 'T_NetLoad(MB)']

#print df
#exit(0)

X = df.ix[:,1:17].values
y = df.ix[:,0].values

#print X
#print y


# #from matplotlib import pyplot as plt
# import numpy as np


# # feature_dict = {0: 'G_Swap_Total', 1: 'G_Swap_Free', 2: 'G_Swap_Used', 3: 'G_Proc_Run', 4: 'G_Cpu_User', 5: 'G_Cpu_Wio', 6: 'G_Load_One', 7: 'G_Load', 
# # 8: 'G_Five', 9: 'G_Load_Fifteen', 10: 'G_Mem_Cached', 11: 'G_Mem_Total', 12: 'T_State', 13: 'T_Slots', 14: 'T_SlotsUsed', 15: 'T_AvailMem(MB)', 16: 'T_TotalMem(MB)/Swap', 17: 'T_Time_Last_Rec', 18: 'T_LoadAve', 19: 'T_NetLoad(MB)'}

# from sklearn.preprocessing import StandardScaler
# X_std = StandardScaler().fit_transform(X)

# CLUSTER_SIZE=2


# from sklearn.decomposition import PCA as sklearnPCA
# sklearn_pca = sklearnPCA(n_components=CLUSTER_SIZE)
# Y_sklearn 	= sklearn_pca.fit_transform(X_std)


# x_corr=[]
# y_corr=[]
# label=[]


# x_l=[]
# y_l=[]
# for lab in machine:
# 	x_l.append(Y_sklearn[y==lab, 0].tolist())
# 	y_l.append(Y_sklearn[y==lab, 1].tolist())

# for x in x_l:
# 	for x1 in x:
# 		x_corr.append(x1)

# for y in y_l:
# 	for y1 in y:
# 		y_corr.append(y1)

# l=len(x_l[0])

# for lab in machine:
# 	for i in [lab for x in range(0,l)]:
# 		label.append(i)


# new_arr=np.array(zip(x_corr,y_corr))

# #df_snp_pca = pd.DataFrame(df_snp_pca, 
# #                columns=['PC' + str(x) for x in range(1, n_components+1)], 
# from sklearn.cluster import KMeans
# #from sklearn import datasets

# #CLUSTER_SIZE=2
# k_means=KMeans(n_clusters=CLUSTER_SIZE)
# k_means.fit(new_arr)

# centroid=k_means.cluster_centers_
# labels=k_means.labels_


# colors=["green","red","cyan","yellow","blue"]

# color_src=[]

# groups_color={"green":set(),
# 			   "red":set(),
# 			   "cyan":set(),
# 			   "yellow":set(),
# 			   "blue":set()}

# for i in range(len(x_corr)):
# 	color_src.append(colors[labels[i]])
# 	groups_color[colors[labels[i]]].add(label[i])

# print groups_color
# red_lst=[]
# ms=0
# f=open("color_cluster.csv",'w+')
# file_color_header=[]
# for i in range(1,CLUSTER_SIZE+1):
# 	file_color_header.append("Color"+str(i))
# f.write(','.join(file_color_header)+','+','.join(df.columns)+'\n')

# for d in new_data:
# 	color_label=[]
# 	if d[0] in groups_color['red']:
# 		color_label.append('red')
# 	if d[0] in groups_color['green']:
# 		color_label.append('green')
# 	if d[0] in groups_color['yellow']:
# 		color_label.append('yellow')
# 	if d[0] in groups_color['blue']:
# 		color_label.append('blue')
# 	if d[0] in groups_color['cyan']:
# 		color_label.append('cyan')	
# 	if ms<len(color_label):
# 		ms=len(color_label)
# 	l=len(color_label)
# 	for i in range(0,CLUSTER_SIZE-l):
# 		color_label.append("None")
# 	#if len(color_label)<4:
# 	#	for i in range()
# 	#	color_label.append("None")
# 	f.write(','.join(color_label)+","+(','.join(d)+"\n"))	

# print "Max Color"+str(ms)




# from bokeh.plotting import figure, output_file, show, ColumnDataSource
# from bokeh.models import HoverTool#,BoxZoomTool, ResetTool,ResizeTool,WheelZoomTool

# output_file("toolbar.html")
# TOOLS="resize,crosshair,pan,wheel_zoom,box_zoom,reset,tap,previewsave,box_select,poly_select,lasso_select"

# source = ColumnDataSource(
#         data=dict(
#             x=x_corr,
#             y=y_corr,
#             desc=label,
#            # colors=color_src,
            
#         )
#     )
# hover = HoverTool(
#         tooltips="""
#         <div>
            
#             <div>
#                 <span style="font-size: 17px; font-weight: bold;">@desc</span>
#                 <span style="font-size: 15px; color: #966;">[$index]</span>
#             </div>
#             <div>
#                 <span style="font-size: 15px;">Location</span>
#                 <span style="font-size: 10px; color: #696;">($x, $y)</span>
#             </div>
#         </div>
#         """
#     )
# #TOOLS= [BoxZoomTool(), ResetTool(),hover,ResizeTool(),WheelZoomTool()]

# TOOLS=["pan,wheel_zoom,box_zoom,reset,resize",hover]
# p = figure(plot_width=1000, plot_height=1000, tools=TOOLS,
#            title="Mouse over the dots")

# p.circle('x', 'y', size=30, source=source,fill_color=color_src)
# p.scatter(centroid[:,0],centroid[:,1], color='black')#,s=200,linewidths=5,zorder=10)

# show(p)

### Doing some feature extraction
import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import make_classification
from sklearn.ensemble import ExtraTreesClassifier

# Build a classification task using 3 informative features

feat=new_att[1:]
# Build a forest and compute the feature importances
forest = ExtraTreesClassifier(n_estimators=250,
                              random_state=0)

forest.fit(X, y)
importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")
add_feat=[]
for f in range(X.shape[1]):
    print("%d. feature %s (%f)" % (f + 1, feat[indices[f]], importances[indices[f]]))
    add_feat.append(feat[indices[f]][2:8])

# Plot the feature importances of the forest
plt.figure()
plt.title("Feature importances")
plt.bar(range(X.shape[1]), importances[indices],
       color="r", yerr=std[indices], align="center")
plt.xticks(range(X.shape[1]), add_feat)
plt.xlim([-1, X.shape[1]])
plt.show()

exit(0)

