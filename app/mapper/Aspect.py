import UserIdMap
import TimeslotIdMap

import UserMapper
import TimeslotMapper

def wrap_find(func, id_map_object):
    def new_find(objectId):
        user = id_map_object.find(int(objectId))
        if user is not None:
            print(id_map_object.__name__ + ' - find() - Cache HIT')
            return user
        print(id_map_object.__name__ + ' -  find() - Cache MISS')
        result = func(objectId)
        if not result:
            return
        else:
            id_map_object.addTo(result)
        return result
    return new_find

def wrap_makeNew(func, id_map_object):
    def new_makeNew(*args):
        result = func(*args)
        print(id_map_object.__name__  + ' - Added a new object')
        id_map_object.addTo(result)
        return result
    return new_makeNew

def wrap_delete(func, id_map_object):
    def new_delete(objectId):
        result = func(objectId)
        object = id_map_object.find(objectId)
        if object is not None:
            id_map_object.removeFrom(object)
            print(id_map_object.__name__  + ' - Deleted an object')
        return result
    return new_delete

UserMapper.find = wrap_find(UserMapper.find, UserIdMap)
UserMapper.makeNew = wrap_makeNew(UserMapper.makeNew, UserIdMap)
UserMapper.delete = wrap_delete(UserMapper.delete, UserIdMap)

TimeslotMapper.find = wrap_find(TimeslotMapper.find, TimeslotIdMap)
TimeslotMapper.makeNew = wrap_makeNew(TimeslotMapper.makeNew, TimeslotIdMap)
TimeslotMapper.delete = wrap_delete(TimeslotMapper.delete, TimeslotIdMap)

print('--- Attached Aspects successfully ----')
