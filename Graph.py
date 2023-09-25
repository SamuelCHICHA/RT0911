from typing import Tuple

class Graph:
    def __init__(self, matrix : list) -> None:
        """Crée un graphe à partir d'une matrice

        Args:
            matrix (list): matrice d'adjacence
        """
        self._matrix = matrix

    def dijkstra(self, source: int) -> Tuple[list, list]:
        """Crée une arborescence en utilisant l'algorithme de dijkstra

        Args:
            source (int): sommet de départ

        Returns:
            Tuple[list, list]: distances depuis le sommet de départ, pères dans l'arborescence
        """
        distances = {}
        previous = {}
        queue = []
        visited = [False for _ in range(len(self._matrix))]
        # Intialisation
        for i in range(len(self._matrix)):
            distances[i] = None
            previous[i] = None
            queue.append(i)
        distances[source] = 0
        while len(queue) != 0:
            min = None
            min_index = None
            # On recherche l'index du sommet le plus près
            for key, value in distances.items():
                if visited[key] == False and value is not None and (min is None or min > value):
                    min = value
                    min_index = key
            # On le récupère dans la queue
            u = queue.pop(queue.index(min_index))
            visited[u] = True
            # Pour chaque sommet
            for i in range(len(self._matrix[u])):
                # On regarde si c'est un sommet voisin du sommet parsé
                if self._matrix[u][i] == 1:
                    alt = distances[u] + self._matrix[u][i]
                    # On regarde si la distance alternative est plus petite que celle actuelle et on la change si c'est le cas
                    if distances[i] is None or alt < distances[i]:
                        distances[i] = alt
                        previous[i] = u
        return distances, previous
            
    def shortest_path(self, source: int, target: int) -> list:
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
