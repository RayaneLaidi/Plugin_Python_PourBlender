bl_info = {
    "name": "Tableau des raccourcis Blender",
    "author": "Eva",
    "version": (1, 0, 0),
    "blender": (4, 3, 0),
    "location": "View3D > Sidebar > Shortcuts",
    "description": "Affiche un tableau des raccourcis clavier de Blender dans l'interface", # au lieu de les chercher pendant longtemps
    "category": "Interface",
}

import bpy

class Table:
    def __init__(self, title, columns, rows):
        self.title = title
        self.columns = columns
        self.rows = rows


TABLES = [

    Table(
        "INTERFACE",
        ["Nom", "Raccourci clavier"],
        [
            ["Barre d'outils", "T"],
            ["Paramètres contextuels", "N"],
            ["Bascule vers mode Édition", "Tab"],
            ["Changer de mode (menu circulaire)", "Ctrl + Tab"],
        ],
    ),

    Table(
        "ACTIONS GÉNÉRALES",
        ["Nom", "Raccourci clavier"],
        [
            ["Ajouter un objet", "Maj + A"],
            ["Supprimer un objet", "X / Suppr"],
            ["Déplacer", "G"],
            ["Tourner", "R"],
            ["Modifier la taille", "S"],
            ["Déplacer sur X / Y / Z", "G puis X, Y ou Z"],
            ["Dupliquer", "Maj + D"],
            ["Mouvement précis", "Maintenir Maj"],
            ["Mouvement progressif", "Maintenir Ctrl"],
            ["Générer un rendu", "F12"],
        ],
    ),

    Table(
        "SÉLECTION",
        ["Nom", "Raccourci clavier"],
        [
            ["Sélectionner", "Clic gauche"],
            ["Tout sélectionner", "A"],
            ["Tout désélectionner", "Alt + A"],
            ["Sélection boîte", "B"],
            ["Inverser sélection", "Ctrl + I"],
        ],
    ),

    Table(
        "NAVIGATION",
        ["Nom", "Raccourci clavier"],
        [
            ["Orbiter", "Bouton milieu souris"],
            ["Se focaliser sur l'objet", ". (pavé num.)"],
            ["Translation caméra", "Maj + bouton milieu"],
            ["Zoom", "Molette souris"],
        ],
    ),

    Table(
        "MODE OBJET",
        ["Nom", "Raccourci clavier"],
        [
            ["Mode Objet / Édition", "Tab"],
            ["Mode de rendu", "Z"],
            ["Réinitialiser position", "Alt + G"],
            ["Réinitialiser rotation", "Alt + R"],
            ["Réinitialiser taille", "Alt + S"],
            ["Appliquer transformations", "Ctrl + A"],
            ["Joindre objets", "Ctrl + J"],
            ["Centrer curseur 3D", "Maj + C"],
        ],
    ),

    Table(
        "MODE ÉDITION",
        ["Nom", "Raccourci clavier"],
        [
            ["Mode Point / Arête / Face", "1 / 2 / 3"],
            ["Sélection boucle", "Alt + Clic gauche"],
            ["Sélection pinceau", "C"],
            ["Dépliage UV", "U"],
        ],
    ),

    Table(
        "MODÉLISATION",
        ["Nom", "Raccourci clavier"],
        [
            ["Extruder", "E"],
            ["Inset", "I"],
            ["Biseau", "Ctrl + B"],
            ["Loop Cut", "Ctrl + R"],
            ["Couteau", "K"],
            ["Fill", "F"],
            ["Inverser normales", "Ctrl + Maj + N"],
            ["Édition proportionnelle", "O"],
        ],
    ),

    Table(
        "VUE 3D (PAVÉ NUMÉRIQUE)",
        ["Direction", "Raccourci clavier 1", "Raccourci clavier 2"],
        [
            ["7 (Vue de dessus)", "8 (Monter)", "9 (Vue opposée)"],
            ["4 (Vers la gauche)", "5 (Perspective)", "6 (Vers la droite)"],
            ["1 (Vue de face)", "2 (Descendre)", "3 (Vue de côté)"],
            ["0\n(Vue de la caméra)", ". (Se focaliser sur l'objet)", "c'est un point"],
        ],
    ),
]

# avec barre de recherche

def match_search(text, search):
    return search in text.lower()


def draw_table(layout, table: Table, search: str):
    # Filtrage des lignes
    filtered_rows = []
    for row in table.rows:
        if any(match_search(str(cell), search) for cell in row):
            filtered_rows.append(row)

    # Si aucune ligne ne correspond, ne pas afficher le tableau
    if search and not filtered_rows and not match_search(table.title.lower(), search):
        return 

    box = layout.box()
    box.label(text=table.title, icon='KEYINGSET')

    header = box.row()
    for col in table.columns:
        header.label(text=col)

    box.separator()

    rows_to_draw = filtered_rows if search else table.rows

    for row_data in rows_to_draw:
        row = box.row()
        for cell in row_data:
            row.label(text=str(cell))


# Panel UI

class VIEW3D_PT_shortcuts_tables(bpy.types.Panel):
    bl_label = "Raccourcis Blender"
    bl_idname = "VIEW3D_PT_shortcuts_tables"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Shortcuts'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Barre de recherche
        layout.prop(scene, "shortcuts_search", text="", icon='VIEWZOOM')
        layout.separator()

        search = scene.shortcuts_search.lower().strip()

        for table in TABLES:
            draw_table(layout, table, search)
            layout.separator()


# Registration

def register():
    bpy.types.Scene.shortcuts_search = bpy.props.StringProperty(
        name="Recherche",
        description="Rechercher un raccourci ou une action",
        default="",
    )

    bpy.utils.register_class(VIEW3D_PT_shortcuts_tables)


def unregister():
    del bpy.types.Scene.shortcuts_search
    bpy.utils.unregister_class(VIEW3D_PT_shortcuts_tables)


if __name__ == "__main__":
    register()
