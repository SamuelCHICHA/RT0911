from typing import Tuple
from typing import Union

class Graph:
    def __init__(self, matrix : dict) -> None:
        """Crée un graphe à partir d'une matrice

        Args:
            matrix (list): matrice d'adjacence
        """
        self._matrix = matrix

    def dijkstra(self, source: Union[str, int]) -> Tuple[list, list]:
        """Crée une arborescence en utilisant l'algorithme de dijkstra

        Args:
            source (int): sommet de départ

        Returns:
            Tuple[list, list]: distances depuis le sommet de départ, pères dans l'arborescence
        """
        distances = {}
        previous = {}
        visited = {}
        queue = []
        # Maximum graph weight
        # Initialisation
        for vertice in self._matrix.keys():
            visited[vertice] = False
            distances[vertice] = float('inf')
            previous[vertice] = None
            queue.append(vertice)
        distances[source] = 0
        while len(queue) != 0:
            # On recherche l'index du sommet le plus près
            unvisited_vertices = {vertice: distance for vertice, distance in distances.items() if not visited[vertice] and distances[vertice] is not None}
            if unvisited_vertices == {}:
                raise ValueError("The queue is not empty.")
            min_index = min(unvisited_vertices, key=unvisited_vertices.get)
            # On le récupère dans la queue
            u = queue.pop(queue.index(min_index))
            visited[u] = True
            # Pour chaque sommet
            for vertice, edge_weight in self._matrix[u].items():
                # On regarde si c'est un sommet voisin du sommet parsé
                if edge_weight is not None:
                    alt = distances[u] + edge_weight
                    # On regarde si la distance alternative est plus petite que celle actuelle et on la change si c'est le cas
                    if distances[vertice] is None or alt < distances[vertice]:
                        distances[vertice] = alt
                        previous[vertice] = u
        return distances, previous
            
    def shortest_path(self, source: Union[str, int], target: Union[str, int]) -> list:
        """Permet de récupérer le chemin le plus court à partir d'une arborescence (dijkstra)

        Args:
            source (int): sommet de départ
            target (int): sommet d'arrivée

        Returns:
            list: chemin du sommet de départ jusqu'au sommet d'arrivée
        """
        path = [target]
        # On récupère l'arborescence
        _, previous = self.dijkstra(source)
        prev = previous[target]
        # On la remonte jusqu'à trouver le sommet de départ
        while prev is not None:
            path.append(prev)
            prev = previous[prev]
        # On inverse le chemin
        path.reverse()
        return path
