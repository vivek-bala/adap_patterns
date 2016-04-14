import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":

	nsims = 10
	sim_arg = 50
	ana_min_exec_time = 5
	ana_max_exec_time = 10
	ana_tot_duration = 50

	# Read given CSV
	df = pd.read_csv('execution_profile_nsims_{0}_simdur_{1}_anaexec_{2}-{4}_anatotdur_{3}.csv'.format(nsims,sim_arg,
		ana_min_exec_time,
		ana_tot_duration,
		ana_max_exec_time),
		header=5,sep=',',skipinitialspace=True)

	df = df.sort("Terminated")
	#print df
	#print df[df.Interrupt<="20"].count()

	# Construct required DF
	req_df = pd.DataFrame(columns=["Executing","Terminated","Done"])
	req_df.loc["0"] = [nsims,0,0]

	#print df[df.Interrupt < 2]
	#print df[df.Interrupt<="2"]

	terminated=0
	#print df[:1][" Started"]

	for row in df.iterrows():
		if row[1:][0]["Interrupt"] != "None":
			terminated+=1
			executing = nsims - terminated
			req_df.loc[row[1:][0]["Interrupt"]] = [executing,terminated,0]

			if terminated == nsims:
				break

	req_df.loc["{0}".format(sim_arg)] = [0,terminated,nsims-terminated]	

	#print req_df
	ax = req_df.plot(kind='bar',stacked=False,ylim=(0,nsims+2))
	ax.set_xlabel("Time (seconds)")
	ax.set_ylabel("Number of tasks")

	fig = plt.gcf()
	fig.set_size_inches(16,6)
	fig.savefig('plots/plot_interrupt_{0}-{1}.png'.format(ana_min_exec_time,ana_max_exec_time), dpi=100)
