import os
from sys import argv

os.system('mkdir results')

os.system('python NodeFailure/node_failure_benchmark.py -i '+argv[2])

os.system('python LinkFailure/link_failure_benchmark.py -i '+argv[2])

os.system('python DaemonFailure/pipeline_daemon_failure_benchmark.py -i '+argv[2])

os.system('python ProvenanceFailure/provenance_daemon_failure.py -i '+argv[2])