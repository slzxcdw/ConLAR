import sys
import subprocess

from Queue import Queue
from observe.observe_component import ObserveComponent
from allocate.allocate_component import AllocateComponent
from predict.predict_component import PredictComponent
ac = AllocateComponent()
oc = ObserveComponent()
pc = PredictComponent()
oc.start()
pc.start()
ac.start()
while True:
	with open("start", "r") as conlar_stop:
		val = conlar_stop.read()
		if val == "-1":
			print "Terminating ..."
			oc.stop()
			pc.stop()
			ac.stop()
			oc.join()
			pc.join()
			ac.join()
			print "Components terminated"
			sys.exit()
