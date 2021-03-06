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
		header=7,sep=',',skipinitialspace=True)

	for i in range(len(df)):
		if df["Interrupt"][i] != "None":
			df["Interrupt"][i] = int(df["Interrupt"][i])

	#print df.sort("Interrupt")	


	# Plot with units as x-axis
	k = df["pid"]
	req_df = pd.DataFrame(columns=["Started","Terminated","Done"])

	for row in df.sort("pid").iterrows():
		started = row[1:][0]["Started"]
		terminated = 0
		done  = 0

		if row[1:][0]["Terminated"] != "None":
			terminated = float(row[1:][0]["Terminated"])
		else:
			terminated = None
		if row[1:][0]["Done"] != "None":
			done = float(row[1:][0]["Done"])
		else:
			done = None

		req_df.loc["{0}".format(row[1:][0]["pid"])] = [started,terminated,done]

	print req_df
	maxx = 0
	for k in df["Done"]:
		if k != "None":
			if maxx < float(k):
				maxx = float(k)

	ax = req_df.plot(kind='bar', ylim = (min(req_df["Started"])-100, maxx+100),rot=0)
	ax.set_xlabel("Tasks")
	ax.set_ylabel("Time (seconds)")

	fig = plt.gcf()
	fig.set_size_inches(16,6)
	fig.savefig('plots/plot_unit_status_anamin_{0}_anamax_{1}.png'.format(interrupt_min_time,interrupt_max_time), dpi=100)