import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import PIL
from djsetslow import ListSet, IDsSet
from unionfind import UFNaive, UFFast
from skimage.transform import resize
import time
from collections import defaultdict

def load_cells_grayscale(filename, n_pixels = 0):
    """
    Load in a grayscale image of the cells, where 1 is maximum brightness
    and 0 is minimum brightness

    Parameters
    ----------
    filename: string
        Path to image holding the cells
    n_pixels: int
        Number of pixels in the image
    """
    cells_original = plt.imread(filename)
    cells_grey = np.asarray(PIL.Image.fromarray(cells_original).convert('L'))
    cells_grey = ndimage.uniform_filter(cells_grey, size=10)
    cells_grey = cells_grey - np.min(cells_grey)
    cells_grey = cells_grey/np.max(cells_grey)
    N = int(np.sqrt(n_pixels))
    if n_pixels > 0:
        cells_grey = resize(cells_grey, (N, N), anti_aliasing=True)
    return cells_grey

def get_cell_labels(I, thresh, uf_class = UFNaive):
    """
    Parameters
    ----------
    I: ndarray(M, N)
        A grayscale image of cells
    thresh: float
        Threshold above which to consider something inside a cell
    uf_class: class
        A data structure that implements the union find ADT.
        Must contain the methods union(i, j), find(i, j), and
        get_set_label(i)
    
    Returns
    -------
    labels: ndarray(M, N)
        An array of labels for the pixels in the image
    """
    
    M = I.shape[0]
    N = I.shape[1]
    
    # This is the disjoint set object on which you will 
    # call union, find, and get_set_label
    djset = uf_class(M*N) 
    # This is the 2D array of labels that you will fill
    # in and return
    labels = np.ones((M, N), dtype=int) 
    
    ## TODO: Fill this in
    ## Formula - (x * numRows) + column
            
    ## Check for each sorrounding cells eligibility for unionization
    for y in range(N-1):
        for x in range(M-1):
            if I[x, y] >= thresh:
                i = (x * M) + y
                if I[x + 1, y] >= thresh:
                    j = ((x+1) * M) + y
                    djset.union(int(i), int(j))
                if I[x + 1, y + 1] >= thresh:
                    j = ((x+1) * M) + (y+1)
                    djset.union(int(i), int(j))
                if I[x, y + 1] >= thresh:
                    j = (x * M) + (y+1)
                    djset.union(int(i), int(j))
    
    for y in range(N):
        for x in range(M):
            labels[x, y] = djset.get_set_label((x * M) + y)
            
    return labels

def permute_labels(labels):
    """
    Shuffle around labels by raising them to a prime and
    modding by a large-ish prime, so that cells are easier
    to see against their backround
    Parameters
    ----------
    labels: ndarray(M, N)
        An array of labels for the pixels in the image

    Returns
    -------
    labels_shuffled: ndarray(M, N)
        A new image where the labels are different but still
        the same within connected components
    """
    return (labels**31) % 833


def get_cluster_centers(labels):
    """
    Compute an array that holds the row and column of the
    mean of each label location that has more than 1 pixel
    assigned to it

    Parameters
    ----------
    labels: ndarray(M, N)
        An array of labels for the pixels in the image
    
    Returns
    -------
    X: ndarray(K, 2)
        An array of average row/column indices of each of the
        K labels that had at least 2 pixels assigned to them
    """
    ## TODO: Fill this in
    
    M = labels.shape[0]
    N = labels.shape[1]
    
    ret = [[0,0]]
    
    label_dict = defaultdict(list)
    
    for y in range(M):
        for x in range(N):
            add = [y, x]
            label_dict[labels[y, x]].append(add)
    
    for i in label_dict:
            x = 0
            y = 0
            total = 0
            arr = label_dict[i]
            for a in arr:
                x += a[0]
                y += a[1]
                total += 1
            if total > 1:
                f = (x/total)
                g = (y/total)
                ret.append([g, f])
    
    return ret # This is a dummy value, but you should return
    # a list of [row, column] lists representing the centers

def time_test():
    thresh = 0.7
    n_pixels = []
    times_idsset = []
    times_uffast = []
    for n in range(100, 100*100, 500):
        n_pixels.append(n)
        I = load_cells_grayscale("Cells.jpg", n)
        ## TODO: Fill this in.  Take an average of the average
        ## time that it takes per operation to run get_cell_labels
        ## for both the IDsSet and the UFFast implementation of
        ## union find, and store these times in times_idsset
        ## and times_uffast, respectively
        avgs = 0
        tic = time.time()
        get_cell_labels(I, thresh)
        elapsed = time.time()-tic
        avgs += elapsed/n
        times_idsset.append(avgs)
        
        avgf = 0
        tic2 = time.time()
        get_cell_labels(I, thresh, UFFast)
        elapsed = time.time()-tic2
        avgf += elapsed/n
        times_uffast.append(avgf)
            
    plt.plot(n_pixels, times_idsset)
    plt.plot(n_pixels, times_uffast)
    plt.legend(["IDsSet", "UFFast"])
    plt.xlabel("Number of pixels")
    plt.ylabel("Average Elapsed Time Per Operation")
    plt.savefig("Timings.png", bbox_inches='tight')

if __name__ == '__main__':
    # Put stuff here that will run when you hit the play button
    """ 
    Test for time_test
    """
    time_test()
    
    
    """
    Test for Get Cell Labels
    """
    """
    thresh = 0.8
    I = load_cells_grayscale("Cells.jpg")
    labels = get_cell_labels(I, thresh)
    plt.imshow(permute_labels(labels))
    plt.savefig("labels.png", bbox_inches='tight')
    """
    """
    Test For Get Cell Centers
    """
    """
    thresh = 0.7
    I = load_cells_grayscale("Cells.jpg")
    labels = get_cell_labels(I, thresh)
    cells_original = plt.imread("Cells.jpg")
    X = get_cluster_centers(labels)
    X = np.array(X)
    plt.imshow(cells_original)
    plt.scatter(X[:, 1], X[:, 0], c='C2')
    plt.savefig("cells_marked.png")
    """
    
    """
    Original __main__ that came w skeleton code
    ------------------
    
    thresh = 0.7
    I = load_cells_grayscale("Cells.jpg")
    labels = get_cell_labels(I, thresh)
    plt.imshow(permute_labels(labels))
    plt.savefig("labels.png", bbox_inches='tight')
    cells_original = plt.imread("Cells.jpg")
    X = get_cluster_centers(labels)
    plt.imshow(cells_original)
    plt.scatter(X[:, 1], X[:, 0], c='C2')
    plt.savefig("cells_marked.png")"""