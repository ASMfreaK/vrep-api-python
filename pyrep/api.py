from .vrep import vrep as v
from .common import ReturnCommandError
from .joints import Joints
from .sensors import Sensors
from .simulationstate import SimulationState


class VRepApi:
    def __init__(self, id):
        self._id = id
        self._def_op_mode = v.simx_opmode_oneshot_wait
        self.joint = Joints(id)  # type: Joints
        self.sensor = Sensors(id)  # type: Sensors
        self.simulation = SimulationState(id)  # type: SimulationState

    @staticmethod
    def connect(ip, port):
        res = v.simxStart(
            connectionAddress=ip,
            connectionPort=port,
            waitUntilConnected=True,
            doNotReconnectOnceDisconnected=True,
            timeOutInMs=5000,
            commThreadCycleInMs=5)
        if res == v.simx_return_ok:
            return VRepApi(res)
        else:
            raise ReturnCommandError(res)

    def __enter__(self):
        self.simulation.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.simulation.stop()

    def object_handle(api, name):
        code, obj = v.simxGetObjectHandle(api._id, name, api._def_op_mode)
        if code != v.simx_return_ok:
            raise ValueError("{} not found in scene or something bad happened!".format(name))
        return obj

    def relative_position(self, what, rel_to):
        code, pos = v.simxGetObjectPosition(self._id, what, rel_to, self._def_op_mode)
        if code != v.simx_return_ok:
            raise ValueError("{} not found in scene or something bad happened!".format(name))
        return pos

    def relative_orientation(self, what, rel_to):
        code, pos = v.simxGetObjectOrientation(self._id, what, rel_to, self._def_op_mode)
        if code != v.simx_return_ok:
            raise ValueError("{} not found in scene or something bad happened!".format(name))
        return pos

    def set_relative_position(self, what, rel_to, pos):
        v.simxSetObjectPosition(self._id, what, rel_to, pos, self._def_op_mode)
