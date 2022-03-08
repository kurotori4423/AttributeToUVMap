import bpy
from bpy.props import StringProperty, FloatProperty, EnumProperty

bl_info = {
    "name": "Face Corner Attribute to UVMap",
    "author": "kurotori",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "location": "3D Viewport > Object",
    "description": "Export face corner (2D Vector) attribute to UVMap",
    "warning": "",
    "doc_url": "https://github.com/kurotori4423/AttributeToUVMap",
    "tracker_url": "https://github.com/kurotori4423/AttributeToUVMap/issues/new",
    "category": "Object"
}

class OBJECT_OT_AttributeToUVMap(bpy.types.Operator):

    bl_idname = "object.op_move_attribute_to_uvmap"
    bl_label = "Move Attribute to UVMap"
    bl_description = "Move Attribute to UVMap"
    bl_options = {'REGISTER', 'UNDO'}

    base_attributes = []

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.selected_objects

    select_attrib: StringProperty(options={'HIDDEN'})

    def execute(self, context):
        obj = context.active_object

        if self.select_attrib is "":
            self.report({'ERROR'}, 'No Face Corner attribute found!')
            return {'CANCELLED'}

        if obj.data.uv_layers.find(self.select_attrib) == -1:
            uvmap = obj.data.uv_layers.new(name=self.select_attrib)
        else:
            uvmap_index = obj.data.uv_layers.find(self.select_attrib)
            uvmap = obj.data.uv_layers[uvmap_index]

        # なぜかわからないけれど、uvmapを追加する前にuv_attributeの参照を追加していると、
        # uv_attributeのコレクションにロックがかかって参照できなくなる
        uv_attribute = obj.data.attributes[self.select_attrib]

        if uv_attribute is None:
            self.report({'ERROR'}, 'Attribute not found')
            return {'CANCELLED'}

        for loop in obj.data.loops:
            uvmap.data[loop.index].uv[0] = uv_attribute.data[loop.index].vector[0]
            uvmap.data[loop.index].uv[1] = uv_attribute.data[loop.index].vector[1]
        obj.data.attributes.remove(uv_attribute)
        self.report({'INFO'}, "Copy {} to UVMap.".format(self.select_attrib))

        return {'FINISHED'}

class OBJECT_MT_AttributeToUVMap(bpy.types.Menu):
    bl_idname = "object.mt_move_attribute_to_uvmap"
    bl_label = "Move Attribute to UVMap"
    bl_description = "Move Attribute to UVMap"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.selected_objects

    def draw(self, context):
        layout = self.layout
        
        # サブメニューの登録
        for attribute in context.active_object.data.attributes:
            if attribute.domain == 'CORNER' and attribute.data_type=="FLOAT2":
                ops = layout.operator(
                    OBJECT_OT_AttributeToUVMap.bl_idname, text=attribute.name
                )
                ops.select_attrib = attribute.name

def menu_fn(self, context):
    self.layout.separator()
    self.layout.menu(OBJECT_MT_AttributeToUVMap.bl_idname)


classes = [
    OBJECT_OT_AttributeToUVMap,
    OBJECT_MT_AttributeToUVMap,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_object.append(menu_fn)


def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_fn)
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()