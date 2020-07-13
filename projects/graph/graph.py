"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if (v1 in self.vertices) and (v2 in self.vertices):
            self.vertices[v1].add(v2)
        else:
            "Invalid vertex detected"

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # Create queue
        q = Queue()
        # Create storage variable for visited vertices
        visited = set()

        # Add starting vertex to the queue
        q.enqueue(starting_vertex)

        # Navigate through vertices while the queue is not empty
        while q.size() > 0:
            # Dequeue a vertex
            vertex = q.dequeue()
            # Add the current vertex to the visited set
            visited.add(vertex)
            # Print the current vertex
            print(vertex)
            # Get the neighbors of current vertex
            neighbors = self.get_neighbors(vertex)
            for neighbor in neighbors:
                # If a neighbor is not in the visited set...
                if neighbor not in visited:
                    # Add to the queue
                    q.enqueue(neighbor)


    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # Create stack
        stack = Stack()
        # Create set for vertices pushed on the stack
        pushed_to_stack = set()

        # Add starting vertex to stack
        stack.push(starting_vertex)
        # Add the starting vertex to the pushed to stack set
        pushed_to_stack.add(starting_vertex)

        # Navigate through vertices in the stack while it's not empty
        while stack.size() > 0:
            # Pop the top vertex from the stack
            vertex = stack.pop()
            # Print the current vertex
            print(vertex)
            # Get the neighbors or the current vertex to loop through
            neighbors = self.get_neighbors(vertex)
            for neighbor in neighbors:
                # Check if already pushed onto stack
                if neighbor not in pushed_to_stack:
                    # Push on the stack
                    stack.push(neighbor)
                    # Add to the pushed to stack set
                    pushed_to_stack.add(neighbor)


    def dft_recursive(self, starting_vertex, visited=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        # Check if visited has not been created yet
        if visited == None:
            # Create it
            visited = set()
        # Add the current vertex to visited
        visited.add(starting_vertex)
        # Print the current vertex
        print(starting_vertex)
        # For each vertex found in the connected vertices of the current one
        for vertex in self.vertices[starting_vertex]:
            # If it's not in the visited set
            if vertex not in visited:
                # Recurse on that new vertex and pass in the visited set
                self.dft_recursive(vertex, visited=visited)

        
    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # Create the q
        q = Queue()
        # Set for visited vertices
        visited = set()

        # Put starting vertex on the queue as a list
        q.enqueue([starting_vertex])

        # Work until destination vertex is found
        while q.size() > 0:
            # Get first vertex from queue
            vertex_path = q.dequeue()

            # Get the last vertex of the current path
            vertex = vertex_path[-1]

            # Check if the vertex has been visited
            if vertex not in visited:
                # Check if it's the vertex we need
                if vertex == destination_vertex:
                    # Return the current path
                    return vertex_path
                
                # Add the vertex to the visited set
                visited.add(vertex)

                # Queue up each connected vertex by making a new path
                # for each branch that can be followed
                for next_vertex in self.get_neighbors(vertex):
                    next_path = list(vertex_path)
                    next_path.append(next_vertex)
                    q.enqueue(next_path)


    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        # Create the stack
        stack = Stack()
        # Set for visited vertices
        visited = set()

        # Put the starting vertex on the stack as a list
        stack.push([starting_vertex])

        # While the stack is not empty and the destination hasn't been found
        while stack.size() > 0:
            # Get the first pathway on the stack
            vertex_path = stack.pop()

            # Look at the last vertex in the current path
            vertex = vertex_path[-1]

            # Check if this vertex has been visited
            if vertex not in visited:
                # If the vertex is the destination we're done
                if vertex == destination_vertex:
                    return vertex_path
                
                # Add the vertex to the visited set
                visited.add(vertex)

                # Push each connected vertex on stack by making a new path
                # for each branch that can be followed
                for next_vertex in self.get_neighbors(vertex):
                    next_path = list(vertex_path)
                    next_path.append(next_vertex)
                    stack.push(next_path)



    def dfs_recursive(self, starting_vertex, destination_vertex, visited=None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        # # Check if visited has not been created yet
        # if not visited:
        #     # Create it
        #     visited = set()
        
        # # Add the current vertex to visited
        # visited.add(starting_vertex)
        pass



if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
