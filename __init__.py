from . import panel, shady_pencil_operator
bl_info = {
    "name": "Shady Pencil",
    "author": "AHK <https://github.com/ahkCodeder>",
    "version": (1, 3),
    "blender": (3, 3, 0),
    "category": "3D View",
    "location": "View3D",
    "description": "This turns Grease pencil strokes into Mesh Objects",
    "warning": "Lines can't be turned to Mesh obj",
    "doc_url": "https://github.com/ahkCodeder"
}


def register():

    shady_pencil_operator.register()
    panel.register()


def unregister():

    shady_pencil_operator.unregister()
    panel.unregister()


if __name__ == "__main__":
    register()
