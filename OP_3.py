# Olfactory Projection Fibers (OP_3)


from ip.ios import *
from ip.enhancement import *
from ip.binary import *
from ip.graph import *
from ip.swc import *
from ip.split import *
from skimage.morphology import skeletonize


# Read Data


folder_path = "./Olfactory Projection Fibers/Image Stacks/OP_3"
# OP_3 (X,Y,Z): (93.742,179,38)
# (94,180,38)


images = load_image_stack(folder_path)


##Code Process and Execution


split = split_and_process_stack(images, 17, 3)


skel = skeletonize(split)


##For visualization purposes only


blend = blended(skel)
single_download(blend, "./SWCs/OP_3.png")
blend_og = blended(images)
single_download(blend_og, "./SWCs/OPOG_3.png")


##Graph generation


graph = Graph(skel)
graph.set_root((38, 180, 94))
graph.create_graph()


root = graph.get_root()
print(root)


distances, parents, labels = graph.dijkstra()


print(len(distances), len(parents), len(labels))


swc = SWCFile("./SWCs/OP_3.swc")


for key, item in parents.items():
    z, y, x = key
    z, y, x = float(z), float(y), float(x)
    if item == -1:
        if key == root:
            swc.add_point(labels[key], 2, x, y, z, 2.0, item)
            continue
        else:
            continue
    swc.add_point(labels[key], 2, x, y, z, 2.0, labels[item])
swc.write_file()


len(swc.data)
