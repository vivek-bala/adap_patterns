import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":

	nsims = 12
	sim_arg = 50
	ana_exec_time = 10
	ana_tot_duration = 50
	cores = 4

	# Read given CSV
	df = pd.read_csv('execution_profile_nsims_{0}_simdur_{1}_anaexec_{2}_anatotdur_{3}.csv'.format(nsims,sim_arg,
		ana_exec_time,
		ana_tot_duration),
		header=4,sep=',',skipinitialspace=True)

	df = df.sort("Terminated")
	#print df
	#print df[df.Interrupt<="20"].count()

	'''
	# Construct required DF
	# Plot with interrupt as x-axis
	req_df = pd.DataFrame(columns=["Executing","Terminated","Done"])
	req_df.loc["0"] = [nsims,0,0]

	#print df[df.Interrupt < 2]
	#print df[df.Interrupt<="2"]

	terminated=0
	#print df[:1][" Started"]

	for row in df.iterrows():
		if row[1:][0]["Interrupt"] != "None":
			print row[1:][0]["Interrupt"]
			terminated+=1
			executing = nsims - terminated
			req_df.loc["{0}".format(row[1:][0]["Interrupt"])] = [executing, terminated,0]
			if terminated == nsims:
				break

	req_df.loc["{0}".format((nsims/cores)*sim_arg)] = [0,terminated,nsims-terminated]	

	#print req_df
	ax = req_df.plot(kind='bar',stacked=False,ylim=(0,nsims+2))
	ax.set_xlabel("Time (seconds)")
	ax.set_ylabel("Number of tasks")

	fig = plt.gcf()
	fig.set_size_inches(16,6)
	fig.savefig('plots/plot_interrupt_{0}.png'.format(ana_exec_time), dpi=100)

	
	# Plot with states as x-axis
	k = df["pid"]
	req_df = pd.DataFrame(columns=k,index=["Started","Terminated","Done"])

	for row in df.sort("pid").iterrows():
		started = float(row[1:][0]["Started"])
		terminated = None
		done  = None

		if row[1:][0]["Terminated"] != "None":
			terminated = float(row[1:][0]["Terminated"])
		if row[1:][0]["Done"] != "None":
			done = float(row[1:][0]["Done"])

		req_df["{0}".format(row[1:][0]["pid"])] = [started,terminated,done]


	#print req_df

	import numpy as np
	k=[]
	for val in req_df.loc["Done"]:
		if np.isfinite(val) == True:
			k.append(val)

	#print max(k)
	#print (min(req_df.loc["Started"]), max(req_df[np.isfinite(req_df.loc["Done"])]))

	#print min(req_df[0])
	print req_df
	my_colors = [(x/20.0, x/40.0, 0.75) for x in range(nsims)]
	ax = req_df.plot(kind='bar', ylim = (min(req_df.loc["Started"])-20, max(k)+200),color=my_colors,rot=0)
	ax.set_xlabel("Units")
	ax.set_ylabel("Time (seconds)")

	fig = plt.gcf()
	fig.set_size_inches(16,6)
	fig.savefig('plots/plot_unit_status.png', dpi=100)

	'''
	
	# Plot with units as x-axis
	k = df["pid"]
	req_df = pd.DataFrame(index=k,columns=["Started","Terminated","Done"])

	for row in df.sort("pid").iterrows():
		started = row[1:][0]["Started"]
		terminated = 0
		done  = 0

		if row[1:][0]["Terminated"] != "None":
			terminated = float(row[1:][0]["Terminated"])
		if row[1:][0]["Done"] != "None":
			done = float(row[1:][0]["Done"])

		req_df.loc["{0}".format(row[1:][0]["pid"])] = [started,terminated,done]

	#print req_df


	ax = req_df.plot(kind='bar', ylim = (min(req_df["Started"])-100, max(req_df["Done"])+100),rot=0)
	ax.set_xlabel("Units")
	ax.set_ylabel("Time (seconds)")

	fig = plt.gcf()
	fig.set_size_inches(16,6)
	fig.savefig('plots/plot_unit_status.png', dpi=100)