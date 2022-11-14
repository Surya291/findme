# imports 

import numpy as np
import dlib
import face_recognition
import matplotlib.pyplot as plt 
import matplotlib.patches as patches 
import os
from PIL import Image
from sklearn.cluster import AgglomerativeClustering
from collections import defaultdict
import shutil

class unit:
    def __init__(self, iid, fid):
        self.iid = iid
        self.fid = fid

## method returning img title, fid, latents : input image_path

class findme(unit):
    def __init__(self,direc): 
        '''
        Takes in directory for iteration , without '/' at the end
        '''
        
        self.direc = direc #direc to iterate 
        self.encod_list = []
        self.units_list = []
        

    def img2vec(self):
        '''
        creates a list of encodings and fid for a given image file
        '''

        self.file_path = self.direc + '/' +  self.img_title
        if(os.path.isfile(self.file_path)):
            
            self.img = face_recognition.load_image_file(str(self.file_path))

            self.img_face_encod = face_recognition.face_encodings(self.img) # list of encodings (arr of 128-d vec)
            self.img_fid =  list(range(len(self.img_face_encod)))           # list of fid : [0,1,2,3,4]

    def update_lists(self) : 
        '''
        updates the encod_list and units_list by creating for a unit for each face
        '''
        
        self.encod_list.extend(self.img_face_encod)
        
        for i in self.img_fid:
            self.units_list.append( unit(iid = self.img_title , fid = i) )
        
    
        
    def iterate_direc(self): #1
        '''
        Iterates over the images in the direc
        --> detects faces -->  converts into encodings --> Stores them as list
        
        At the end we have a list of encodings ready for clustering
        '''
        for self.img_title in os.listdir(self.direc):
            self.img2vec()
            self.update_lists()
            
            
    def clusterize(self, threshold = 0.6): #2
        '''
        Given the encod list find clusters --> return cluster_list
        '''
        
        self.clustering = AgglomerativeClustering( n_clusters = None, distance_threshold = threshold).fit(self.encod_list)
        self.cluster_list = self.clustering.labels_
        
    def create_dicts(self):
        '''
        i2c -> dict with showing how many clusters(id) belong to a single image
        c2i -> how many images belong to a given cluster id
        '''
        
        self.i2c =  defaultdict(set)
        self.c2i =  defaultdict(list)
        
        # creating i2c list
        self.i2c_list = defaultdict(list)
        
        for _idx, _unit in enumerate(self.units_list):
            
            self.i2c[_unit.iid].add(self.cluster_list[_idx])
            
            self.c2i[ self.cluster_list[_idx] ].append(_unit.iid)
            self.i2c_list[_unit.iid].append(self.cluster_list[_idx])
            
    def create_display_i2c(self): 
        '''
        input i2c output : display_i2c : containing images to be displayed with unique faces(almost) to be named
        
        Inorder to display as low images as possible for naming the detected cluster.
        
        Iterates through i2c to pick the image with max no. of unnamed faces , uses a set(cluster_set) to 
        keep track of what all clusters are already part of display_i2c.
        '''
        self.create_dicts()
        
        self.display_i2c = defaultdict(list)
        self.cluster_set = set(self.cluster_list) # set to keep a watch of what clusters are left
        
        # temporary variables used for iterating
        
        self.temp_dict = self.i2c
        self.temp_set = self.cluster_set
        

        while (self.temp_set != set()):
            
            '''
            max keys are the key in the dict whose len of the set is high --> meaning trying
            to find image with most unseen faces 
            '''

            (max_key, max_val) = max(self.temp_dict.items(), key = lambda item: len(item[1]))
            self.display_i2c[max_key] = self.i2c_list[max_key] # copying the max keys from i2c 
            
            self.temp_set = self.temp_set - max_val
            
            del self.temp_dict[max_key] ## del the max key entry from temp dict to find other new clusters
            
            for _key in self.temp_dict:
                self.temp_dict[_key] = self.temp_dict[_key] - max_val
                
    def name_the_cluster(self): #3
        '''
        We have the dict of what images to display.. 
        Need to show bbox of faces and ask to set a name
        
        If nothing is set for a cluster id : that dir will not be created
        '''
        self.create_display_i2c()
        
        self.c2name = {} # empty dict to store the name of cluster 
        

        print(self.display_i2c)
        for key,val in self.display_i2c.items():
            
            self.dis_file_path = self.direc + '/' +  key
            self.dis_img = face_recognition.load_image_file(str(self.dis_file_path))
            self.dis_face_locations = face_recognition.face_locations(self.dis_img)
            
            figure, ax = plt.subplots(1)
            ax.imshow(self.dis_img)
            
            for _idx, _c in enumerate(val):
                
                if(_c in self.cluster_set): #To show bbox for new faces only ..
                    t,r,b,l = self.dis_face_locations[_idx]
                    x,y,w, h = l, t, r-l ,b -t  ## transforming vars for plotting rectangles
                    rect = patches.Rectangle((x,y),w,h, edgecolor='r', facecolor="none")
                    ax.add_patch(rect) # Adds rectangles for each face
                    ax.text(x,y, str(_c), bbox=dict(facecolor='red', alpha=1))   # Adds its face id
                    
            ax.axis('off')
            
            im = fig2img(figure)
            im = im.convert('RGB')
            im.save('cluster/' + key)
            
            '''
            # donot require this ... the naming should be done in html and returnas c2name map..

            #plt.show()
            
            ### Asking for names
            for _idx, _c in enumerate(val):
                if(_c in self.cluster_set):
                    print("Enter a name for face id {}" .format(_c))
                    name = str(input())

                    if(name != ''):
                        self.c2name[_c] = name

            '''
            im.show()

            
            ### Deleting already recognised faces from the set
            self.cluster_set = self.cluster_set - set(val) 
        print(self.display_i2c)
            
    def create_my_dir(self,dest=None): #4
        '''
        Iterates over c2name 
        --> Creates a dir with name 
        --> Iterates over the images belonging to that cluster using c2i
        '''
        
        if(dest != None):
            self.dest = dest # Without / at the end
        else :
            self.dest = self.direc
            
        for _c,_name in self.c2name.items():
            
            self.dest_child = self.dest + '/' + str(_name)
            print('Creating {} folder ....'.format(_name))
            
            if not (os.path.isfile(self.dest_child)): # Create a new dir if there is none
                os.mkdir(self.dest_child)
            
            src_files = self.c2i[_c]
            for file_name in src_files : 
                full_file_name= os.path.join(self.direc, file_name)
                if(os.path.isfile(full_file_name)):
                    shutil.copy(full_file_name, self.dest_child)
            
        print("!!!!!!!!!!!   Donneee   !!!!!!!!!!!!")
         
def fig2data ( fig ):
    """
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    # draw the renderer
    fig.canvas.draw ( )
 
    # Get the RGBA buffer from the figure
    w,h = fig.canvas.get_width_height()
    buf = np.fromstring ( fig.canvas.tostring_argb(), dtype=np.uint8 )
    buf.shape = ( w, h,4 )
 
    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll ( buf, 3, axis = 2 )
    return buf

def fig2img(fig):
    """
    @brief Convert a Matplotlib figure to a PIL Image in RGBA format and return it
    @param fig a matplotlib figure
    @return a Python Imaging Library ( PIL ) image
    """
    # put the figure pixmap into a numpy array
    buf = fig2data ( fig )
    w, h, d = buf.shape
    return Image.frombytes( "RGBA", ( w ,h ), buf.tostring() )
        
        
if __name__ == "__main__":

	direc = 'the_office_dataset/data'
	test = findme(direc)
	test.iterate_direc()
	test.clusterize(threshold = 0.6)
	test.name_the_cluster()
    # need to input this 
	test.create_my_dir()