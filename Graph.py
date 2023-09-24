class Graph:
    def __init__(self, matrix : list) -> None:
        self._matrix = matrix

    def dijkstra(self, source: int) -> list:
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
                if self._matrix[u][i] is not None and self._matrix[u][i] is not 0:
                    alt = distances[u] + self._matrix[u][i]
                    # On regarde si la distance alternative est plus petite que celle actuelle et on la change si c'est le cas
                    if distances[i] is None or alt < distances[i]:
                        distances[i] = alt
                        previous[i] = u
        return distances, previous
            
    def shortest_path(self, source: int, target: int):
        path = [target]
        _, previous = self.dijkstra(source)
        prev = previous[target]
        while prev is not None:
            path.append(prev)
            prev = previous[prev]
        path.reverse()
        return path
