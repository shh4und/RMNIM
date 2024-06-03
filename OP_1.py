# # Olfactory Projection Fibers (OP_1)

from ip.ios import *
from ip.enhancement import *
from ip.binary import *
from ip.graph import *
from ip.swc import *
from ip.split import *
from skimage.morphology import skeletonize

# ## Read Data

folder_path = "./OlfactoryProjectionFibers/ImageStacks/OP_1"

images = load_image_stack(folder_path)

# ## Code Process and Execution

split = split_and_process_stack(images, 10, 3)

skel = skeletonize(split)


# ### For visualization purposes only

blend = blended(skel)
single_download(blend, "./Test/Images/OP_1.png")
blend_og = blended(images)
single_download(blend_og, "./Test/Images/OPOG_1.png")

# ### Graph generation

print("Creating graph...")
graph = Graph(skel)
graph.set_root((2, 429, 33))
graph.create_graph()
print("Graph created.")
root = graph.get_root()
print(f"Root set: {root}")
# OP_1 (X,Y,Z): (30.979,429.04,0)


distances, parents, labels = graph.dijkstra()

print(f"{len(distances)}, {len(parents)}, {len(labels)}")

swc = SWCFile("./Test/OP_1.swc")

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

print(f"swc generated: {swc.write_file()} with {len(swc.data)} nodes" )

