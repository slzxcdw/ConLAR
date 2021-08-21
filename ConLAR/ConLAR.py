import sys
import subprocess

from Queue import Queue
from observe.observe_component import ObserveComponent
from act.act_component import ActComponent
from predict.predict_component import PredictComponent
ac = ActComponent()
oc = ObserveComponent()
pc = PredictComponent()
oc.start()
pc.start()
#dc.start()
ac.start()
while True:
	with open("start", "r") as cap_stop:
		val = cap_stop.read()

		if val == "1":
			print "Terminating ..."
			oc.stop()
			pc.stop()
			#dc.stop()
			ac.stop()
			
			oc.join()
			pc.join()
			#dc.join()
			ac.join()
			print "Components terminated"
			sys.exit()
	
	subprocess.call(["sleep", str(3)])
