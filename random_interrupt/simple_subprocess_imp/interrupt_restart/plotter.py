import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":

	nsims = 10
	sim_arg = 50
	ana_exec_time = 5
	ana_tot_duration = 50

	# Read given CSV
	df = pd.read_csv('execution_profile_nsims_{0}_simdur_{1}_anaexec_{2}_anatotdur_{3}.csv'.format(nsims,sim_arg,
		ana_exec_time,
		ana_tot_duration),
		header=4,sep=',',skipinitialspace=True)

	df = df.sort("Interrupt")
	print df
	#print df[df.Interrupt<="20"].count()

	# Construct required DF

	req_df = pd.DataFrame(columns=["Executing","Terminated","Done"])
	req_df.loc["0"] = [nsims,0,0]

	#print df[df.Interrupt < 2]
	#print df[df.Interrupt<="2"]

	terminated=0
	restarted_cnt = 0
	#print df[:1][" Started"]
	
	for t in range(ana_exec_time, ana_tot_duration, ana_exec_time):
		#print t
		#terminated = len(df[df.Interrupt<="{0}".format(t)])
		terminated += len(df[df.Interrupt==str(t)])
		print "Terminated: ",terminated

		# Count restarted processes
		terminated_time_this =  float(df[df.Interrupt==str(t)]["Terminated"])
		if int(t) < int(ana_tot_duration - ana_exec_time):
			terminated_time_next =  float(df[df.Interrupt==str(t+ana_exec_time)]["Terminated"])
			restarted = df[(df.Started > terminated_time_this) & (df.Started < terminated_time_next)]
		else:
			restarted = df[(df.Started > terminated_time_this) ]
		restarted_cnt += len(restarted)
		print "restarted: ",restarted_cnt
		executing = nsims - terminated + restarted_cnt
		#print executing
		req_df.loc["{0}".format(t)] = [executing, terminated,0]
		if terminated == nsims:
			break
		#iter+=1

	req_df.loc["{0}".format(sim_arg)] = [restarted_cnt,terminated,nsims-terminated]	

	#print req_df
	ax = req_df.plot(kind='bar',stacked=False,ylim=(0,nsims+2))
	ax.set_xlabel("Time (seconds)")
	ax.set_ylabel("Number of tasks")

	fig = plt.gcf()
	fig.set_size_inches(16,6)
	fig.savefig('plots/plot_interrupt_{0}.png'.format(ana_exec_time), dpi=100)
	