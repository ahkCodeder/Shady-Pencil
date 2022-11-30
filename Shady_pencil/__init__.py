from Shady_pencil import operator, panel
bl_info = {
    "name": "Shady Pencil",
    "author": "AHK <https://github.com/ahkCodeder>",
    "version": (1, 0),
    "blender": (3, 3, 0),
    "category": "3D View",
    "location": "View3D",
    "description": "This turns Grease pencil strokes into Mesh Objects",
    "warning": "Lines can't be turned to Mesh obj",
    "doc_url": "https://github.com/ahkCodeder"
}


def register():

    operator.register()
    panel.register()


def unregister():

    operator.unregister()
    panel.unregister()


if __name__ == "__main__":
    register()
