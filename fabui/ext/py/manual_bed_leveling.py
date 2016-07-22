#!/bin/env python
# -*- coding: utf-8; -*-
#
# (c) 2016 FABtotum, http://www.fabtotum.com
#
# This file is part of FABUI.
#
# FABUI is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# FABUI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with FABUI.  If not, see <http://www.gnu.org/licenses/>.

# Import standard python module
import argparse
import time
import gettext
import numpy as np
import re

# Import external modules
from threading import Event, Thread

# Import internal modules
from fabtotum.fabui.config  import ConfigService
from fabtotum.fabui.gpusher import GCodePusher
import fabtotum.fabui.macros.general as general_macros
import fabtotum.fabui.macros.printing as print_macros

# Set up message catalog access
tr = gettext.translation('manual_bed_leveling', 'locale', fallback=True)
_ = tr.ugettext

################################################################################

class ManualBedLeveling(GCodePusher):

    PROBE_POINTS  = [
                        [5+17,      5+61.5,     0.0], # (1)
                        [5+17,      148.5+61.5, 0.0], # (2)
                        [178+17,    148.5+61.5, 0.0], # (3)
                        [178+17,    5+61.5,     0.0]  # (4)
                    ]
    # First screw offset (lower left corner)
    SCREW_OFFSET        = [8.726, 10.579, 0]
    SCREW_PITCH         = 0.5 # mm/deg
    CARRIAGE_POSITION   = [17, 61.5]
    # Default offsets
    MILLING_OFFSET      = 0.0
    PROBE_SECURE_OFFSET = 15.0    
    # Movement speed
    XY_FEEDRATE         = 5000
    Z_FEEDRATE          = 1500
    E_FEEDRATE          = 800
    
    def __init__(self, log_trace, monitor_file, config):
        super(ManualBedLeveling, self).__init__(log_trace, monitor_file, config=config)
        
        self.bed_leveling_stats = {
            'screw_1' : [0.0, 0.0, 0.0], # [turns, degree, height]
            'screw_2' : [0.0, 0.0, 0.0],
            'screw_3' : [0.0, 0.0, 0.0],
            'screw_4' : [0.0, 0.0, 0.0],
        }
        
        self.add_monitor_group('bed_leveling', self.bed_leveling_stats)

    def trace(self, msg):
        print msg

    def probe(self, x, y, timeout = 90):
        """ 
        Probe Z at specific (X,Y). Returns Z or ``None`` on failure.
        
        :param x: X position
        :param y: Y position
        :rtype: float
        """
        self.send('G0 X{0} Y{1} F{2}'.format(x, y, self.XY_FEEDRATE) )
        
        reply = self.send('G30', expected_reply = 'echo:', timeout = timeout)
        if reply:            
            z = float( reply[-1].split("Z:")[1].strip() )
            z = round(z, 3)  # round to 3 decimanl points
            return [x,y,z,1]
            
        return None

    def fitplane(self, XYZ):
        [npts,rows] = XYZ.shape

        if not rows == 3:
            #print XYZ.shape
            raise ('data is not 3D')
            return None

        if npts < 3:
            raise ('too few points to fit plane')
            return None

        # Set up constraint equations of the form  AB = 0,
        
        # where B is a column vector of the plane coefficients
        # in the form   b(1)*X + b(2)*Y +b(3)*Z + b(4) = 0.
        t = XYZ
        p = (np.ones((npts,1)))
        A = np.hstack([t,p])

        if npts == 3:                       # Pad A with zeros
            A = [A, np.zeros(1,4)]

        [u, d, v] = np.linalg.svd(A)        # Singular value decomposition.
        #print v[3,:]
        B = v[3,:];                         # Solution is last column of v.
        nn = np.linalg.norm(B[0:3])
        B = B / nn
        #plane = Plane(Point(B[0],B[1],B[2]),D=B[3])
        #return plane
        return B[:]

    def run(self, task_id, num_probes, skip_homing):
        """
        """

        probe_height    = 50.0
        milling_offset  = self.MILLING_OFFSET
        
        # Get probe length
        data = self.send("M503")
        for line in data:
            if line.startswith("echo:Z Probe Length:"):
                probe_length = abs(float(line.split("Z Probe Length: ")[1]))
                probe_height = (probe_length + 1) + self.PROBE_SECURE_OFFSET
                    

        self.prepare_task(task_id, task_type='bed_leveling')
        self.set_task_status(GCodePusher.TASK_STARTED)
        
        self.trace( _("Manual bed leveling started.") )
        try:
            safety_door = self.config.get('settings', 'safety')['door']
        except KeyError:
            safety_door = 0
    
        if safety_door == 1:
            self.macro("M741",  "TRIGGERED",    2,  _("Front panel door control"), 1, verbose=False)
        
        # If milling bed side up, add milling sacrificial layer offset to probe_height
        self.macro("M744",  "TRIGGERED",    2,  _("Milling bed side up"),  1, warning=True, verbose=False)
        if self.macro_warning != 0:
            self.macro_warning = 0

            try:
                milling_offset = float(config.get('settings', 'milling')['layer-offset'])
                self.trace("Milling sacrificial layer thickness: "+str(milling_offset))
                probe_height += milling_offset
            except KeyError:
                trace("Milling sacrificial layer thickness not configured - assuming zero")

        self.macro("M402",  "ok",   2,  _("Retracting Probe (safety)"), 0.1, warning=True, verbose=False)
        self.macro("G90",   "ok",   5,  _("Setting abs mode"),          0.1, verbose=False)
        
        if not skip_homing:
            self.macro("G27",           "ok",   100,    _("Homing Z - Fast"), 0.1 )
            self.macro("G92 Z241.2",    "ok",   5,      _("Setting correct Z"), 0.1, verbose=False)
            self.macro("M402",          "ok",   2,      _("Retracting Probe (safety)"), 1, verbose=False)

        self.macro("G0 Z{0} F5000".format(probe_height),    "ok",   5,  _("Moving to start Z height"), 10) #mandatory!
        self.send("M400")

        self.send("M401")
        
        probed_points = np.array(self.PROBE_POINTS)            
        print probed_points

        for (p,point) in enumerate(self.PROBE_POINTS):        
            self.trace( _("Measuring point {0} of {1} ({2} times)").format( str(p+1), len(self.PROBE_POINTS), num_probes) )
        
            # Real carriage position
            x = point[0] - self.CARRIAGE_POSITION[0]
            y = point[1] - self.CARRIAGE_POSITION[1]
            
            probed_points[p,2] = 0.0
            probes = 0
            
            for i in xrange(0, num_probes):
                print "x: {0}, y: {1} / {2}".format(x,y, i)
                new_point = self.probe(x, y, timeout = 20)
                if new_point:
                    probes += 1
                    probed_points[p,2] += new_point[2]
                else:
                    print "Error probing"
                
                self.macro("G0 Z{0} F5000".format(probe_height),    "ok",   5,  _("Rising Bed."), 10)
        
            probed_points[p,2] /= probes
        
            print probed_points[p,2]
        
        # Retract probe
        self.send("M402")
        self.send("G0 X5 Y5 Z{0} F10000".format(probe_height))
        self.send("M18")
        
        # Offset from the first calibration screw (lower left)
        probed_points = np.add(probed_points, self.SCREW_OFFSET)
        
        # Math
        Fit = self.fitplane(probed_points)
        coeff = Fit[0:3]
        d = Fit[3]
        
        # Calibration Points of the screws
        cal_point = np.array([
                    [0.0-8.726, 0.0-10.579,     0.0],
                    [0.0-8.726, 257.5-10.579,   0.0],
                    [223-8.726, 257.5-10.579,   0.0],
                    [223-8.726, 0.0-10.579,     0.0]
                ])
        
        for p,point in enumerate(cal_point):
            z = (-coeff[0]*point[0] - coeff[1]*point[1] +d)/coeff[2]
                
            # Difference from titled plane to straight plane
            # Distance = P2-P1
            diff = abs(d)-abs(z)
            
            # Number of screw turns, pitch 0.5mm
            turns   = round(diff/0.5, 2) #
            degrees = turns*360
            # Lets round to upper 5 degrees
            degrees = int(5 * round(float(degrees)/5))
            
            screw_label = 'screw_{0}'.format(p+1)
            self.bed_leveling_stats[screw_label][0] = str(turns)
            self.bed_leveling_stats[screw_label][1] = str(degrees)
            self.bed_leveling_stats[screw_label][2] = str( round(diff, 5) )
            
            print "Calculated=" + str(z) + " Difference " + str(diff) +" Turns: "+ str(turns) + " deg: " + str(degrees)
        
        # Make sure the new data is written to the monitor file
        self.update_monitor_file()
        
        self.send("M300")
        self.trace( _("Manual bed leveling finished.") )
        self.set_task_status(GCodePusher.TASK_COMPLETED)
        
        self.stop()

def main():
    config = ConfigService()

    # SETTING EXPECTED ARGUMENTS
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("task_id",                                  help=_("Task ID.") )
    parser.add_argument("-n", "--num_probes",                       help=_("Number of probings per screw."),     default=4)
    parser.add_argument("-s", "--skip_homing", action='store_true', help=_("Skip homing.") )

    # GET ARGUMENTS
    args = parser.parse_args()

    # INIT VARs
    task_id         = int(args.task_id)
    monitor_file    = config.get('general', 'task_monitor')
    log_trace       = config.get('general', 'trace') 
    num_probes      = args.num_probes
    skip_homing     = args.skip_homing

    app = ManualBedLeveling(log_trace, monitor_file, config=config)

    app_thread = Thread( 
            target = app.run, 
            args=( [task_id, num_probes, skip_homing] ) 
            )
    app_thread.start()

    app.loop()          # app.loop() must be started to allow callbacks
    app_thread.join()

if __name__ == "__main__":
    main()