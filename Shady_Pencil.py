bl_info = {
    "name": "Shady Pencil",
    "author": "AHK <https://github.com/ahkCodeder>",
    "version": (1,0),
    "blender": (3,3,0),
    "category": "Add Grease Pencil",
    "location": "",
    "description": "This turns Grease pencil strokes into Mesh Objects",
    "warning": "Lines can't be turned to Mesh obj",
    "doc_url": "https://github.com/ahkCodeder",
    "tracer_url": ""
}

import bpy
"""
########################## REQUIERMENTS ###########################################
"""
# 1 WINDOWS THAT NEED TO BE ACTIVLY OPENED 

# 3D VIEW
# DOPE SHEET
# OUTLINER

# 2 SETTINGS NEED TO BE RIGHT FOR WITH WHAT YOU WANT AND THE RIGHT COLLECTIONS TO OUTPUT TO 

# 3 MAKE SURE YOU HAVE A STROKE ON THE START FRAME OF THE ANIMATION OR YOU CAN GET A CONTEXT ERROR

"""
########################## END OF REQUIERMENTS ###########################################
"""

"""
############################ SETTING VARIABLES ####################################
"""

# CONTROLLS THE DISTANCE OBJECTS ARE MOVED AWAY FROM THE VIEW IF THEY ARE NOT HIDDEN
away_from_frame_distance = (0,0,10000000000)

# NAME OF THE GPENCIL OBJECT YOU'RE
gp_obj_name = 'SHADEING'

# layer in gpencil
regular_layer = 'shadeing'

# IF NO NAME IS GIVEN IT WILL BE THE SAME WHERE IT GPENCIL IS IN
output_collection = 'dss'

# MAKE A SPERATE LAYER ON THE SAME GPENCIL THAT MAKES HOLES POSSIBLE
sub_layer = ''

# if the sub traction and makeing holes increase if or low if it dose not make the holes
sub_layer_extrution_amount = 1

# where the subtraction gets outputed to if in cluded
sub_output_collection = ''

# MODE BETWEEN THE FRAMES 'CONSTANT' TO GET A MORE ANIMATION LOOK TO IT
interpolation_type = 'CONSTANT'

# !!TIP!! :: IF YOU WANT MORE DETAIL IN THE OBJECTS LOWER THIS NUMBER AND CLOSE EVERY LINE
# BY ZOOMING IN AND DRAWING A LINE OVER THE EXISTING LINES WHERE THEY CLOSE THEN RUN THE SCRIPT
# ADJUST THE DETAIL OF THE OBJECT THAT GETST TRANSFORMED
# 0.0200 fast but still looking good
# 0.0100 and lower you need to have clean lines that are filled and close well
merge_distance = 0.0100

# if True then it will out delete the collections of subtraction layer
auto_delete_sub_layers = False

# where the transform should start IMP
start_frame = 0

# DEBUG MODE
#bpy.app.debug_wm = False

# TODO :: MAKE THE SUB AUTO DELETE WORK 

"""
############################ END OF SETTING VARIABLES ##################################
"""
def Shady_Pencil(gp_obj_name='',regular_layer='',output_collection='',sub_layer='',sub_layer_extrution_amount=1,sub_output_collection='',merge_distance = 0.0100,auto_delete_sub_layers = False,start_frame = 1):
    
    away_from_frame_distance = (0,0,10000000000)

    interpolation_type = 'CONSTANT'

    if not bpy.context.active_object == 'GPENCIL':

        print('FAIL NO GPENCIL OBJECT SELECTED')


    bpy.context.view_layer.objects.active = bpy.data.objects[gp_obj_name]
    bpy.data.objects[gp_obj_name].select_set(True)
    bpy.data.scenes[0].frame_current = start_frame

    bpy.data.scenes[bpy.context.scene.name_full].view_layers[bpy.context.view_layer.name].active_layer_collection = bpy.context.window.view_layer.layer_collection.children[output_collection]

    def convert_curves_to_filled_mesh(output_collection,merge_distance):

        for obj in bpy.data.collections[output_collection].objects:
        
            bpy.data.objects[obj.name].select_set(True)
            bpy.context.view_layer.objects.active = obj

            if  bpy.data.objects[obj.name].type == 'CURVE':

                bpy.ops.object.convert(target='MESH')
                bpy.ops.object.editmode_toggle()

                bpy.ops.mesh.select_all() 
                bpy.ops.mesh.remove_doubles(threshold=merge_distance, use_sharp_edge_from_normals=False)
                bpy.ops.object.editmode_toggle()

                bpy.context.view_layer.objects.active = obj
                bpy.data.objects[obj.name].select_set(True)

                index_of_looped = [0]

                vert_index_limit = len(bpy.context.object.data.vertices)   

                while True: 

                    if vert_index_limit == len(bpy.context.object.data.vertices.data.loops):
                        break
                    
                    current_index = len(bpy.context.object.data.vertices.data.loops)

                    if current_index > vert_index_limit:
                        break
                    
                    bpy.ops.object.mode_set(mode = 'EDIT')
                    bpy.ops.mesh.select_mode(type="VERT")
                    bpy.ops.mesh.select_all(action = 'DESELECT')
                    bpy.ops.object.mode_set(mode = 'OBJECT')

                    bpy.context.object.data.vertices[current_index].select = True    

                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.select_linked(delimit=set())
                    bpy.ops.mesh.edge_face_add()
                    bpy.ops.object.editmode_toggle()

                    bpy.context.object.data.vertices[current_index].select = False

            bpy.data.objects[obj.name].select_set(False)


    def hide_none_active_obj(output_collection):
        for key_obj in bpy.data.collections[output_collection].objects[1:]:
            selected_key_obj = ""
            try:
                selected_key_obj = key_obj.name
                bpy.data.objects[selected_key_obj].select_set(True)
                key_obj.hide_render = True
                key_obj.keyframe_insert("hide_render")
            except:
                bpy.data.objects[selected_key_obj].select_set(False)

            try:
                selected_key_obj = key_obj.name
                bpy.data.objects[selected_key_obj].select_set(True)
                key_obj.keyframe_insert(bpy.ops.transform.translate(value=away_from_frame_distance))
            except:
                bpy.data.objects[selected_key_obj].select_set(False)    

    def context_swap(area_type=""):

        if area_type == "":
            print("no type given")

        override_context = bpy.context.copy()
        area = [area for area in bpy.context.screen.areas if area.type == area_type][0]
        override_context['window'] = bpy.context.window
        override_context['screen'] = bpy.context.screen
        override_context['area'] = area
        override_context['region'] = area.regions[-1]
        override_context['scene'] = bpy.context.scene
        override_context['space_data'] = area.spaces.active

        return override_context

    def convert_GP(gp_obj_name='',output_collection='',interpolation_type = 'CONSTANT',merge_distance = 0.0401,layer='',away_from_frame_distance=away_from_frame_distance): 

        override_context = context_swap("VIEW_3D")

        if not 'FINISHED' in bpy.ops.object.mode_set(mode='OBJECT'): 
            print('FAILED TO ENTER OBJECT MODE')

        prev_obj_name = ""
        current_object_index = 0

        while True:

            name_of_GP_Stroke = bpy.context.object.data.name

            bpy.data.grease_pencils[name_of_GP_Stroke].layers.active = bpy.data.grease_pencils[name_of_GP_Stroke].layers[layer]
            current_frame = bpy.data.scenes[0].frame_current
            bpy.data.scenes[bpy.context.scene.name_full].view_layers[bpy.context.view_layer.name].active_layer_collection = bpy.context.window.view_layer.layer_collection.children[output_collection]
            bpy.ops.gpencil.convert(override_context,type='CURVE', use_timing_data=False)

            bpy.data.objects[gp_obj_name].select_set(False)

            obj_name = bpy.data.collections[output_collection].all_objects[current_object_index].name_full

            try:
                bpy.data.collections[output_collection].objects[obj_name].hide_render = False
                bpy.data.collections[output_collection].objects[obj_name].keyframe_insert("hide_render")
            except:
                print("dont know error i gess")

            try:
                bpy.data.collections[output_collection].objects[obj_name].keyframe_insert(bpy.ops.transform.translate())
            except:
                print("dont know error i gess")

            try:
                if not prev_obj_name == "":
                    bpy.data.objects[obj_name].select_set(False)
                    bpy.data.objects[prev_obj_name].select_set(True)
                    bpy.data.collections[output_collection].objects[prev_obj_name].hide_render = True
                    bpy.data.collections[output_collection].objects[prev_obj_name].keyframe_insert("hide_render")
                    bpy.data.objects[prev_obj_name].select_set(False)
            except:
                bpy.data.objects[prev_obj_name].select_set(False)

            try:
                if not prev_obj_name == "":
                    bpy.data.objects[obj_name].select_set(False)
                    bpy.data.objects[prev_obj_name].select_set(True)
                    bpy.data.collections[output_collection].objects[prev_obj_name].keyframe_insert(bpy.ops.transform.translate(value=away_from_frame_distance))
                    bpy.data.objects[prev_obj_name].select_set(False)
            except:
                bpy.data.objects[prev_obj_name].select_set(False)

            bpy.data.objects[obj_name].select_set(False)
            current_object_index += 1
            prev_obj_name = obj_name 
            bpy.data.objects[gp_obj_name].select_set(True)
            ret = bpy.ops.screen.keyframe_jump(next=True)

            if 'CANCELLED' in ret :
                break

        bpy.context.scene.frame_set(0)
        bpy.data.objects[gp_obj_name].select_set(False)

        hide_none_active_obj(output_collection)

        convert_curves_to_filled_mesh(output_collection,merge_distance)


    convert_GP(
            gp_obj_name,
            output_collection,
            interpolation_type,
            merge_distance,
            layer=regular_layer)


    if not sub_layer == '':   

        bpy.context.view_layer.objects.active = bpy.data.objects[gp_obj_name]
        bpy.data.objects[gp_obj_name].select_set(True)

        override_context = context_swap("OUTLINER")

        bpy.data.scenes[bpy.context.scene.name_full].view_layers[bpy.context.view_layer.name].active_layer_collection = bpy.data.scenes[bpy.context.scene.name_full].view_layers[bpy.context.view_layer.name].layer_collection.children['subtraction']

        convert_GP(
            gp_obj_name,
            sub_output_collection,
            interpolation_type,
            merge_distance,
            layer=sub_layer)

        for sub in bpy.data.collections[sub_output_collection].objects:

            sub.modifiers.new(name='SOLIDIFY',type='SOLIDIFY')
            sub.modifiers['SOLIDIFY'].offset = 0
            sub.modifiers['SOLIDIFY'].thickness = sub_layer_extrution_amount

            bpy.context.view_layer.objects.active = sub
            bpy.ops.object.modifier_apply(modifier="SOLIDIFY")

        for obj in bpy.data.collections[output_collection].objects:
        
            obj.modifiers.new("BOOLEAN","BOOLEAN")

        used_sub = []
        bpy.ops.screen.frame_jump()

        for obj in bpy.data.collections[output_collection].objects:

            for sub in bpy.data.collections[sub_output_collection].objects[len(used_sub):]:

                if not sub.name in used_sub and not sub.hide_render:

                    obj.modifiers['BOOLEAN'].object = sub

                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.modifier_apply(modifier="BOOLEAN")

                    used_sub.append(sub.name)

            bpy.context.view_layer.objects.active = bpy.data.collections[gp_obj_name].objects[gp_obj_name]
            bpy.ops.screen.keyframe_jump()

    index = 0
    for obj in bpy.data.collections[output_collection].objects:
        bpy.data.collections[output_collection].objects[index].select_set(True)
        index += 1

    if not sub_layer == '':
        index = 0
        for obj in bpy.data.collections[sub_output_collection].objects:
            bpy.data.collections[sub_output_collection].objects[index].select_set(True)
            index += 1

    override_context = context_swap("DOPESHEET_EDITOR")

    bpy.ops.action.select_all(override_context,action='SELECT')
    bpy.ops.action.interpolation_type(override_context,type=interpolation_type)

class VIEW3D_PT_GP_Shady_Pencil(bpy.types.Panel):
    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Shady Pencil"
    bl_label = "Shady Pencil"
    


    def draw(self,context):
        
        props = self.layout.operator("data.shady_pencil",text="Run")
        
        col = self.layout.column(align=True)
        
        col.prop(context.scene,'gp_obj_name')
        
        col.prop(context.scene,'regular_layer')
        
        col.prop(context.scene,'output_collection')

        col.prop(context.scene, 'sub_layer')
        
        col.prop(context.scene,'sub_output_collection')
        
        col.prop(context.scene,'sub_layer_extrution_amount')
        
        col.prop(context.scene,'merge_distance')
        
        col.prop(context.scene,'auto_delete_sub_layers')

        col.prop(context.scene,'start_frame')
        
        props.gp_obj_name = context.scene.gp_obj_name

        props.regular_layer = context.scene.regular_layer

        props.output_collection = context.scene.output_collection

        props.sub_layer = context.scene.sub_layer

        props.sub_layer_extrution_amount = context.scene.sub_layer_extrution_amount

        props.sub_output_collection = context.scene.sub_output_collection

        props.merge_distance = context.scene.merge_distance

        props.auto_delete_sub_layers = context.scene.auto_delete_sub_layers

        props.start_frame = context.scene.start_frame   


class DATA_OT_GP_Shady_Pencil(bpy.types.Operator):
    
    bl_idname = "data.shady_pencil"
    bl_label = "Shady Pencil"
    bl_options = {'REGISTER','UNDO'}

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
     
    auto_delete_sub_layers: bpy.props.BoolProperty(
                                    name="auto_delete_sub_layers",
                                    description="this auto deletes the subtract layer",
                                    default=False)
    
    start_frame: bpy.props.IntProperty(
                            name="start_frame",
                            description="start frame for the script to run on.",
                            default=00,
                            min=1,
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
                        start_frame = self.start_frame)
        
            return {'FINISHED'}
        
        return {'CANCELED'}

def register():
    
    
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
    
    bpy.types.Scene.start_frame = bpy.props.IntProperty(
                            name="start_frame",
                            description="start frame for the script to run on.",
                            default=0,
                            min=1,
                            max=2000)
                             
    bpy.utils.register_class(VIEW3D_PT_GP_Shady_Pencil)
    bpy.utils.register_class(DATA_OT_GP_Shady_Pencil)
    
def unregister():
    
    del bpy.types.Scene.gp_obj_name

    del bpy.types.Scene.regular_layer

    del bpy.types.Scene.output_collection

    del bpy.types.Scene.sub_layer

    del bpy.types.Scene.sub_layer_extrution_amount

    del bpy.types.Scene.sub_output_collection

    del bpy.types.Scene.merge_distance

    del bpy.types.Scene.auto_delete_sub_layers

    del bpy.types.Scene.start_frame     
                            
    bpy.utils.unregister_class(VIEW3D_PT_GP_Shady_Pencil)
    bpy.utils.unregister_class(DATA_OT_GP_Shady_Pencil)
       
if __name__ == "__main__":
    register()
