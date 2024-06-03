# # Olfactory Projection Fibers (OP_2)


from ip.ios import *
from ip.enhancement import *
from ip.binary import *
from ip.graph import *
from ip.swc import *
from ip.split import *
from skimage.morphology import skeletonize


# ## Read Data


folder_path = "./Olfactory Projection Fibers/Image Stacks/OP_2"


images = load_image_stack(folder_path)


# ## Code Process and Execution


from skimage.morphology import flood_fill

floodf = flood_fill(images, (40, 267, 470), 0, tolerance=235)
floodf2 = flood_fill(floodf, (48, 282, 64), 0, tolerance=90)
floodf3 = flood_fill(floodf2, (43, 251, 105), 0, tolerance=200)
floodf4 = flood_fill(floodf3, (0, 367, 52), 0, tolerance=35)


split_flood = split_and_process_stack(floodf4, 250, 5)


skel = skeletonize(split_flood)


# ### For visualization purposes only


blend = blended(skel)
single_download(blend, "./SWCs/OP_2.png")
blend_og = blended(images)
single_download(blend_og, "./SWCs/OPOG_2.png")


# ### Graph generation


graph = Graph(skel)
graph.set_root((26, 391, 1))
graph.create_graph()


root = graph.get_root()
print(root)


distances, parents, labels = graph.dijkstra()


print(len(distances), len(parents), len(labels))


swc = SWCFile("./SWCs/OP_2.swc")


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
