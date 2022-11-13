import bpy

class VIEW3D_PT_GP_Shady_Pencil(bpy.types.Panel):
    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Shady Pencil"
    bl_label = "Shady Pencil"
    


    def draw(self,context):
        
        props = self.layout.operator("data.shady_pencil",text="Run")
        
        col = self.layout.column(align=True)
        
        col.prop(context.scene,'MODE')

        props.MODE = context.scene.MODE

        if props.MODE == "DEFAULT":

            col.prop(context.scene,'gp_obj_name')

            col.prop(context.scene,'regular_layer')

            col.prop(context.scene,'output_collection')

            col.prop(context.scene, 'sub_layer')

            col.prop(context.scene,'sub_output_collection')

            col.prop(context.scene,'sub_layer_extrution_amount')

            col.prop(context.scene,'merge_distance')

            col.prop(context.scene,'auto_delete_sub_layers')

            col.prop(context.scene,'start_frame')

            props.MODE = context.scene.MODE

            props.gp_obj_name = context.scene.gp_obj_name

            props.regular_layer = context.scene.regular_layer

            props.output_collection = context.scene.output_collection

            props.sub_layer = context.scene.sub_layer

            props.sub_layer_extrution_amount = context.scene.sub_layer_extrution_amount

            props.sub_output_collection = context.scene.sub_output_collection

            props.merge_distance = context.scene.merge_distance

            props.auto_delete_sub_layers = context.scene.auto_delete_sub_layers

            props.start_frame = context.scene.start_frame 

        elif props.MODE == "CURVES":
            
            col.prop(context.scene,'gp_obj_name')

            col.prop(context.scene,'regular_layer')  

            col.prop(context.scene,'output_collection')

            col.prop(context.scene, 'close_curves')

            col.prop(context.scene,'start_frame')

            props.MODE = context.scene.MODE

            props.gp_obj_name = context.scene.gp_obj_name
            
            props.regular_layer = context.scene.regular_layer
            
            props.output_collection = context.scene.output_collection
            
            props.close_curves = context.scene.close_curves

            props.sub_layer = ""

            props.sub_output_collection = ""

            props.start_frame = context.scene.start_frame 

        elif props.MODE == "GEOMETRY":

            col.prop(context.scene,'gp_obj_name')

            col.prop(context.scene,'regular_layer')  

            col.prop(context.scene,'output_collection')

            col.prop(context.scene,'extrusion_length')

            col.prop(context.scene, 'sub_layer')

            col.prop(context.scene,'sub_output_collection')

            col.prop(context.scene,'sub_layer_extrution_amount')

            col.prop(context.scene,'start_frame')

            props.MODE = context.scene.MODE

            props.gp_obj_name = context.scene.gp_obj_name
            
            props.regular_layer = context.scene.regular_layer
            
            props.output_collection = context.scene.output_collection

            props.extrusion_length = context.scene.extrusion_length

            props.sub_layer = context.scene.sub_layer 

            props.sub_output_collection = context.scene.sub_output_collection

            props.sub_layer_extrution_amount = context.scene.sub_layer_extrution_amount
            
            props.start_frame = context.scene.start_frame

def register():
    
    bpy.types.Scene.MODE = bpy.props.EnumProperty(items=[("DEFAULT","DEFAULT",""),("CURVES","CURVES",""),("GEOMETRY","GEOMETRY","")])

    bpy.types.Scene.gp_obj_name = bpy.props.StringProperty(
                                    name="gp_obj_name",
                                    description="Grease Pencil Object Name Here",
                                    default="") 
    
    bpy.types.Scene.regular_layer = bpy.props.StringProperty(
                                    name="regular_layer",
                                    description="Name of the layer that you want to turn into a Mesh",
                                    default="")    
    
    bpy.types.Scene.output_collection = bpy.props.StringProperty(
                                    name="output_collection",
                                    description="name of the collection to out put to",
                                    default="")   
    
    bpy.types.Scene.sub_layer = bpy.props.StringProperty(
                                    name="sub_layer",
                                    description="the layer that's used to sub tract from so that you can have holes",
                                    default="")   
    
    bpy.types.Scene.sub_layer_extrution_amount = bpy.props.IntProperty(
                            name="sub_layer_extrution_amount",
                            description="sets the length of the sub layer you don't ",
                            default=30,
                            min=1,
                            max=2000)
    
    bpy.types.Scene.sub_output_collection = bpy.props.StringProperty(
                                    name="sub_output_collection",
                                    description="name of the collection where subtract layer should out put to",
                                    default="")   
    
    bpy.types.Scene.merge_distance = bpy.props.FloatProperty(
                                name="merge_distance",
                                description="controlls the detail of the mesh keep this number low it you want the out put to be good qualty",
                                default=0.01,
                                min=0.0,
                                max=1.0)     
     
    bpy.types.Scene.auto_delete_sub_layers = bpy.props.BoolProperty(
                                    name="auto_delete_sub_layers",
                                    description="this auto deletes the subtract layer",
                                    default=False)
    
    bpy.types.Scene.close_curves = bpy.props.BoolProperty(
                                    name="close_curves",
                                    description="this closes curves if selected",
                                    default=False)
    
    bpy.types.Scene.extrusion_length = bpy.props.FloatProperty(
                                name="extrusion_length",
                                description="controlls the leght you want the regular layer extend in the normal direction",
                                default=0.01,
                                min=0.001,
                                max=50.0)
    
    bpy.types.Scene.start_frame = bpy.props.IntProperty(
                            name="start_frame",
                            description="start frame for the script to run on.",
                            default=0,
                            min=0,
                            max=2000)
                             
    bpy.utils.register_class(VIEW3D_PT_GP_Shady_Pencil)

    
    
def unregister():
    
    del bpy.types.Scene.MODE

    del bpy.types.Scene.gp_obj_name

    del bpy.types.Scene.regular_layer

    del bpy.types.Scene.output_collection

    del bpy.types.Scene.sub_layer

    del bpy.types.Scene.sub_layer_extrution_amount

    del bpy.types.Scene.sub_output_collection

    del bpy.types.Scene.merge_distance

    del bpy.types.Scene.auto_delete_sub_layers

    del bpy.types.Scene.close_curves

    del bpy.types.Scene.extrusion_length

    del bpy.types.Scene.start_frame     
                            
    bpy.utils.unregister_class(VIEW3D_PT_GP_Shady_Pencil)

       
if __name__ == "__main__":
    register()