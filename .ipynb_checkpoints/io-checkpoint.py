import cv2
import numpy as np
import os
import re

def load_image_stack(folder):
    images = []
    # Filtrar apenas arquivos .tiff e ordená-los pelo nome
    tiff_files = sorted([f for f in os.listdir(folder) if re.match(r'.*\.tif$', f)], key=lambda x: int(re.findall(r'\d+', x)[0]))
    
    for filename in tiff_files:
        img = cv2.imread(os.path.join(folder, filename), cv2.IMREAD_UNCHANGED)
        if img is not None:
            images.append(img)
    
    return np.stack(np.array(images), axis=0)

def cv2_imshow(n_imgs, sets):
    x = 0
    for s in sets:
        x+=1
        combined_image = np.concatenate(([s[n-1] for n in n_imgs]), axis=1)
        cv2.imshow(f'Compare Images {x}', combined_image)
        
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True

def blend(imgs):
    blend_img = imgs[0]
    # Iterar sobre as imagens restantes para mesclá-las
    for img in imgs[1:]:
        # Carregar a próxima imagem
        # Mesclar a imagem com a imagem mesclada atual
        blend_img = cv2.addWeighted(blend_img, 1, img, 0.5, 0)

    # Mostrar a imagem mesclada
    cv2.imshow('blend_img', blend_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def download(images, path):
    save_all = True
    for idx, img in enumerate(images):
        if cv2.imwrite(f"{path}/{idx+1}.tif", img):
            pass
        else:
            print(f"Error download(images[{idx}])")
            save_all = False
    return save_all



