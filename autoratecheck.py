from util.oms import omsapi
import util.utility as u

fout = open("rate_monitoring.csv", "w")

ls_delta = 0 # The starting lumisection after stable beam. 
#For example, stable beam start at 7, so if ls_delta=163 we will start from lumisection 7+163=170.
ls_num_to_avg = 20 # How many lumisections to be averaged. 

runnums = [373710] # Run numbers to be used

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

	url = "https://cmsoms.cern.ch/agg/api/v1/runs/" + str(runnum) + "/lumisections?filter[beams_stable]=true"

	print('Stable beam start at lumisection',ls_start)
	ls_start+=ls_delta
	print('We start at lumisection',ls_start)
	print('Number of lumisections used to average:',ls_num_to_avg)

	fout.write(str(runnum) + " (LS " + str(ls_start) + "-"  + str(ls_start+ls_num_to_avg) + "),")
	
	for l1_path in l1_paths:
		q_l1.clear_filter()
		q_l1.filter("run_number", runnum).filter("name", l1_path).filter("first_lumisection_number",ls_start,"GE").filter("last_lumisection_number",ls_start+ls_num_to_avg,"LE")

		rate = 0
		for i in range(ls_num_to_avg):
			rate += q_l1.data().json()["data"][i]['attributes']['post_dt_rate']
		
		rate/=ls_num_to_avg
		print(l1_path,"rate:",rate)
	
		fout.write(str(rate) + ',')
	
	for hlt_path in hlt_paths:
		q_hlt.clear_filter()
		q_hlt.filter("run_number", runnum).filter("path_name", hlt_path).filter("first_lumisection_number",ls_start,"GE").filter("last_lumisection_number",ls_start+ls_num_to_avg,"LE")
		
		rate = 0
		for i in range(ls_num_to_avg):
			rate += q_hlt.data().json()['data'][i]['attributes']['rate']
		
		rate/=ls_num_to_avg
		print(hlt_path,"rate:",rate)
	
		fout.write(str(rate)+ ',')
	
	fout.write('\n')

print('Done')