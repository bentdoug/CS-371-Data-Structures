# A naive implementation of union find which can lead to long
# branches
class UFNaive:
    def __init__(self, N):
        self._parent = list(range(N))
    
    def _root(self, i):
        """
        Follow parent pointers until reaching a root
        Parameters
        ----------
        i: int
            The starting node 
        
        Returns
        -------
        The root node of i
        """
        while self._parent[i] != i:
            i = self._parent[i]
        return i

    def get_set_label(self, i):
        """
        Return a number that is the same for every element in
        the set that i is in, and which is unique to that set
        Parameters
        ----------
        i: int
            Element we're looking for
        
        Returns
        -------
        Index of the bubble containing i
        """
        return self._root(i)
    
    def find(self, i, j):
        """
        Return true if i and j are in the same component, or
        false otherwise
        Parameters
        ----------
        i: int
            Index of first element
        j: int
            Index of second element
        """
        return self._root(i) == self._root(j)
    
    def union(self, i, j):
        """
        Merge the two sets containing i and j, or do nothing if they're
        in the same set
        Parameters
        ----------
        i: int
            Index of first element
        j: int
            Index of second element
        """
        root_i = self._root(i)
        root_j = self._root(j)
        if root_i != root_j:
            self._parent[root_j] = root_i


# A fast version of union find using path compression and
# rank-based merging
class UFFast:
    def __init__(self, N):
        self._parent = list(range(N))
        self._rank = list(range(N))
    
    def _root(self, i):
        """
        Follow parent pointers until reaching a root
        Parameters
        ----------
        i: int
            The starting node 
        
        Returns
        -------
        The root node of i
        """
        while self._parent[i] != i:
            i = self._parent[i]
        return i

    def get_set_label(self, i):
        """
        Return a number that is the same for every element in
        the set that i is in, and which is unique to that set
        Parameters
        ----------
        i: int
            Element we're looking for
        
        Returns
        -------
        Index of the bubble containing i
        """
        self._parent[i] = self._root(i)
        return self._root(i)
    
    def find(self, i, j):
        """
        Return true if i and j are in the same component, or
        false otherwise
        Parameters
        ----------
        i: int
            Index of first element
        j: int
            Index of second element
        """
        
        return self._root(i) == self._root(j)
    
    def union(self, i, j):
        """
        Merge the two sets containing i and j, or do nothing if they're
        in the same set
        Parameters
        ----------
        i: int
            Index of first element
        j: int
            Index of second element
        """
        root_i = self._root(i)
        root_j = self._root(j)
        if root_i != root_j and self._rank[i] > self._rank[j]:
            self._parent[root_j] = root_i
            self._rank[i] += 1
        else:
            self._parent[root_i] = root_j
            self._rank[j] += 1