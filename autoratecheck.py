from util.oms import omsapi
import util.utility as u

fout = open("rate_monitoring.csv", "w")

ls_delta = 10 # The starting lumisection after stable beam. 
#For example, stable beam start at 7, so if ls_delta=163 we will start from lumisection 7+163=170.
ls_num_to_avg = 50 # How many lumisections to be averaged. 

#runnums = [373710] # Run numbers to be used
runnums = [374322,374323] # Run numbers to be used


#ppref paths
'''
hlt_paths = [
"HLT_PPRefGEDPhoton10_v1", "HLT_PPRefGEDPhoton20_v1", "HLT_PPRefGEDPhoton30_v1",
"HLT_PPRefGEDPhoton40_v1", "HLT_PPRefGEDPhoton50_v1", "HLT_PPRefGEDPhoton60_v1", 
"HLT_PPRefGEDPhoton10_EB_v1", "HLT_PPRefGEDPhoton20_EB_v1", "HLT_PPRefGEDPhoton30_EB_v1",
"HLT_PPRefGEDPhoton40_EB_v1", "HLT_PPRefGEDPhoton50_EB_v1", "HLT_PPRefGEDPhoton60_EB_v1",
"HLT_PPRefEle10Gsf_v1", "HLT_PPRefEle15Gsf_v1", "HLT_PPRefEle20Gsf_v1", "HLT_PPRefEle30Gsf_v1", 
"HLT_PPRefEle40Gsf_v1", "HLT_PPRefEle50Gsf_v1",
"HLT_PPRefEle15Ele10Gsf_v1", "HLT_PPRefEle15Ele10GsfMass50_v1",
"HLT_PPRefDoubleEle10Gsf_v1", "HLT_PPRefDoubleEle10GsfMass50_v1",
"HLT_PPRefDoubleEle15Gsf_v1", "HLT_PPRefDoubleEle15GsfMass50_v1"
] 

l1_paths = ["L1_ZeroBias","L1_SingleEG15","L1_SingleEG21","L1_SingleEG30","L1_DoubleEG_15_10"]
'''

#PbPb paths
hlt_paths = [
"HLT_HIGEDPhoton10_v8", "HLT_HIGEDPhoton20_v8", "HLT_HIGEDPhoton30_v8",
"HLT_HIGEDPhoton40_v8", "HLT_HIGEDPhoton50_v8", "HLT_HIGEDPhoton60_v8", 
"HLT_HIGEDPhoton10_EB_v8", "HLT_HIGEDPhoton20_EB_v8", "HLT_HIGEDPhoton30_EB_v8",
"HLT_HIGEDPhoton40_EB_v8", "HLT_HIGEDPhoton50_EB_v8", "HLT_HIGEDPhoton60_EB_v8",
"HLT_HIDoubleGEDPhoton20_v1",
"HLT_HIEle10Gsf_v8", "HLT_HIEle15Gsf_v8", "HLT_HIEle20Gsf_v8", "HLT_HIEle30Gsf_v8", 
"HLT_HIEle40Gsf_v8", "HLT_HIEle50Gsf_v8",
"HLT_HIEle15Ele10Gsf_v8", "HLT_HIEle15Ele10GsfMass50_v8",
"HLT_HIDoubleEle10Gsf_v8", "HLT_HIDoubleEle10GsfMass50_v8",
"HLT_HIDoubleEle15Gsf_v8", "HLT_HIDoubleEle15GsfMass50_v8",
] 

l1_paths = ["L1_ZeroBias","L1_SingleEG7_BptxAND","L1_SingleEG15_BptxAND","L1_SingleEG21_BptxAND","L1_SingleEG30_BptxAND","L1_DoubleEG5_BptxAND"]

path_txt = "Run,"

for path in l1_paths:
	path_txt += path
	path_txt += ","

for path in hlt_paths:
	path_txt += path
	path_txt += ","

fout.write(path_txt + '\n')

q_lumi = omsapi.query("lumisections")
q_lumi.paginate(per_page = 3000)
q_lumi.set_verbose(False)

q_l1 = omsapi.query("l1algorithmtriggers")
q_l1.paginate(per_page = 3000)
q_l1.set_verbose(False)

q_hlt = omsapi.query("hltpathrates")
q_hlt.paginate(per_page = 3000)
q_hlt.set_verbose(False)

for runnum in runnums:
	print('run:',runnum)

	q_lumi.clear_filter()
	q_lumi.filter("run_number", runnum).filter("beams_stable", 'true')
	ls_start = q_lumi.data().json()["data"][0]['attributes']['lumisection_number']
	#ls_start=1
	#https://cmsoms.cern.ch/agg/api/v1/runs/373710/lumisections?filter[beams_stable]=true

	print('Stable beam start at lumisection',ls_start)
	ls_start+=ls_delta
	print('We start at lumisection',ls_start)
	print('Number of lumisections used to average:',ls_num_to_avg)

	fout.write(str(runnum) + " (LS " + str(ls_start) + "-"  + str(ls_start+ls_num_to_avg-1) + "),")
	
	for l1_path in l1_paths:
		q_l1.clear_filter()
		q_l1.filter("run_number", runnum).filter("name", l1_path).filter("first_lumisection_number",ls_start,"GE").filter("last_lumisection_number",ls_start+ls_num_to_avg,"LE")

	#https://cmsoms.cern.ch/agg/api/v1/l1algorithmtriggers?filter[run_number][EQ]=373710&&filter[name][EQ]=L1_ZeroBias&&filter[first_lumisection_number][GE]=7&&filter[last_lumisection_number][LE]=27

		rate = 0
		for i in range(ls_num_to_avg):
			rate += q_l1.data().json()["data"][i]['attributes']['post_dt_rate']
			#rate += q_l1.data().json()["data"][i]['attributes']['pre_dt_before_prescale_rate']
		
		rate/=ls_num_to_avg
		print(l1_path,"rate:",rate)
	
		fout.write(str(rate) + ',')
	
	for hlt_path in hlt_paths:
		q_hlt.clear_filter()
		q_hlt.filter("run_number", runnum).filter("path_name", hlt_path).filter("first_lumisection_number",ls_start,"GE").filter("last_lumisection_number",ls_start+ls_num_to_avg,"LE")
		
		#https://cmsoms.cern.ch/agg/api/v1/hltpathrates?filter[run_number][EQ]=373710&&filter[path_name][EQ]=HLT_PPRefGEDPhoton10_v1&&filter[first_lumisection_number][GE]=7&&filter[last_lumisection_number][LE]=27

		rate = 0
		for i in range(ls_num_to_avg):
			rate += q_hlt.data().json()['data'][i]['attributes']['rate']
		
		rate/=ls_num_to_avg
		print(hlt_path,"rate:",rate)
	
		fout.write(str(rate)+ ',')
	
	fout.write('\n')

print('Done')