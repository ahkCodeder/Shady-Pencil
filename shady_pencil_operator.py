import bpy
from . import Shady_Pencil
error_message = ""
class DATA_OT_GP_Shady_Pencil(bpy.types.Operator):

    bl_idname = "data.shady_pencil"
    bl_label = "Shady Pencil"
    bl_options = {'REGISTER', 'UNDO'}

    MODE: bpy.props.EnumProperty(items=[(
        "DEFAULT", "DEFAULT", ""), ("CURVES", "CURVES", ""), ("GEOMETRY", "GEOMETRY", ""), ("REPAIR", "REPAIR", ""), ("LINE", "LINE", "")])

    gp_obj_name: bpy.props.StringProperty(
        name="gp_obj_name",
        description="Grease Pencil Object Name Here",
        default="")

    regular_layer: bpy.props.StringProperty(
        name="regular_layer",
        description="Name of the layer that you want to turn into a Mesh",
        default="")

    output_collection: bpy.props.StringProperty(
        name="output_collection",
        description="name of the collection to out put to",
        default="")

    sub_layer: bpy.props.StringProperty(
        name="sub_layer",
        description="the layer that's used to sub tract from so that you can have holes",
        default="")

    sub_layer_extrution_amount: bpy.props.IntProperty(
        name="sub_layer_extrution_amount",
        description="sets the length of the sub layer you don't ",
        default=30,
        min=1,
        max=2000)

    sub_output_collection: bpy.props.StringProperty(
        name="sub_output_collection",
        description="name of the collection where subtract layer should out put to",
        default="")

    repair_collection: bpy.props.StringProperty(
        name="repair_collection",
        description="name of the collection to output the repair frame",
        default="")

    merge_angle: bpy.props.FloatProperty(
        name="merge_angle",
        description="controlls the detail of the mesh keep this number low it you want the out put to be good qualty",
        default=0.01,
        min=0.0,
        max=1.0)

    merge_distance: bpy.props.FloatProperty(
        name="merge_distance",
        description="controlls the detail of the mesh keep this number low it you want the out put to be good qualty",
        default=0.01,
        min=0.0,
        max=1.0)

    close_curves: bpy.props.BoolProperty(
        name="close_curves",
        description="this closes curves if selected",
        default=False)

    auto_delete_sub_layers: bpy.props.BoolProperty(
        name="auto_delete_sub_layers",
        description="this auto deletes the subtract layer",
        default=False)

    auto_remove_vertices_and_faces: bpy.props.BoolProperty(
            name="auto_remove_vertices_and_faces",
            description="this auto deletes all verices and faces",
            default=False)

    extrusion_length: bpy.props.FloatProperty(
        name="extrusion_length",
        description="controlls the leght you want the regular layer extend in the normal direction",
        default=0.01,
        min=0.001,
        max=50.0)

    complex_convert: bpy.props.BoolProperty(
        name="complex_convert",
        description="this converts the strokes useing a diffrent alorithem is slower but might work better for strokes that overlap",
        default=False)
    
    @classmethod
    def poll(cls, context):
        
        global error_message

        try:
            [area for area in bpy.context.screen.areas if area.type == "OUTLINER"][0]
            [area for area in bpy.context.screen.areas if area.type == "VIEW_3D"][0]
            [area for area in bpy.context.screen.areas if area.type ==
                "DOPESHEET_EDITOR"][0]
        except:
            
            error_message = "you need to have OUTLINE and VIEW_3D and DOPSHEET_EDITOR open"
            cls.poll_message_set(error_message)
            return False

        try:
            bpy.data.grease_pencils_v3[bpy.data.objects[bpy.context.scene.gp_obj_name].data.id_data.name_full]
        except:
            
            error_message = "the given grease pencil object dose not exist"
            cls.poll_message_set(error_message)
            return False

        try:
            bpy.data.grease_pencils_v3[bpy.data.objects[bpy.context.scene.gp_obj_name].data.id_data.name_full].layers[bpy.context.scene.regular_layer]   
        except:
            error_message = "the given regular layer dose not exist"
            cls.poll_message_set(error_message)
            return False

        if bpy.context.scene.MODE != "CURVES":
            if bpy.context.scene.merge_angle == 0.0 and bpy.context.scene.merge_distance == 0.0:
                error_message = "YOU NEED TO HAVE ONE OR BOTH MERGE ANGLE OR MERGE DISTANCE NOT TO BE 0.0"
                cls.poll_message_set(error_message)
                return False

        if bpy.context.scene.MODE != "REPAIR":
            try:

                if len(bpy.data.collections[bpy.context.scene.output_collection].objects) > 0:

                    error_message = "youre output collection needs to be EMPTY"
                    cls.poll_message_set(error_message)
                    return False
            except:

                error_message = "probly gave the wrong name for output collection"
                cls.poll_message_set(error_message)
                return False

        if bpy.context.scene.MODE == "DEFAULT" or bpy.context.scene.MODE == "GEOMETRY":
            try:
                if bpy.context.scene.sub_output_collection != "":

                    if len(bpy.data.collections[bpy.context.scene.sub_output_collection].objects) > 0:

                        error_message = "youre sub output collection needs to be EMPTY"
                        cls.poll_message_set(error_message)
                        return False

                    try:
                        bpy.data.grease_pencils_v3[bpy.data.objects[bpy.context.scene.gp_obj_name].data.id_data.name_full].layers[bpy.context.scene.sub_layer]
                    except:
                        error_message = "the given sub layer dose not exist"
                        cls.poll_message_set(error_message)
                        return False
            except:

                error_message = "probly gave the wrong name for sub output collection needs to be EMPTY"
                cls.poll_message_set(error_message)
                return False

        if bpy.context.scene.MODE == "REPAIR":
            try:
                if bpy.context.scene.repair_collection != "":

                    if len(bpy.data.collections[bpy.context.scene.repair_collection].objects) > 0:

                        error_message = "youre repair output collection needs to be EMPTY"
                        cls.poll_message_set(error_message)
                        return False
                else:
                    error_message = "you need to give a repair output collection"
                    cls.poll_message_set(error_message)
                    return False
            except:

                error_message = "probly gave the wrong name for repair output collection needs to be EMPTY"
                cls.poll_message_set(error_message)
                return False

        if bpy.context.scene.repair_collection == "" and bpy.context.scene.sub_output_collection == "" and bpy.context.scene.output_collection == "":

            error_message = "you NEED to pass one output collection"
            cls.poll_message_set(error_message)
            return False

        try:
            seleted_keyframes = []
            for f in bpy.data.grease_pencils_v3[bpy.data.objects[bpy.context.scene.gp_obj_name].data.id_data.name_full].layers[bpy.context.scene.regular_layer].frames:
                seleted_keyframes.append(int(f.frame_number))

            is_on_existing_key_frame = False
            for key_frame in seleted_keyframes:
                if int(bpy.data.scenes[0].frame_current) == key_frame:
                    is_on_existing_key_frame = True

            if not is_on_existing_key_frame:

                error_message = "move the the frame to a exising key frame of youre Greace pencil object"
                cls.poll_message_set(error_message)
                return False
        except:
            error_message = "this object has no key frames or SOMETHING ELSE went wrong"
            cls.poll_message_set(error_message)
            return False

        return True

    # SIMPLE JUST RUNS SOMETHING
    def execute(self, context):
        global error_message

        if self.poll(self):
            Shady_Pencil.Shady_Pencil(gp_obj_name=self.gp_obj_name,
                                      regular_layer=self.regular_layer,
                                      output_collection=self.output_collection,
                                      sub_layer=self.sub_layer,
                                      sub_layer_extrution_amount=self.sub_layer_extrution_amount,
                                      sub_output_collection=self.sub_output_collection,
                                      merge_angle=self.merge_angle,
                                      merge_distance=self.merge_distance,
                                      auto_delete_sub_layers=self.auto_delete_sub_layers,
                                      auto_remove_vertices_and_faces=self.auto_remove_vertices_and_faces,
                                      extrusion_length=self.extrusion_length,
                                      MODE=self.MODE, close_curves=self.close_curves,
                                      complex_convert=self.complex_convert, repair_collection=self.repair_collection)

            return {'FINISHED'}
        
        return {'CANCELED'}



def register():

    bpy.utils.register_class(DATA_OT_GP_Shady_Pencil)


def unregister():

    bpy.utils.unregister_class(DATA_OT_GP_Shady_Pencil)


if __name__ == "__main__":
    register()
