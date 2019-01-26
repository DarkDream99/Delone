import copy

NEW_STAGE = "new_stage"
ADD_SEGMENT = "add_segment"
DELETE_SEGMENT = "delete_segment"
ADD_BASE_SEGMENT = "add_base_segment"
DELETE_BASE_SEGMENT = "delete_base_segment"
CHECK_SEGMENT = "check_segment"

SELECT_POINT = "select_point"
DESELECT_POINT = "deselect_point"
SELECT_BASE_POINT = "select_base_point"

ADD_LOCATION_ROOT = "add_location_root"
ADD_LOCATION_LAYER = "add_location_layer"
REFERENCE_TO_LOCATION_LAYER = "reference_to_location_layer"


class Event (object):

    def __init__(self, ev_type, data=None, description=""):
        self._event_type = ev_type
        self._data = data
        self._description = description

    @property
    def type(self):
        return self._event_type

    @property
    def data(self):
        return copy.deepcopy(self._data)

    @property
    def description(self):
        return self._description
