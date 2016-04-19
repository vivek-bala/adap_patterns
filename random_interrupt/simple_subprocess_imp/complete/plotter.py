import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":

	nsims = 10
	sim_arg = 50

	ana_tot_duration = 50

	interrupt_min_tasks = 1
	interrupt_max_tasks = 3

	interrupt_min_time = 5
	interrupt_max_time = 10

	# Read given CSV
	df = pd.read_csv('execution_profile_nsims_{0}_simdur_{1}_anamin_{2}_anamax{3}_anatotdur_{4}_max_{5}.csv'.format(nsims,
		sim_arg,
		interrupt_min_time,
		interrupt_max_time,
		ana_tot_duration,
		interrupt_max_tasks),
		header=7,sep=',',skipinitialspace=True)

	df = df.sort("Interrupt")
	#print df
	#print df[df.Interrupt<="20"].count()

	# Construct required DF

	req_df = pd.DataFrame(columns=["Executing","Terminated","Done"])
	req_df.loc["0"] = [nsims,0,0]

	#print df[df.Interrupt < 2]
	#print df[df.Interrupt<="2"]

	terminated=0
	restarted_cnt = 0
	#print df[:1][" Started"]
	
	for row in df.iterrows():
		#print t
		#terminated = len(df[df.Interrupt<="{0}".format(t)])
		terminated += len(df[df.Interrupt==str(t)])
		#print "Terminated: ",terminated

		# Count restarted processes
		terminated_time_this =  float(df[df.Interrupt==str(t)]["Terminated"])
		if int(t) < int(ana_tot_duration - ana_exec_time):
			terminated_time_next =  float(df[df.Interrupt==str(t+ana_exec_time)]["Terminated"])
			restarted = df[(df.Started > terminated_time_this) & (df.Started < terminated_time_next)]
		else:
			restarted = df[(df.Started > terminated_time_this) ]
		restarted_cnt += len(restarted)
		#print "restarted: ",restarted_cnt
		executing = nsims - terminated + restarted_cnt
		#print executing
		req_df.loc["{0}".format(t)] = [executing, terminated,0]
		if terminated == nsims:
			break
		#iter+=1

	req_df.loc["{0}".format(sim_arg)] = [restarted_cnt,terminated,nsims-terminated]	

	print terminated_time_this
	print df[df.Started > terminated_time_this]

	#print req_df
	ax = req_df.plot(kind='bar',stacked=False,ylim=(0,nsims+2), title="Cancel and restart every {0} seconds".format(ana_exec_time))
	ax.set_xlabel("Time (seconds)")
	ax.set_ylabel("Number of tasks")

	fig = plt.gcf()
	fig.set_size_inches(16,6)
	fig.savefig('plots/plot_interrupt_{0}.png'.format(ana_exec_time), dpi=100)
	