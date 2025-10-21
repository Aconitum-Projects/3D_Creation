import bpy

# --- Collections à contrôler ---
collections_to_control = {
    "Hair": "Hair",
    "Shirts": "Shirts",
    "Pants": "Pants",
    "Dress": "Dresses"
}

# --- Fonctions pour activer/désactiver ---
def deactivate_collection(collection_name):
    coll = bpy.data.collections.get(collection_name)
    if coll:
        for obj in coll.objects:
            obj.hide_viewport = True

def activate_object(category, obj_name):
    if category == "Hair":
        for obj in bpy.data.collections[collections_to_control["Hair"]].objects:
            obj.hide_viewport = (obj.name != obj_name)
    elif category in ["Shirts", "Pants"]:
        for dress_obj in bpy.data.collections[collections_to_control["Dress"]].objects:
            dress_obj.hide_viewport = True
        coll = bpy.data.collections[collections_to_control[category]]
        for obj in coll.objects:
            obj.hide_viewport = (obj.name != obj_name)
        other = "Shirts" if category == "Pants" else "Pants"
        other_coll = bpy.data.collections[collections_to_control[other]]
        if all(o.hide_viewport for o in other_coll.objects):
            first_obj = sorted(other_coll.objects, key=lambda o: o.name)[0]
            first_obj.hide_viewport = False
    elif category == "Dress":
        for cat in ["Shirts", "Pants"]:
            for obj in bpy.data.collections[collections_to_control[cat]].objects:
                obj.hide_viewport = True
        coll = bpy.data.collections[collections_to_control["Dress"]]
        for obj in coll.objects:
            obj.hide_viewport = (obj.name != obj_name)

def init_objects():
    for category, prefix in collections_to_control.items():
        coll = bpy.data.collections.get(prefix)
        if coll and coll.objects:
            for obj in coll.objects:
                obj.hide_viewport = True
            first_obj = [o for o in coll.objects if "_00" in o.name]
            if first_obj:
                first_obj[0].hide_viewport = False

# --- Operator pour activer les objets ---
class OBJECT_OT_activate_item(bpy.types.Operator):
    bl_idname = "object.activate_item"
    bl_label = "Activate Item"
    
    category: bpy.props.StringProperty()
    obj_name: bpy.props.StringProperty()
    
    def execute(self, context):
        activate_object(self.category, self.obj_name)
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
        return {'FINISHED'}

# --- Operator Reset ---
class OBJECT_OT_reset_items(bpy.types.Operator):
    bl_idname = "object.reset_items"
    bl_label = "Reset All"
    
    def execute(self, context):
        init_objects()
        return {'FINISHED'}

# --- UI Panel ---
class VIEW3D_PT_collection_visibility(bpy.types.Panel):
    bl_label = "Character Customizer"
    bl_idname = "VIEW3D_PT_collection_visibility"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Character'

    def draw(self, context):
        layout = self.layout

        # Hair en haut
        hair_coll = bpy.data.collections.get(collections_to_control["Hair"])
        if hair_coll:
            box = layout.box()
            box.label(text="Hair")
            for obj in sorted(hair_coll.objects, key=lambda o: o.name):
                row = box.row()
                op = row.operator("object.activate_item", text=obj.name)
                op.category = "Hair"
                op.obj_name = obj.name

        # Shirts et Pants côte à côte avec box
        row = layout.row()
        for cat in ["Shirts", "Pants"]:
            coll = bpy.data.collections.get(collections_to_control[cat])
            if coll:
                box = row.box()
                box.label(text=cat)
                for obj in sorted(coll.objects, key=lambda o: o.name):
                    row_obj = box.row()
                    op = row_obj.operator("object.activate_item", text=obj.name)
                    op.category = cat
                    op.obj_name = obj.name

        # Dress en bas
        dress_coll = bpy.data.collections.get(collections_to_control["Dress"])
        if dress_coll:
            box = layout.box()
            box.label(text="Dress")
            for obj in sorted(dress_coll.objects, key=lambda o: o.name):
                row = box.row()
                op = row.operator("object.activate_item", text=obj.name)
                op.category = "Dress"
                op.obj_name = obj.name

        # Bouton reset
        layout.separator()
        layout.operator("object.reset_items", text="Reset All", icon='FILE_REFRESH')

# --- Registration ---
classes = [VIEW3D_PT_collection_visibility, OBJECT_OT_activate_item, OBJECT_OT_reset_items]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    init_objects()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
