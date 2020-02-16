from simulator.road.road import Road


class Dispatcher:
    road: Road

    def __init__(self, road: Road):
        self.road = road

    def dispatch(self) -> None:
        '''
        Adds vehicles to the road.
        :return: None.
        '''
        raise NotImplementedError
