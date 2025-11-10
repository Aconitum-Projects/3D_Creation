import bpy
import os

# Dossier d'export
export_path = "D:/Repository/3D_Creation/Ahkiu_Temple/Crowd/Animations/"  # ← change ce chemin

# Nom de base de ton personnage
base_name = "Char_Anim"

# Boucle sur toutes les actions
for action in bpy.data.actions:
    bpy.context.object.animation_data.action = action
    filepath = os.path.join(export_path, f"{base_name}_{action.name}.fbx")
    bpy.ops.export_scene.fbx(
        filepath=filepath,
        use_selection=True,
        bake_anim=True,
        bake_anim_use_all_bones=True,
        bake_anim_force_startend_keying=True,
        apply_scale_options='FBX_SCALE_ALL',
        object_types={'ARMATURE', 'MESH'},
        mesh_smooth_type='FACE',
        add_leaf_bones=False
    )
    print(f"Exported {filepath}")
