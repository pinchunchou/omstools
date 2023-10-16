from util.oms import omsapi
import util.utility as u

fout = open("count_monitoring.csv", "w")

runnums = [
#374291,374293,374307,374322,374323,374344,
#374345,374347,374354,374521,
#374588,374595,374596,374599
#374668,374719,374728,374729,374730,374731,374751,374752,374753,374754,374763,374764,374765,
#374766,374767,374768,374778,374803,374804,374810,374828,374833,374834,374925,374950,374961,374970,
#374997,375002,375007,375013,
#375055,375058,375060,375061
#375064,375110
#375145,375164
#375195
375202
] # Run numbers to be used


#PbPb paths
hlt_paths = [
#"HLT_HIUPC_SingleJet8_ZDC1nXOR_MaxPixelCluster50000_v",
#"HLT_HIUPC_SingleJet12_ZDC1nXOR_MaxPixelCluster50000_v",
#"HLT_HIUPC_SingleJet16_ZDC1nXOR_MaxPixelCluster50000_v",
#"HLT_HIUPC_SingleJet20_ZDC1nXOR_MaxPixelCluster50000_v",
#"HLT_HIUPC_SingleJet24_ZDC1nXOR_MaxPixelCluster50000_v",
#"HLT_HIUPC_SingleJet28_ZDC1nXOR_MaxPixelCluster50000_v",

"HLT_HIUPC_SingleJet8_ZDC1nAsymXOR_MaxPixelCluster50000_v",
"HLT_HIUPC_SingleJet12_ZDC1nAsymXOR_MaxPixelCluster50000_v",
"HLT_HIUPC_SingleJet16_ZDC1nAsymXOR_MaxPixelCluster50000_v",
"HLT_HIUPC_SingleJet20_ZDC1nAsymXOR_MaxPixelCluster50000_v",
"HLT_HIUPC_SingleJet24_ZDC1nAsymXOR_MaxPixelCluster50000_v",
"HLT_HIUPC_SingleJet28_ZDC1nAsymXOR_MaxPixelCluster50000_v",

"HLT_HIUPC_SingleJet8_NotMBHF2AND_MaxPixelCluster50000_v",
"HLT_HIUPC_SingleJet12_NotMBHF2AND_MaxPixelCluster50000_v",
"HLT_HIUPC_SingleJet16_NotMBHF2AND_MaxPixelCluster50000_v",
"HLT_HIUPC_SingleJet20_NotMBHF2AND_MaxPixelCluster50000_v",
"HLT_HIUPC_SingleJet24_NotMBHF2AND_MaxPixelCluster50000_v",
"HLT_HIUPC_SingleJet28_NotMBHF2AND_MaxPixelCluster50000_v",
"HLT_HIUPC_ZDC1nOR_SinglePixelTrackLowPt_MaxPixelCluster400_v",
"HLT_HIUPC_ZDC1nOR_MinPixelCluster400_MaxPixelCluster10000_v",
"HLT_HIEphemeralZeroBias_v",
"HLT_HIRandom_v",
"HLT_HIRandom_HighRate_v",
] 

path_txt = "Run,"


for path in hlt_paths:
	path_txt += path
	path_txt += ","

fout.write(path_txt + '\n')

q_lumi = omsapi.query("lumisections")
q_lumi.paginate(per_page = 3000)
q_lumi.set_verbose(False)

q_hlt = omsapi.query("hltpathrates")
q_hlt.paginate(per_page = 3000)
q_hlt.set_verbose(False)

r_id = 0

for runnum in runnums:
	print('run:',runnum)

	q_lumi.clear_filter()
	q_lumi.filter("run_number", runnum).filter("beams_stable", 'true')

	if len(q_lumi.data().json()['data']) == 0:
		continue
	ls_stable_start = q_lumi.data().json()["data"][0]['attributes']['lumisection_number']
	ls_stable_end = q_lumi.data().json()["data"][-1]['attributes']['lumisection_number']
	#https://cmsoms.cern.ch/agg/api/v1/runs/373710/lumisections?filter[beams_stable]=true

	print('Stable beam start at lumisection',ls_stable_start)
	print('Stable beam end at lumisection',ls_stable_end)

	fout.write(str(runnum) + " (LS " + str(ls_stable_start) + "-"  + str(ls_stable_end) + "),")
	
	
	for hlt_path in hlt_paths:

		for v_num in range(1,12):
			q_hlt.clear_filter()
			q_hlt.filter("run_number", runnum).filter("path_name", hlt_path + str(v_num) ).filter("first_lumisection_number",ls_stable_start,"GE").filter("last_lumisection_number",ls_stable_end,"LE")

			if len(q_hlt.data().json()['data']) > 1:
				break

		data = q_hlt.data().json()['data']

		print('v = ',v_num,', len = ',len(data))
		
		#https://cmsoms.cern.ch/agg/api/v1/hltpathrates?filter[run_number][EQ]=373345&&filter[path_name][EQ]=HLT_PPRefGEDPhoton10_v1&&filter[first_lumisection_number][GE]=7&&filter[last_lumisection_number][LE]=27
		
		count = 0

		print(hlt_path+ str(v_num))

		i_len = ls_stable_end-ls_stable_start+1

		if i_len>len(data):
			i_len = len(data)

		for i in range(i_len):
			count += data[i]['attributes']['counter']		
		
		print("count:",count)
	
		fout.write(str(count)+ ',')
	
	fout.write('\n')
	r_id += 1

print('Done')