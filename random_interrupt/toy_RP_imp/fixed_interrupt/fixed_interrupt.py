import radical.pilot as rp
from random import randint
import os
import sys
import time
import math
import pprint

sim_kernel = "/bin/sleep"
tot_sim_tasks = 12
sim_arg = 5

interrupt_time_period = 1
interrupt_total_duration = 5

unit_info = dict()

def pilot_state_cb (pilot, state) :
	print "Resource state has changed to {0}".format(state)

	if state == rp.FAILED:
		print "Pilot FAILED"
		sys.exit(1)

	if state == rp.DONE:
		print "Pilot DONE"

            	if state == rp.CANCELED:
                	print "Pilot CANCELED"


def unit_state_cb (unit, state) :

	print "Unit {0} state has changed to {1}".format(unit.uid,state)

	if state == rp.FAILED:
		raise "ComputeUnit error: STDERR: {0}, STDOUT: {0}"
		sys.exit(1)

	if state == rp.EXECUTING:
		unit_info[unit.uid] = dict()
		unit_info[unit.uid]['Started'] = time.time()

	if state == rp.DONE:
		unit_info[unit.uid]['Done'] = time.time()

if __name__ == "__main__":

	unit_list = []
	out_list = []

	# Sanity check
	assert interrupt_total_duration <= sim_arg
	assert interrupt_time_period <= interrupt_total_duration


	# Start RP related processes

	## Starting session
	db_url = os.getenv ("RADICAL_PILOT_DBURL", None)
	if db_url == None:
		db_url = "mongodb://vivek:hawkie91@ds039145.mongolab.com:39145/vivek_enmd"		
	session = rp.Session(database_url=db_url)

	## Session context
	c = rp.Context('ssh')
	#c.user_id = username
	session.add_context(c)

	## Starting Pilot Manager
	pmgr = rp.PilotManager(session=session)
	pmgr.register_callback(pilot_state_cb)

	# Creating a Pilot + Submitting
	pdesc = rp.ComputePilotDescription()
	pdesc.resource = "localhost"
	pdesc.runtime  = 10
	pdesc.cores    = 4

	#pdesc.queue = self._queue
	#pdesc.project = self._project

	pilot = pmgr.submit_pilots(pdesc)
	pilot.wait(rp.ACTIVE)

	# Creating Unit Manager
	umgr = rp.UnitManager(session=session, scheduler=rp.SCHED_DIRECT_SUBMISSION)
	umgr.add_pilots(pilot)
	umgr.register_callback(unit_state_cb)

	# Start first set of N tasks
	cud_list = list()
	for i in range(tot_sim_tasks):
		cud = rp.ComputeUnitDescription()
		cud.executable     = sim_kernel
		cud.arguments      = sim_arg

		cud_list.append(cud)

	# Submit all processes
	units = umgr.submit_units(cud_list)

	# "Analysis" process to randomly kill a process
	interrupt_time_cnt = 0

	# Interrupt till all processes haven't finished AND total time is less than max exec time
	while( (len(units) is not 0) and (interrupt_time_cnt<=int(math.ceil(tot_sim_tasks/pilot.description["cores"]))*interrupt_total_duration - 1)):

		# Sleep for a random time
		interrupt_time= interrupt_time_period
		time.sleep(interrupt_time)
		interrupt_time_cnt += interrupt_time

		# Create a list of executing units
		exec_units = [cu for cu in units if cu.state == "Executing"]
		#print interrupt_time_cnt,"Exec list: ", exec_units

		if len(exec_units) != 0:

			# Pick a particular process - terminate if it is alive
			candidate_unit =exec_units[randint(0,len(exec_units) - 1)]

			if candidate_unit.state == "Executing":
				candidate_unit.cancel()
				unit_info[candidate_unit.uid]["Terminated"] = time.time()
				unit_info[candidate_unit.uid]["Interrupt"] = interrupt_time_cnt
				print "Terminated unit: {0}".format(candidate_unit.uid)
				units.remove(candidate_unit)

		# Remove units already completed
		done_units = [cu for cu in units if cu.state == "Done"]
		for unit in done_units:
			units.remove(unit)

		
	# Wait for processes to finish
	uids = [cu.uid for cu in units]
	umgr.wait_units(uids)

	session.close(cleanup=False)

	# Pretty print
	pprint.pprint(unit_info)

	# Write proc info record to file

	title = "pid, Interrupt, Started, Terminated, Done"

	f1 = open("execution_profile_nsims_{0}_simdur_{3}_anaexec_{1}_anatotdur_{2}.csv".format(tot_sim_tasks,
		interrupt_time_period,
		interrupt_total_duration,
		sim_arg),
	'w')

	f1.write("total no. of sims = {0} \n".format(tot_sim_tasks))
	f1.write("sim duration = {0} \n".format(sim_arg))
	f1.write("interrupt time period= {0} \n".format(interrupt_time_period))
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