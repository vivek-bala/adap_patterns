import multiprocessing as mp
import subprocess as sp
from random import randint
import time
import pprint

tot_sim_tasks = 10
sim_kernel = "/bin/sleep"
sim_arg = "10"
max_sleep = 5

ana_min_exec_time = 1
ana_max_exec_time = 3
ana_tot_duration = 5

if __name__ == '__main__':

	proc_list = []
	out_list = []

	proc_info = dict()

	# Start first set of N tasks
	for i in range(tot_sim_tasks):

		#sim_arg = str(randint(0,max_sleep))
		exec_comm = [sim_kernel,sim_arg]
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
		exec_time = randint(ana_min_exec_time,ana_max_exec_time)
		time.sleep(exec_time)
		exec_time_cnt += exec_time

		#Pick a particular process - terminate if it is alive
		proc = proc_list.pop(randint(0,len(proc_list)-1))
		proc.terminate()

		# Record time process is Terminated
		proc_info[proc.pid]['Terminated'] = time.time()
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