import multiprocessing as mp
import subprocess as sp
from random import randint
import time
import pprint
import uuid


sim_kernel = "/bin/sleep"
tot_sim_tasks = 10
sim_arg = 10

#ana_min_exec_time = 1
#ana_max_exec_time = 3
ana_exec_time = 1
ana_tot_duration = 10

if __name__ == '__main__':

	proc_list = []
	out_list = []

	proc_info = dict()


	assert ana_tot_duration <= sim_arg
	assert ana_exec_time <= ana_tot_duration

	# Start first set of N tasks
	for i in range(tot_sim_tasks):

		#sim_arg = str(randint(0,max_sleep))
		exec_comm = [sim_kernel, str(sim_arg)]
		proc = sp.Popen(exec_comm)

		# List of all processes
		proc_list.append(proc)

		# Record time process is Started
		proc_info[proc.pid] = dict()
		proc_info[proc.pid]['Started'] = time.time()
		#print 'Started: ', proc.pid, ': ', proc_info[proc.pid]


	
	# "Analysis"
	exec_time_cnt = 0

	# Interrupt till all processes haven't finished AND total time is less than max exec time
	while( (len(proc_list) is not 0) and (exec_time_cnt<=ana_tot_duration)):

		# Sleep for a random time
		#exec_time = randint(ana_min_exec_time,ana_max_exec_time)
		exec_time = ana_exec_time
		time.sleep(exec_time)
		exec_time_cnt += exec_time

		#Pick a particular process - terminate if it is alive
		proc = proc_list[randint(0,len(proc_list)-1)]


		if proc.poll() is None:
			proc.terminate()
			# Record time process is Terminated
			proc_info[proc.pid]['Terminated'] = time.time()
			proc_list.remove(proc)
			
		#print 'Terminated: ', proc.pid, ': ', proc_info[proc.pid]

	# Wait for all tasks to finish
	while(len(proc_list) is not 0):

		for proc in proc_list:
			if proc.poll() == 0:
				proc_list.remove(proc)

				# Record time process is Done
				proc_info[proc.pid]['Done'] = time.time()
				#print 'Done: ', proc.pid, ': ', proc_info[proc.pid]


	
	# Pretty print
	pprint.pprint(proc_info)

	# Write proc info record to file

	title = "pid, Started, Terminated, Done"

	f1 = open("execution_profile_nsims_{0}_simdur_{3}_anaexec_{1}_anatotdur_{2}.csv".format(tot_sim_tasks,
		ana_exec_time,
		ana_tot_duration,
		sim_arg),
	'w')

	f1.write("total no. of sims = {0} \n".format(tot_sim_tasks))
	f1.write("sim duration = {0} \n".format(sim_arg))
	f1.write("ana exec time = {0} \n".format(ana_exec_time))
	f1.write("ana tot duration = {0} \n".format(ana_tot_duration))

	f1.write("\n"+ title + "\n\n")

	for pid, vals in proc_info.iteritems():

		if "Terminated" in vals.keys():
			line = "{0}, {1}, {2}, None\n".format(pid, vals["Started"],vals["Terminated"])
			f1.write(line)

		elif "Done" in vals.keys():
			line = "{0}, {1}, None, {2}\n".format(pid, vals["Started"],vals["Done"])
			f1.write(line)

	f1.close()