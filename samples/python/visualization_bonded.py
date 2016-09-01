from __future__ import print_function
import espressomd._system as es
import espressomd
from espressomd import thermostat
from espressomd.interactions import HarmonicBond
from espressomd import visualization
import numpy

box_l = 10
n_part = 5

system = espressomd.System()
system.time_step = 0.01
system.cell_system.skin      = 0.4
system.thermostat.set_langevin(kT=1.0,gamma=1.0)

# integration
int_steps   = 250000
int_n_times = 500

system.box_l = [box_l,box_l,box_l]

system.non_bonded_inter[0,0].lennard_jones.set_params(
    epsilon=0, sigma=1,
    cutoff=2, shift="auto")
system.bonded_inter[0] = HarmonicBond(k=1.0,r_0=1.0)
system.bonded_inter[1] = HarmonicBond(k=1.0,r_0=1.0)

for i in range(n_part):
  system.part.add(id=i, pos=numpy.random.random(3) * system.box_l)

for i in range(n_part/2):
  system.part[i].add_bond((system.bonded_inter[0], system.part[i+1].id))
for i in range(n_part/2,n_part-1):
  system.part[i].add_bond((system.bonded_inter[1], system.part[i+1].id))

mayavi = visualization.mayavi_live(system)

j = 0
for i in range(0,int_n_times):
  print(i)
  system.integrator.run(int_steps)
  mayavi.update()
