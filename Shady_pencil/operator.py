import bpy
from . import Shady_Pencil

class DATA_OT_GP_Shady_Pencil(bpy.types.Operator):
    
    bl_idname = "data.shady_pencil"
    bl_label = "Shady Pencil"
    bl_options = {'REGISTER','UNDO'}

    MODE : bpy.props.EnumProperty(items=[("DEFAULT","DEFAULT",""),("CURVES","CURVES",""),("GEOMETRY","GEOMETRY","")])

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

    extrusion_length: bpy.props.FloatProperty(
                                name="extrusion_length",
                                description="controlls the leght you want the regular layer extend in the normal direction",
                                default=0.01,
                                min=0.001,
                                max=50.0)
    
    start_frame: bpy.props.IntProperty(
                            name="start_frame",
                            description="start frame for the script to run on.",
                            default=0,
                            min=0,
                            max=2000)
            
    @classmethod
    def poll(cls, context):   

        try:
            bpy.data.collections[bpy.context.scene.output_collection]
            bpy.data.objects[bpy.context.scene.gp_obj_name]
            
            # Check to see if output collections are empty
            if len(bpy.data.collections[bpy.context.scene.output_collection].objects) > 0:
                return False
        except:
            return False

        try:

            if bpy.context.scene.sub_output_collection == '':
                return True

            elif len(bpy.data.collections[bpy.context.scene.sub_output_collection].objects) > 0:
                return False
        except:
            return False

        return True
    
    # SIMPLE JUST RUNS SOMETHING
    def execute(self, context):
        
        if self.poll(self):
            Shady_Pencil(gp_obj_name = self.gp_obj_name,
                        regular_layer = self.regular_layer,
                        output_collection = self.output_collection,
                        sub_layer = self.sub_layer,
                        sub_layer_extrution_amount = self.sub_layer_extrution_amount,
                        sub_output_collection = self.sub_output_collection,
                        merge_distance = self.merge_distance,
                        auto_delete_sub_layers = self.auto_delete_sub_layers,
                        start_frame = self.start_frame,extrusion_length = self.extrusion_length, 
                        MODE = self.MODE, close_curves = self.close_curves)
        
            return {'FINISHED'}
        
        return {'CANCELED'}

def register():
    
    bpy.utils.register_class(DATA_OT_GP_Shady_Pencil)
    
    
def unregister():
 
    bpy.utils.unregister_class(DATA_OT_GP_Shady_Pencil)
       
if __name__ == "__main__":
    register()