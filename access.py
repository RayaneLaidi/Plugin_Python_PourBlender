import bpy
import difflib
import unicodedata

bl_info = {
    "name": "Blender Simple Smart Assistant",
    "author": "itMeBitch",
    "version": (2, 0),
    "blender": (4, 3, 0),
    "location": "View3D > Sidebar > Assistant",
    "description": "Blender simplifié avec recherche intelligente avancée",
    "category": "Interface",
}


#  NORMALISATION TEXTE


def normalize(text):
    text = text.lower()
    text = ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')
    return text


#  SYNONYMES


SYNONYMS = {
    "ajouter": ["creer", "faire", "generer"],
    "creer": ["ajouter", "faire", "generer"],
    "effacer": ["supprimer", "enlever", "delete"],
    "bouger": ["deplacer", "move", "translation"],
    "tourner": ["rotation", "rotate"],
    "agrandir": ["scale", "grandir", "taille"],
    "photo": ["rendu", "render", "image"],
    "lumiere": ["lampe", "light"],
}

def expand_words(words):
    expanded = set(words)
    for word in words:
        for key, values in SYNONYMS.items():
            if word == key or word in values:
                expanded.add(key)
                expanded.update(values)
    return list(expanded)


#  ACTIONS SIMPLIFIÉES


ACTIONS = [


    #  CRÉATION - MESH COMPLET
  

    {"name": "Créer Cube", "icon": "MESH_CUBE", "category": "Créer",
     "tags": ["cube", "boite", "bloc"],
     "func": lambda: bpy.ops.mesh.primitive_cube_add()},

    {"name": "Créer Sphère UV", "icon": "MESH_UVSPHERE", "category": "Créer",
     "tags": ["sphere", "uv", "ballon"],
     "func": lambda: bpy.ops.mesh.primitive_uv_sphere_add()},

    {"name": "Créer Icosphère", "icon": "MESH_ICOSPHERE", "category": "Créer",
     "tags": ["icosphere", "sphere triangulaire"],
     "func": lambda: bpy.ops.mesh.primitive_ico_sphere_add()},

    {"name": "Créer Cylindre", "icon": "MESH_CYLINDER", "category": "Créer",
     "tags": ["cylindre", "tube"],
     "func": lambda: bpy.ops.mesh.primitive_cylinder_add()},

    {"name": "Créer Cone", "icon": "MESH_CONE", "category": "Créer",
     "tags": ["cone", "pointe"],
     "func": lambda: bpy.ops.mesh.primitive_cone_add()},

    {"name": "Créer Torus", "icon": "MESH_TORUS", "category": "Créer",
     "tags": ["torus", "anneau", "donut"],
     "func": lambda: bpy.ops.mesh.primitive_torus_add()},

    {"name": "Créer Plan", "icon": "MESH_PLANE", "category": "Créer",
     "tags": ["plan", "sol", "surface"],
     "func": lambda: bpy.ops.mesh.primitive_plane_add()},

    {"name": "Créer Monkey (Suzanne)", "icon": "MESH_MONKEY", "category": "Créer",
     "tags": ["suzanne", "monkey", "tete"],
     "func": lambda: bpy.ops.mesh.primitive_monkey_add()},

    {"name": "Créer Cercle", "icon": "MESH_CIRCLE", "category": "Créer",
     "tags": ["cercle", "circle"],
     "func": lambda: bpy.ops.mesh.primitive_circle_add()},

    {"name": "Créer Grille", "icon": "MESH_GRID", "category": "Créer",
     "tags": ["grille", "grid"],
     "func": lambda: bpy.ops.mesh.primitive_grid_add()},

  
    # CRÉATION - AUTRES OBJETS
    

    {"name": "Créer Lumière Point", "icon": "LIGHT_POINT", "category": "Créer",
     "tags": ["lumiere", "point", "lampe"],
     "func": lambda: bpy.ops.object.light_add(type='POINT')},

    {"name": "Créer Lumière Sun", "icon": "LIGHT_SUN", "category": "Créer",
     "tags": ["soleil", "sun"],
     "func": lambda: bpy.ops.object.light_add(type='SUN')},

    {"name": "Créer Caméra", "icon": "CAMERA_DATA", "category": "Créer",
     "tags": ["camera", "vue"],
     "func": lambda: bpy.ops.object.camera_add()},

    {"name": "Créer Texte", "icon": "FONT_DATA", "category": "Créer",
     "tags": ["texte", "ecrire"],
     "func": lambda: bpy.ops.object.text_add()},

    {"name": "Créer Empty", "icon": "EMPTY_DATA", "category": "Créer",
     "tags": ["empty", "vide", "pivot"],
     "func": lambda: bpy.ops.object.empty_add()},

#  TRANSFORMATIONS AVANCÉES


{"name": "To Sphere", "icon": "MESH_UVSPHERE", "category": "Transformer",
 "tags": ["sphere", "arrondir", "tosphere", "spherify"],
 "func": lambda: bpy.ops.transform.tosphere()},

{"name": "Shear (Cisaillement)", "icon": "MOD_SIMPLEDEFORM", "category": "Transformer",
 "tags": ["shear", "cisaillement", "incliner", "deformer"],
 "func": lambda: bpy.ops.transform.shear()},

{"name": "Bend (Courber)", "icon": "MOD_SIMPLEDEFORM", "category": "Transformer",
 "tags": ["bend", "courber", "plier", "courbure"],
 "func": lambda: bpy.ops.transform.bend()},

{"name": "Push / Pull", "icon": "ARROW_LEFTRIGHT", "category": "Transformer",
 "tags": ["push", "pull", "pousser", "tirer", "repousser"],
 "func": lambda: bpy.ops.transform.push_pull()},

{"name": "Shrink / Fatten", "icon": "FULLSCREEN_ENTER", "category": "Transformer",
 "tags": ["shrink", "fatten", "epaisseur", "gonfler", "inflater"],
 "func": lambda: bpy.ops.transform.shrink_fatten()},

{"name": "Trackball Rotation", "icon": "FORCE_VORTEX", "category": "Transformer",
 "tags": ["trackball", "rotation libre", "rotation trackball"],
 "func": lambda: bpy.ops.transform.trackball()},

{"name": "Edge Slide", "icon": "UV_EDGESEL", "category": "Transformer",
 "tags": ["edge slide", "glisser arete", "slide edge"],
 "func": lambda: bpy.ops.transform.edge_slide()},

{"name": "Vertex Slide", "icon": "VERTEXSEL", "category": "Transformer",
 "tags": ["vertex slide", "glisser sommet", "slide vertex"],
 "func": lambda: bpy.ops.transform.vert_slide()},

{"name": "Mirror Transform", "icon": "MOD_MIRROR", "category": "Transformer",
 "tags": ["mirror", "miroir", "symetrie", "mirroir"],
 "func": lambda: bpy.ops.transform.mirror()},

{"name": "Aligner Objets", "icon": "ALIGN_CENTER", "category": "Transformer",
 "tags": ["align", "aligner", "alignement", "centrer", "alligner", "alligenement"],
 "func": lambda: bpy.ops.object.align()},


#  APPLY TRANSFORM


{"name": "Appliquer Location", "icon": "CHECKMARK", "category": "Transformer",
 "tags": ["apply location", "fix position", "appliquer position"],
 "func": lambda: bpy.ops.object.transform_apply(location=True)},

{"name": "Appliquer Rotation", "icon": "CHECKMARK", "category": "Transformer",
 "tags": ["apply rotation", "fix rotation", "appliquer rotation"],
 "func": lambda: bpy.ops.object.transform_apply(rotation=True)},

{"name": "Appliquer Scale", "icon": "CHECKMARK", "category": "Transformer",
 "tags": ["apply scale", "fix taille", "appliquer scale"],
 "func": lambda: bpy.ops.object.transform_apply(scale=True)},

{"name": "Appliquer Tout", "icon": "CHECKMARK", "category": "Transformer",
 "tags": ["apply all", "fix transform", "appliquer tout"],
 "func": lambda: bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)},


#  CLEAR TRANSFORM


{"name": "Clear Location", "icon": "X", "category": "Transformer",
 "tags": ["reset position", "clear location", "reset location", "position reset"],
 "func": lambda: bpy.ops.object.location_clear()},

{"name": "Clear Rotation", "icon": "X", "category": "Transformer",
 "tags": ["reset rotation", "clear rotation", "rotation reset"],
 "func": lambda: bpy.ops.object.rotation_clear()},

{"name": "Clear Scale", "icon": "X", "category": "Transformer",
 "tags": ["reset scale", "clear scale", "scale reset"],
 "func": lambda: bpy.ops.object.scale_clear()},


   
    #  MODÉLISATION

    {"name": "Extruder", "icon": "MOD_SOLIDIFY", "category": "Modéliser",
     "tags": ["extrude", "tirer"],
     "func": lambda: bpy.ops.mesh.extrude_region_move()},

    {"name": "Inset", "icon": "MOD_SOLIDIFY", "category": "Modéliser",
     "tags": ["inset", "encoche"],
     "func": lambda: bpy.ops.mesh.inset()},

    {"name": "Loop Cut", "icon": "MOD_BEVEL", "category": "Modéliser",
     "tags": ["loopcut", "coupe"],
     "func": lambda: bpy.ops.mesh.loopcut_slide()},

    {"name": "Bevel", "icon": "MOD_BEVEL", "category": "Modéliser",
     "tags": ["biseau", "bevel"],
     "func": lambda: bpy.ops.mesh.bevel()},

    {"name": "Subdivision Surface", "icon": "MOD_SUBSURF", "category": "Modéliser",
     "tags": ["subdivision", "lisser"],
     "func": lambda: bpy.ops.object.modifier_add(type='SUBSURF')},

    {"name": "Shade Smooth", "icon": "SHADING_RENDERED", "category": "Modéliser",
     "tags": ["smooth", "lisse"],
     "func": lambda: bpy.ops.object.shade_smooth()},

    {"name": "Shade Flat", "icon": "SHADING_SOLID", "category": "Modéliser",
     "tags": ["flat"],
     "func": lambda: bpy.ops.object.shade_flat()},

    
    #  GÉNÉRAL
  

    {"name": "Supprimer", "icon": "TRASH", "category": "Général",
     "tags": ["delete", "effacer"],
     "func": lambda: bpy.ops.object.delete()},

    {"name": "Dupliquer", "icon": "DUPLICATE", "category": "Général",
     "tags": ["copier", "double"],
     "func": lambda: bpy.ops.object.duplicate_move()},

    {"name": "Joindre", "icon": "AUTOMERGE_ON", "category": "Général",
     "tags": ["join", "fusionner"],
     "func": lambda: bpy.ops.object.join()},

    {"name": "Mode Édition", "icon": "EDITMODE_HLT", "category": "Général",
     "tags": ["edit mode"],
     "func": lambda: bpy.ops.object.mode_set(mode='EDIT')},

    {"name": "Mode Objet", "icon": "OBJECT_DATAMODE", "category": "Général",
     "tags": ["object mode"],
     "func": lambda: bpy.ops.object.mode_set(mode='OBJECT')},

 
    #  RENDU
 

    {"name": "Rendu Image", "icon": "RENDER_STILL", "category": "Rendu",
     "tags": ["render", "photo"],
     "func": lambda: bpy.ops.render.render(write_still=True)},


    #  MODE ULTRA SIMPLE
 

   {"name": "AHH Y'A TROP D'INFO (Mode Plein Écran)", 
     "icon": "FULLSCREEN_ENTER", 
     "category": "Ultra Simple",
     "tags": ["trop", "simple", "focus"],
     "func": lambda: bpy.ops.screen.screen_full_area()},
]



#  MOTEUR DE RECHERCHE INTELLIGENT


def get_filtered_actions(query):

    if not query:
        return ACTIONS

    query = normalize(query)
    words = expand_words(query.split())

    scored = []

    for action in ACTIONS:

        score = 0

        name = normalize(action["name"])
        category = normalize(action["category"])
        tags = [normalize(t) for t in action["tags"]]

        searchable = [name, category] + tags

        for word in words:

            for field in searchable:

                if word == field:
                    score += 12

                elif word in field:
                    score += 7

                else:
                    similarity = difflib.SequenceMatcher(None, word, field).ratio()
                    if similarity > 0.65:
                        score += similarity * 6

        if score > 0:
            scored.append((score, action))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [item[1] for item in scored]


#  OPÉRATEUR


class SIMPLE_OT_RunAction(bpy.types.Operator):
    bl_idname = "simple.run_action"
    bl_label = "Run Action"

    action_index: bpy.props.IntProperty()

    def execute(self, context):
        ACTIONS[self.action_index]["func"]()
        return {'FINISHED'}


#  PANEL


class VIEW3D_PT_SimpleSmartPanel(bpy.types.Panel):
    bl_label = "Assistant Intelligent Blender"
    bl_idname = "VIEW3D_PT_simple_smart_blender"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Assistant'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

      
        # Barre de recherche
    
        col = layout.column()
        col.scale_y = 1.6
        col.prop(scene, "simple_search", text="", icon='VIEWZOOM')
        layout.separator()

     
        # Bouton Mode Ultra Simple (toujours visible)
     
        layout.label(text="Mode Ultra Simple", icon='FULLSCREEN_ENTER')
        row = layout.row()
        row.scale_y = 1.6
        row.operator(
            "simple.run_action",
            text="AHH Y'A TROP D'INFO",
            icon="FULLSCREEN_ENTER"
        ).action_index = len(ACTIONS) - 1  # le dernier de la liste = Mode Ultra Simple
        layout.separator()

    
        # Boutons filtrés par recherche
     
        filtered = get_filtered_actions(scene.simple_search)

        if scene.simple_search and not filtered:
            layout.label(text="Aucune action trouvée", icon='ERROR')
            return

        current_category = ""
        for action in filtered:

            if action["category"] == "Ultra Simple":
                continue  # ne pas répéter le bouton Ultra Simple dans les résultats

            if action["category"] != current_category:
                layout.separator()
                layout.label(text=action["category"], icon="DOT")
                current_category = action["category"]

            row = layout.row()
            row.scale_y = 1.6

            op = row.operator(
                "simple.run_action",
                text=action["name"],
                icon=action["icon"]
            )
            op.action_index = ACTIONS.index(action)


# REGISTRATION


classes = (
    SIMPLE_OT_RunAction,
    VIEW3D_PT_SimpleSmartPanel,
)

def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.simple_search = bpy.props.StringProperty(name="Recherche")

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

    del bpy.types.Scene.simple_search

if __name__ == "__main__":
    register()
