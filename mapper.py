import math
 
import rospy
 
from sensor_msgs.msg  import LaserScan
from nav_msgs.msg import OccupancyGrid
from nav_msgs.msg import MapMetaData
 
ranges = []
 
rospy.init_node("mappet")
pub = rospy.Publisher("/map", OccupancyGrid, queue_size=10)
 
 
def laser_cb(scan):
    global ranges
    ranges = scan.ranges
 
_mdata = MapMetaData()
_map = OccupancyGrid()
 
_mdata.resolution = 0.1
_mdata.width = 50
_mdata.height = 50
 
_mdata.origin.position.x = -(_mdata.width * _mdata.resolution /2)
_mdata.origin.position.y = -(_mdata.height * _mdata.resolution /2)
_mdata.origin.orientation.w = 1.0
 
_map.info = _mdata
 
def map_assembly():
    _map.data = [-1 for i in range(_mdata.width*_mdata.height)]
    angle = 0
    for i in ranges:
        if i > 4:
            x = 0
            y = 0
        else:
            rad_angle = math.radians(angle)
            x = i * math.cos(rad_angle)
            y = i * math.sin(rad_angle)
        if (x == 0 and y == 0):
            pass
        else:
            #print(int(y * _mdata.width * _mdata.resolution) + int(x * _mdata.resolution))
            #print("x:", x, " y: " ,y, " angle: ", angle, "dist: ", math.sqrt(x*x+y*y))
            _map.data[int(y / _mdata.resolution) * (_mdata.width) + int(x / _mdata.resolution) + 
                            int((_mdata.width+1)*_mdata.height/ 2)] = 100
            angle += 1
        _map.data[2499] = 1
        _map.data[0] = 127
        _map.data[49] = 110
        
seq = 0
 
rospy.Subscriber("/scan", LaserScan, laser_cb)
rospy.sleep(0.5)
 
while not rospy.is_shutdown():
    seq += 1
    _map.header.seq = seq
    pub.publish(_map)
    map_assembly()
    rospy.sleep(2)
