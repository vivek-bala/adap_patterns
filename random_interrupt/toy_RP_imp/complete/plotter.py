import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":

	nsims = 10
	sim_arg = 50

	ana_tot_duration = 50

	interrupt_min_tasks = 1
	interrupt_max_tasks = 3

	interrupt_min_time = 10
	interrupt_max_time = 15

	# Read given CSV
	df = pd.read_csv('execution_profile_nsims_{0}_simdur_{1}_anamin_{2}_anamax{3}_anatotdur_{4}_max_{5}.csv'.format(nsims,
		sim_arg,
		interrupt_min_time,
		interrupt_max_time,
		ana_tot_duration,
		interrupt_max_tasks),
		header=0,sep=',')

	#print df

	req_df = df[["uid","Executing","Canceled","Done"]].sort("Executing")
	print req_df

	req_df = req_df.T.drop("uid")
	#print req_df
	

	ax = req_df.plot(kind='barh',color=["red","blue","green"])
	ax.set_ylabel("Tasks")
	ax.set_xlabel("Time (seconds)")

	fig = plt.gcf()
	fig.set_size_inches(16,6)
	fig.savefig('plot_test.png'.format(interrupt_min_time,interrupt_max_time), dpi=100)
	