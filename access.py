bl_info = {
    "name": "Accessibility Simple Names",
    "author": "ItsMe",
    "version": (1, 1),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > SimpleUI",
    "description": "Interface simplifiée avec noms simples",
    "category": "Interface",
}

import bpy

# ---------------------------------------------------
# PROPRIÉTÉS
# ---------------------------------------------------

class SimpleUIProperties(bpy.types.PropertyGroup):
    show_help: bpy.props.BoolProperty(
        name="Afficher explications",
        description="Affiche des explications simples pour chaque bouton",
        default=True
    )

# ---------------------------------------------------
# FONCTIONS UTILITAIRES
# ---------------------------------------------------

def ensure_object(context):
    obj = context.object
    if not obj:
        return False
    if obj.type != 'MESH':
        return False
    return True

def ensure_mode(mode):
    if bpy.context.object.mode != mode:
        bpy.ops.object.mode_set(mode=mode)

# ---------------------------------------------------
# OPERATEURS
# ---------------------------------------------------

# Transformation
class SIMPLE_OT_move(bpy.types.Operator):
    bl_idname = "simple.move"
    bl_label = "Déplacer ⬆"
    bl_description = "Déplace l'objet ou la sélection"

    def execute(self, context):
        bpy.ops.wm.tool_set_by_id(name="builtin.move")
        return {'FINISHED'}


class SIMPLE_OT_rotate(bpy.types.Operator):
    bl_idname = "simple.rotate"
    bl_label = "Tourner 🔄"
    bl_description = "Tourne l'objet ou la sélection"

    def execute(self, context):
        bpy.ops.wm.tool_set_by_id(name="builtin.rotate")
        return {'FINISHED'}


class SIMPLE_OT_scale(bpy.types.Operator):
    bl_idname = "simple.scale"
    bl_label = "Taille 📏"
    bl_description = "Change la taille de l'objet ou de la sélection"

    def execute(self, context):
        bpy.ops.wm.tool_set_by_id(name="builtin.scale")
        return {'FINISHED'}


class SIMPLE_OT_extrude(bpy.types.Operator):
    bl_idname = "simple.extrude"
    bl_label = "Étendre ⬆"
    bl_description = "Tire une face pour créer du volume"

    def execute(self, context):
        if not ensure_object(context):
            self.report({'WARNING'}, "Sélectionne un objet Mesh")
            return {'CANCELLED'}

        ensure_mode('EDIT')
        bpy.ops.mesh.extrude_region_move()
        return {'FINISHED'}


class SIMPLE_OT_inset(bpy.types.Operator):
    bl_idname = "simple.inset"
    bl_label = "Inset ⬛"
    bl_description = "Crée une face plus petite à l'intérieur d'une face"

    def execute(self, context):
        if not ensure_object(context):
            self.report({'WARNING'}, "Sélectionne un objet Mesh")
            return {'CANCELLED'}

        ensure_mode('EDIT')
        bpy.ops.mesh.inset()
        return {'FINISHED'}


# Création
class SIMPLE_OT_add_cube(bpy.types.Operator):
    bl_idname = "simple.add_cube"
    bl_label = "Créer un cube 🟦"
    bl_description = "Ajoute un nouveau cube dans la scène"

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        return {'FINISHED'}


class SIMPLE_OT_subdivision(bpy.types.Operator):
    bl_idname = "simple.subdivision"
    bl_label = "Subdivision ➗"
    bl_description = "Ajoute un modificateur Subdivision Surface pour lisser l'objet"

    def execute(self, context):
        if not ensure_object(context):
            self.report({'WARNING'}, "Sélectionne un objet Mesh")
            return {'CANCELLED'}

        ensure_mode('OBJECT')
        bpy.ops.object.modifier_add(type='SUBSURF')
        return {'FINISHED'}


class SIMPLE_OT_boolean(bpy.types.Operator):
    bl_idname = "simple.boolean"
    bl_label = "Combiner 🔗"
    bl_description = "Ajoute un modificateur Boolean pour combiner des objets"

    def execute(self, context):
        if not ensure_object(context):
            self.report({'WARNING'}, "Sélectionne un objet Mesh")
            return {'CANCELLED'}

        ensure_mode('OBJECT')
        bpy.ops.object.modifier_add(type='BOOLEAN')
        return {'FINISHED'}


class SIMPLE_OT_solidify(bpy.types.Operator):
    bl_idname = "simple.solidify"
    bl_label = "Épaissir ⬛"
    bl_description = "Ajoute un modificateur Solidify pour donner de l'épaisseur"

    def execute(self, context):
        if not ensure_object(context):
            self.report({'WARNING'}, "Sélectionne un objet Mesh")
            return {'CANCELLED'}

        ensure_mode('OBJECT')
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        return {'FINISHED'}


# Sélection
class SIMPLE_OT_select_linked(bpy.types.Operator):
    bl_idname = "simple.select_linked"
    bl_label = "Sélection liée 🔗"
    bl_description = "Sélectionne toutes les faces connectées"

    def execute(self, context):
        if not ensure_object(context):
            self.report({'WARNING'}, "Sélectionne un objet Mesh")
            return {'CANCELLED'}

        ensure_mode('EDIT')
        bpy.ops.mesh.select_linked()
        return {'FINISHED'}


# ---------------------------------------------------
# PANEL
# ---------------------------------------------------

class VIEW3D_PT_simple_ui(bpy.types.Panel):
    bl_label = " Interface Simple"
    bl_idname = "VIEW3D_PT_simple_ui"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SimpleUI"

    def draw(self, context):
        layout = self.layout
        props = context.scene.simple_ui_props

        layout.prop(props, "show_help")

        layout.separator()
        
        # Transformations
        layout.label(text="📐 Transformations")
        col = layout.column(align=True)
        col.operator("simple.move")
        col.operator("simple.rotate")
        col.operator("simple.scale")
        col.operator("simple.extrude")
        col.operator("simple.inset")
        
        if props.show_help:
            box = layout.box()
            box.label(text="  Déplacer : bouger l'objet", icon='INFO')
            box.label(text="  Tourner : pivoter l'objet", icon='INFO')
            box.label(text="  Taille : agrandir/rétrécir", icon='INFO')
            box.label(text="  Étendre : créer du volume", icon='INFO')
            box.label(text="  Inset : face dans la face", icon='INFO')

        layout.separator()
        
        # Création / Modificateurs
        layout.label(text="🔨 Création / Modificateurs")
        col = layout.column(align=True)
        col.operator("simple.add_cube")
        col.operator("simple.subdivision")
        col.operator("simple.boolean")
        col.operator("simple.solidify")
        
        if props.show_help:
            box = layout.box()
            box.label(text="  Cube : ajouter un cube", icon='INFO')
            box.label(text="  Subdivision : lisser l'objet", icon='INFO')
            box.label(text="  Combiner : fusionner des objets", icon='INFO')
            box.label(text="  Épaissir : donner de l'épaisseur", icon='INFO')

        layout.separator()
        
        # Sélection
        layout.label(text="🔍 Sélection")
        col = layout.column(align=True)
        col.operator("simple.select_linked")
        
        if props.show_help:
            box = layout.box()
            box.label(text="  Sélection liée : tout sélectionner d'un coup", icon='INFO')


# ---------------------------------------------------
# REGISTER
# ---------------------------------------------------

classes = (
    SimpleUIProperties,
    SIMPLE_OT_move,
    SIMPLE_OT_rotate,
    SIMPLE_OT_scale,
    SIMPLE_OT_extrude,
    SIMPLE_OT_inset,
    SIMPLE_OT_add_cube,
    SIMPLE_OT_subdivision,
    SIMPLE_OT_boolean,
    SIMPLE_OT_solidify,
    SIMPLE_OT_select_linked,
    VIEW3D_PT_simple_ui,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.simple_ui_props = bpy.props.PointerProperty(type=SimpleUIProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.simple_ui_props

if __name__ == "__main__":
    register()