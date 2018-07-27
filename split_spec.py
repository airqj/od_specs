import xmltodict,os
from PIL import Image

path = "/home/qinjianbo/DATA/od_specs/大胡笳_0.xml"
path_specs_p = "/home/qinjianbo/DATA/specs/positive/"
path_specs_n = "/home/qinjianbo/DATA/specs/negetive/"
path_od_specs = "/home/qinjianbo/DATA/od_specs/"


def parse_xml(path):
    data_str = open(path).read()
    data_dict = xmltodict.parse(data_str)

    objects = data_dict['annotation']['object']
    filename = data_dict['annotation']['filename']
    path_img = data_dict['annotation']['path']
    width = 20
    img = Image.open(path_img)
    count_p = 0
    count_n = 0
    last_max = 0
    for item in objects:
        xmin = int(item['bndbox']['xmin'])
        xmax = int(item['bndbox']['xmax'])

        if((xmin - last_max) > width):
            for i in range(int((xmin - last_max) % width)):
                n_point_start = last_max + i * width
                n_point_end   = n_point_start + width
                if(n_point_end < xmin):
                    pass
                else:
                    break
                box_n = (n_point_start,0,n_point_end,img.size[1])

                croped_img = img.crop(box_n)
                path_cropped_spec = path_specs_n + filename.split(".")[0] + "_" + str(count_n) + ".png"
                croped_img.save(path_cropped_spec)
                count_n +=1

        last_max = xmax

        point_start = int((xmin + xmax ) / 2 - width/2)

        box_p = (point_start,0,point_start + width,img.size[1]) # positive box

        croped_img = img.crop(box_p)
        path_cropped_spec = path_specs_p + filename.split(".")[0] + "_" + str(count_p) + ".png"
        croped_img.save(path_cropped_spec)
        count_p +=1

def parser(path_specs):
    for file in os.listdir(path_specs):
        if(file.endswith("xml")):
            print(file)
            pass
        else:
            continue
        path_file = path_specs + file
        parse_xml(path_file)

if __name__ == '__main__':
    parser(path_od_specs)
