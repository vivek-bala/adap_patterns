import radical.pilot as rp
from random import randint
import os
import sys
import time
import math
import pprint

sim_kernel = "/bin/sleep"
tot_sim_tasks = 10
sim_arg = 50

interrupt_total_duration = 50

interrupt_min_tasks = 1
interrupt_max_tasks = 3

interrupt_gap_min = 10
interrupt_gap_max = 15

os.environ['RADICAL_PILOT_PROFILE'] = "True"

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


if __name__ == "__main__":

	unit_list = []
	out_list = []

	# Sanity check
	assert interrupt_total_duration <= sim_arg


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
	pdesc.runtime  = 20
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
		interrupt_time= randint(interrupt_gap_min,interrupt_gap_max)
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
				units.remove(candidate_unit)

		# Remove units already completed
		done_units = [cu for cu in units if cu.state == "Done"]
		for unit in done_units:
			units.remove(unit)

		
	# Wait for processes to finish
	uids = [cu.uid for cu in units]
	umgr.wait_units(uids)

	session.close(cleanup=False)



	import radical.pilot.utils as rpu

	# we have a session
	sid        = session.uid
	profiles   = rpu.fetch_profiles(sid=sid, tgt='/tmp/')
	profile    = rpu.combine_profiles (profiles)
	frame      = rpu.prof2frame(profile)
	sf, pf, uf = rpu.split_frame(frame)

	rpu.add_info(uf)

	rpu.add_states(uf)
	adv = uf[uf['event'].isin(['advance'])]
	rpu.add_frequency(adv, 'f_exe', 0.5, {'state' : 'Executing', 'event' : 'advance'})

	s_frame, p_frame, u_frame = rpu.get_session_frames(sid)
	#print str(u_frame)

	info = ["uid",	"Unscheduled", 
			"StagingInput", 
			"AgentStagingInputPending",
			"AgentStagingInput",
			"AllocatingPending",
			"Allocating",
			"ExecutingPending",
			"Executing",
			"AgentStagingOutputPending",
			"AgentStagingOutput",
			"StagingOutput",
			"Canceled",
			"Done"]
	u_frame.to_csv("execution_profile_nsims_{0}_simdur_{3}_anamin_{1}_anamax{5}_anatotdur_{2}_max_{4}.csv".format(tot_sim_tasks,
		interrupt_gap_min,
		interrupt_total_duration,
		sim_arg,
		interrupt_max_tasks,
		interrupt_gap_max), sep=',', columns = info, header = info)