import bpy

away_from_frame_distance = (0, 0, 10000000000)

interpolation_type = 'CONSTANT'

merge_distance = 0.0100

auto_delete_sub_layers = ""

# TODO :: IF A STROKE IS CREATE INFRONT OF ALL ITS FRAMES THERE IS A ERROR CONVERTING
#! WE KNOW THAT SUB WORKS FOR DEFUALT TAKE THE END OF DEAFAULT AND A GEOMETRY EXTUTION TO IT SIMPLE AS THAT WITH AT IF CHECK FOR GEOMETRY AND REMOVE THE WEIRD GEOMETRY
# TODO :: UPLOAD FULL TUTORICAL WHEN ALL IS DONE

def convert_curves_to_filled_mesh(output_collection, merge_angle, merge_distance, complex_convert):

    if complex_convert:
        for obj in bpy.data.collections[output_collection].objects:

            bpy.data.objects[obj.name].select_set(True)
            bpy.context.view_layer.objects.active = obj
            if bpy.data.objects[obj.name].type == 'CURVE':

                bpy.ops.object.convert(target='MESH')
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.select_all()
                bpy.ops.mesh.dissolve_limited(angle_limit=merge_angle)
                bpy.ops.mesh.remove_doubles(threshold=merge_distance)
                bpy.ops.object.editmode_toggle()
                bpy.context.view_layer.objects.active = obj
                bpy.data.objects[obj.name].select_set(True)
                vert_index_limit = len(bpy.context.object.data.vertices)
                while True:

                    if vert_index_limit == len(bpy.context.object.data.vertices.data.loops):
                        break

                    current_index = len(
                        bpy.context.object.data.vertices.data.loops)
                    if current_index > vert_index_limit:
                        break

                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_mode(type="VERT")
                    bpy.ops.mesh.select_all(action='DESELECT')
                    bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.context.object.data.vertices[current_index].select = True
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.select_linked(delimit=set())
                    bpy.ops.mesh.edge_face_add()
                    bpy.ops.object.editmode_toggle()
                    bpy.context.object.data.vertices[current_index].select = False

            bpy.data.objects[obj.name].select_set(False)
    else:
        for obj in bpy.data.collections[output_collection].objects:
            bpy.data.objects[obj.name].select_set(True)
            bpy.context.view_layer.objects.active = obj
            if bpy.data.objects[obj.name].type == 'CURVE':

                bpy.ops.object.convert(target='MESH')
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.dissolve_limited(angle_limit=merge_angle)
                bpy.ops.mesh.remove_doubles(threshold=merge_distance)
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.convert(target='CURVE')
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.curve.select_all(action='SELECT')
                bpy.ops.curve.cyclic_toggle()

                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.convert(target='MESH')
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.edge_face_add()

                bpy.ops.object.mode_set(mode='OBJECT')
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
            key_obj.keyframe_insert(bpy.ops.transform.translate(
                value=away_from_frame_distance))
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


def convert_GP(gp_obj_name='', output_collection='', merge_angle=0.0401, merge_distance=0.01, layer='', away_from_frame_distance=away_from_frame_distance, extrusion_length=0.01, complex_convert=True, MODE="", close_curves=False, sub_layer="", start_frame=0):

    override_context = context_swap("VIEW_3D")

    if not 'FINISHED' in bpy.ops.object.mode_set(mode='OBJECT'):
        print('FAILED TO ENTER OBJECT MODE')

    if sub_layer != "":

        key_frame_animation(gp_obj_name, output_collection, sub_layer,
                            away_from_frame_distance, override_context)
    else:
        key_frame_animation(gp_obj_name, output_collection, layer,
                            away_from_frame_distance, override_context)
    # ? USE START_FRAME INSTEAD OF ZERO
    bpy.context.scene.frame_set(start_frame)
    bpy.data.objects[gp_obj_name].select_set(False)

    hide_none_active_obj(output_collection)

    if MODE == "DEFAULT" or MODE == "GEOMETRY":
        convert_curves_to_filled_mesh(
            output_collection, merge_angle, merge_distance, complex_convert)

    elif MODE == "CURVES" and close_curves:

        for obj in bpy.data.collections[output_collection].objects:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.curve.select_all(action='SELECT')
            bpy.ops.curve.cyclic_toggle()
            bpy.ops.object.mode_set(mode='OBJECT')

            obj.select_set(False)


def key_frame_animation(gp_obj_name, output_collection, layer, away_from_frame_distance, override_context):
    prev_obj_name = ""
    current_object_index = 0

    while True:
        name_of_GP_Stroke = bpy.context.object.data.name
        
        for obj in bpy.context.object.data.layers:
            obj.hide = True

        bpy.context.object.data.layers[layer].hide = False

        with bpy.context.temp_override(window=override_context['window'],area=override_context['area'],region=override_context['region']):
            bpy.ops.object.convert(target='MESH',keep_original=True, merge_customdata=False)
            bpy.ops.object.convert(target='CURVE')
        
        bpy.data.collections[output_collection].objects.link(bpy.context.object)
        bpy.ops.object.make_local()
        # FIX start here :: COLLECTION HARDCODED THIS SHOULD BE THE ONLY COLLETION THAT HOLD ORIGINAL STROKE AND THE CREATE ONE IN ONE COLLEXTION 
        
        bpy.data.collections['Collection'].objects.unlink(bpy.context.object)

        bpy.data.objects[gp_obj_name].select_set(False)

        obj_name = bpy.data.collections[output_collection].all_objects[current_object_index].name_full

        try:
            bpy.data.collections[output_collection].objects[obj_name].hide_render = False
            bpy.data.collections[output_collection].objects[obj_name].keyframe_insert("hide_render")
        except:
            print("i assume the error happens here")

        try:
            # fix this line 
            bpy.ops.transform.translate(value=(0, 0, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
           # bpy.data.collections[output_collection].objects[obj_name].keyframe_insert(bpy.ops.transform.translate())
        except:
            print("so is it this line of codso is it this line of codee")

        try:
            if not prev_obj_name == "":
                bpy.data.objects[obj_name].select_set(False)
                bpy.data.objects[prev_obj_name].select_set(True)
                bpy.data.collections[output_collection].objects[prev_obj_name].hide_render = True
                bpy.data.collections[output_collection].objects[prev_obj_name].keyframe_insert(
                    "hide_render")
                bpy.data.objects[prev_obj_name].select_set(False)
        except:
            bpy.data.objects[prev_obj_name].select_set(False)

        try:
            if not prev_obj_name == "":
                bpy.data.objects[obj_name].select_set(False)
                bpy.data.objects[prev_obj_name].select_set(True)
                bpy.data.collections[output_collection].objects[prev_obj_name].keyframe_insert(
                    bpy.ops.transform.translate(value=away_from_frame_distance))
                bpy.data.objects[prev_obj_name].select_set(False)
        except:
            bpy.data.objects[prev_obj_name].select_set(False)
        
        bpy.data.objects[obj_name].select_set(False)
        current_object_index += 1
        prev_obj_name = obj_name
        bpy.data.objects[gp_obj_name].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[gp_obj_name]
        ret = bpy.ops.screen.keyframe_jump(next=True)

        if 'CANCELLED' in ret:
            break


def Shady_Pencil(MODE="DEFAULT", gp_obj_name='', regular_layer='', output_collection='', sub_layer='', sub_layer_extrution_amount=1, sub_output_collection='',
                 merge_angle=0.0100, auto_delete_sub_layers=False, auto_remove_vertices_and_faces=False, merge_distance=0.01, extrusion_length=0.01, complex_convert=False, repair_collection="", close_curves=False):

    interpolation_type = 'CONSTANT'
    print(gp_obj_name)
    if not bpy.context.active_object == 'GPENCIL':
        print('FAIL NO GPENCIL OBJECT SELECTED')

    bpy.context.view_layer.objects.active = bpy.data.objects[gp_obj_name]
    bpy.data.objects[gp_obj_name].select_set(True)

    start_frame = bpy.data.scenes[0].frame_current

    if not output_collection == "":
        # THIS SET THE OUTPUT COLLECTION
        bpy.data.scenes[bpy.context.scene.name_full].view_layers[bpy.context.view_layer.name].active_layer_collection = bpy.context.window.view_layer.layer_collection.children[output_collection]

    if not MODE == "REPAIR" and not MODE == "LINE":

        convert_GP(
            gp_obj_name=gp_obj_name,
            output_collection=output_collection,
            merge_angle=merge_angle,
            merge_distance=merge_distance,
            layer=regular_layer,
            away_from_frame_distance=away_from_frame_distance,
            extrusion_length=extrusion_length,
            complex_convert=complex_convert,
            sub_layer="",
            MODE=MODE,
            close_curves=close_curves,
            start_frame=start_frame)

        if sub_layer != '':

            bpy.context.view_layer.objects.active = bpy.data.objects[gp_obj_name]
            bpy.data.objects[gp_obj_name].select_set(True)

            override_context = context_swap("OUTLINER")

            bpy.data.scenes[bpy.context.scene.name_full].view_layers[bpy.context.view_layer.name].active_layer_collection = bpy.data.scenes[
                bpy.context.scene.name_full].view_layers[bpy.context.view_layer.name].layer_collection.children[sub_output_collection]
            bpy.data.scenes[0].frame_current = start_frame

            convert_GP(
                gp_obj_name=gp_obj_name,
                output_collection=sub_output_collection,
                merge_angle=merge_angle,
                merge_distance=merge_distance,
                layer=regular_layer,
                away_from_frame_distance=away_from_frame_distance,
                extrusion_length=extrusion_length,
                complex_convert=complex_convert,
                sub_layer=sub_layer,
                MODE=MODE,
                close_curves=close_curves,
                start_frame=start_frame)

            for sub in bpy.data.collections[sub_output_collection].objects:

                sub.modifiers.new(name='SOLIDIFY', type='SOLIDIFY')
                sub.modifiers['SOLIDIFY'].offset = 0
                sub.modifiers['SOLIDIFY'].thickness = sub_layer_extrution_amount

                bpy.context.view_layer.objects.active = sub
                bpy.ops.object.modifier_apply(modifier="SOLIDIFY")

            for obj in bpy.data.collections[output_collection].objects:

                obj.modifiers.new(name='SOLIDIFY', type='SOLIDIFY')
                obj.modifiers['SOLIDIFY'].offset = 0
                obj.modifiers['SOLIDIFY'].thickness = extrusion_length

                bpy.context.view_layer.objects.active = obj 
                bpy.ops.object.modifier_apply(modifier="SOLIDIFY")

                obj.modifiers.new("BOOLEAN", "BOOLEAN")
                bpy.context.object.modifiers["BOOLEAN"].solver = 'EXACT'

            used_sub = []
            bpy.ops.screen.frame_jump()

            for obj in bpy.data.collections[output_collection].objects:

                for sub in bpy.data.collections[sub_output_collection].objects[len(used_sub):]:

                    if not sub.name in used_sub and not sub.hide_render:

                        obj.modifiers['BOOLEAN'].object = sub

                        bpy.context.view_layer.objects.active = obj
                        bpy.ops.object.modifier_apply(modifier="BOOLEAN")

                        used_sub.append(sub.name)

                bpy.ops.screen.keyframe_jump()

        for obj in bpy.data.collections[output_collection].objects:
            obj.select_set(True)

        if not sub_layer == '':
            for obj in bpy.data.collections[sub_output_collection].objects:
                obj.select_set(True)

        override_context = context_swap("DOPESHEET_EDITOR")

        with bpy.context.temp_override(window=override_context['window'],area=override_context['area'],region=override_context['region']):
            bpy.ops.action.select_all(action='SELECT')
            bpy.ops.action.interpolation_type( type=interpolation_type)

        # EXTRUDES MESH
        if MODE == "GEOMETRY":
            for obj in bpy.data.collections[output_collection].objects:

                obj.select_set(True)

                obj.modifiers.new(name='SOLIDIFY', type='SOLIDIFY')
                obj.modifiers['SOLIDIFY'].offset = 0
                obj.modifiers['SOLIDIFY'].thickness = extrusion_length

                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.modifier_apply(modifier="SOLIDIFY")

                obj.select_set(False)
        
        clean_up(auto_remove_vertices_and_faces,auto_delete_sub_layers,output_collection,regular_layer,sub_layer,sub_output_collection,MODE,gp_obj_name)
       

    elif MODE == "REPAIR":


        bpy.data.scenes[bpy.context.scene.name_full].view_layers[bpy.context.view_layer.name].active_layer_collection = bpy.context.window.view_layer.layer_collection.children[repair_collection]
        bpy.context.view_layer.objects.active = bpy.data.objects[gp_obj_name]
        bpy.data.objects[gp_obj_name].select_set(True)
        #start here :: both layes get converted into mesh

        name_of_gp_stroke = bpy.context.object.data.name
        bpy.data.grease_pencils_v3[name_of_gp_stroke].layers.active = bpy.data.grease_pencils_v3[name_of_gp_stroke].layers[regular_layer]

        bpy.ops.object.convert(target='CURVE')
        # bpy.ops.gpencil.convert(type='path', use_timing_data=False)

        convert_curves_to_filled_mesh(
            repair_collection, merge_angle, merge_distance, complex_convert)

    elif MODE == "LINE":

        if (bpy.context.blend_data.version[0] >= 3 and bpy.context.blend_data.version[1] >= 4) or bpy.context.blend_data.version[0] >= 4:

            bpy.context.view_layer.objects.active = bpy.data.objects[gp_obj_name]
            bpy.data.objects[gp_obj_name].select_set(true)

            bpy.ops.object.mode_set(mode='object')

            override_context = context_swap("view_3d")

            while true:

                bpy.ops.gpencil.editmode_toggle()

                with bpy.context.temp_override(window=override_context['window'],area=override_context['area'],region=override_context['region']):
                    bpy.ops.gpencil.select_all(action='select')
                
                with bpy.context.temp_override(window=override_context['window'],area=override_context['area'],region=override_context['region'],editable_gpencil_strokes = bpy.data.objects[gp_obj_name].data.layers[regular_layer].frames[0].strokes):
                    bpy.ops.gpencil.stroke_outline()

                bpy.ops.gpencil.editmode_toggle()

                ret = bpy.ops.screen.keyframe_jump(next=true)

                if 'cancelled' in ret:
                    break

            bpy.data.scenes[0].frame_current = start_frame

            bpy.data.scenes[bpy.context.scene.name_full].view_layers[bpy.context.view_layer.name].active_layer_collection = bpy.context.window.view_layer.layer_collection.children[output_collection]

            for obj in bpy.data.objects:
                obj.select_set(false)

            override_context = context_swap("view_3d")
            key_frame_animation(gp_obj_name=gp_obj_name, output_collection=output_collection, layer=regular_layer,
                                away_from_frame_distance=away_from_frame_distance, override_context=override_context)

            convert_curves_to_filled_mesh(
                output_collection=output_collection, merge_angle=merge_angle, merge_distance=merge_distance, complex_convert=complex_convert)

            bpy.context.scene.frame_set(start_frame)

            hide_none_active_obj(output_collection)


def clean_up(auto_remove_vertices_and_faces,auto_delete_sub_layers,output_collection,regular_layer,sub_layer,sub_output_collection,MODE,gp_obj_name):
    if auto_delete_sub_layers and ( MODE == "GEOMETRY" or MODE == "DEFAULT" ):
        for obj in bpy.data.collections[output_collection].objects:
            try:
                obj.select_set(false)
            except:
                print("error :: failed to deselect obj in output_collection")
        obj_arr = []
        try: 
            obj_arr.extend(bpy.data.collections[sub_output_collection].objects)
        except:
            print("err :: extend on sub collection")
        with bpy.context.temp_override(selected_objects=obj_arr):
            
            bpy.ops.object.delete()

    if MODE == "DEFAULT" and auto_remove_vertices_and_faces:   
        print("this is running ther auto clean")
        for obj in bpy.data.collections[output_collection].objects:
            bpy.data.objects[obj.name].select_set(True)
            bpy.context.view_layer.objects.active = obj

            bpy.ops.object.convert(target='MESH')
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all()
            bpy.ops.mesh.remove_doubles(threshold=0.002)
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.delete(type='ONLY_FACE')
            bpy.ops.object.editmode_toggle()

    bpy.context.view_layer.objects.active = bpy.data.objects[gp_obj_name]
    bpy.data.objects[gp_obj_name].select_set(True)
    for obj in bpy.context.object.data.layers:
        obj.hide = False
