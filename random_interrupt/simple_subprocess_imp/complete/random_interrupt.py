import subprocess as sp
from random import randint
import time
import pprint


sim_kernel = "/bin/sleep"
tot_sim_tasks = 10
sim_arg = 50

interrupt_total_duration = 50

interrupt_min_tasks = 1
interrupt_max_tasks = 3

interrupt_gap_min = 10
interrupt_gap_max = 15

if __name__ == '__main__':

	proc_list = []
	out_list = []
	proc_info = dict()

	# Sanity check
	assert interrupt_total_duration <= sim_arg

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
	interrupt_time_cnt = 0

	# Interrupt till all processes haven't finished AND total time is less than max exec time
	while( (len(proc_list) is not 0) and (interrupt_time_cnt<(interrupt_total_duration - interrupt_gap_max))):

		# Sleep for a random time
		interrupt_time = randint (interrupt_gap_min,interrupt_gap_max)
		time.sleep(interrupt_time)
		interrupt_time_cnt += interrupt_time

		#Pick a particular process - terminate if it is alive
		num_int_tasks = randint(interrupt_min_tasks,interrupt_max_tasks)
		for i in range(num_int_tasks):
			proc = proc_list[randint(0,len(proc_list)-1)]

			if proc.poll() is None:
				proc.terminate()

				# Record time process is Terminated
				proc_info[proc.pid]['Terminated'] = time.time()
				proc_info[proc.pid]['Interrupt'] = interrupt_time_cnt
				proc_list.remove(proc)
			

				# Start next process
				exec_comm = [sim_kernel, str(sim_arg)]
				proc = sp.Popen(exec_comm)

				# List of all processes
				proc_list.append(proc)

				# Record time process is Started
				proc_info[proc.pid] = dict()
				proc_info[proc.pid]['Started'] = time.time()

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
	#pprint.pprint(proc_info)

	# Write proc info record to file

	title = "pid, Interrupt, Started, Terminated, Done"

	f1 = open("execution_profile_nsims_{0}_simdur_{3}_anamin_{1}_anamax{5}_anatotdur_{2}_max_{4}.csv".format(tot_sim_tasks,
		interrupt_gap_min,
		interrupt_total_duration,
		sim_arg,
		interrupt_max_tasks,
		interrupt_gap_max),
	'w')

	f1.write("total no. of sims = {0} \n".format(tot_sim_tasks))
	f1.write("sim duration = {0} \n".format(sim_arg))
	f1.write("interrupt min time = {0} \n".format(interrupt_gap_min))
	f1.write("interrupt max time = {0} \n".format(interrupt_gap_max))
	f1.write("interrupt min tasks = {0} \n".format(interrupt_min_tasks))
	f1.write("interrupt max tasks = {0} \n".format(interrupt_max_tasks))
	f1.write("interrupt_total_duration = {0} \n".format(interrupt_total_duration))

	f1.write("\n"+ title + "\n\n")

	for pid, vals in proc_info.iteritems():

		if "Terminated" in vals.keys():
			line = "{0}, {1}, {2:0.5f}, {3:0.5f}, None\n".format(pid, vals["Interrupt"], vals["Started"],vals["Terminated"])
			f1.write(line)

		elif "Done" in vals.keys():
			line = "{0}, None, {1:0.5f}, None, {2:0.5f}\n".format(pid, vals["Started"],vals["Done"])
			f1.write(line)

	f1.close()
