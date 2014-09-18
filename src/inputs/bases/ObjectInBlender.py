import bpy
import rospy
from . import InputBase
from mathutils import Vector

class ObjectInBlender(InputBase):
  """A base class that can be used to move an object in Blender space."""

  def set_object_location(self, point):
    self._confirm_object()
    # Go straight to _set_object_location() next time.
    self.set_object_location = self._set_object_location
    self.set_object_location(point)

  def _set_object_location(self, point):
    if self.confentry["enabled"]:
      offset = None
      if isinstance(self.binding["offset"], list):
        offset = Vector(self.binding["offset"])
      else:
        offset = bpy.data.objects[self.binding["offset"]].matrix_world.to_translation()
        # Check if vector and distance is set
        if 'direction' in self.binding:
          distance = 1
          if 'distance' in self.binding:
            distance = self.binding['distance']
          d = bpy.data.objects[self.binding["direction"]].location-offset
          d.normalize()
          offset = offset + d * distance
      self._location = offset + point * self.binding["scale"]
      bpy.data.objects[self.binding["name"]].location = self._location

  def _confirm_object(self):
    """Create object with name specified in config if it's not there."""
    if not self.binding["name"] in bpy.data.objects:
      bpy.ops.mesh.primitive_cube_add(radius=0.024)
      bpy.context.selected_objects[0].name = self.binding["name"]

  def _update_from_object(self):
    pass
    if self.binding["name"] in bpy.data.objects:
      self._location = bpy.data.objects[self.binding["name"]].location

  @property
  def location(self):
    self._update_from_object()
    return self._location

  def __init__(self, confentry):
    self.confentry = confentry
    self.binding = confentry["binding"]["objectpos"]
    self._location = Vector()
    self._update_from_object()