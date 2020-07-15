import random
from itertools import combinations

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()
    
    def fisher_yates_shuffle(self, l):
        for i in range(0, len(l)):
            random_index = random.randint(i, len(l) - 1)
            l[random_index], l[i] = l[i], l[random_index]

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for user in range(num_users):
            self.add_user(user)

        # Create friendships
        friendships = []
        for user in range(1, self.last_id + 1):
            for friend in range(user + 1, num_users + 1):
                friendship = (user, friend)
                friendships.append(friendship)
        
        # Shuffle the list of friendships using Fisher Yates Shuffle
        self.fisher_yates_shuffle(friendships)

        # Split off the number of friendships we need
        #print(len(friendships))
        friendships = friendships[:(num_users * avg_friendships)//2]
        #print(len(friendships))

        # Add friendships to network
        for friendship in friendships:
            self.add_friendship(friendship[0], friendship[1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME

        # Start with the input user. Add to the visited dictionary
        visited[user_id] = [user_id]

        # This is a list for all of the friends we need to check connections for
        to_do = []

        # Get the friends of user_id entered
        for id in self.friendships[user_id]:
            # Put each friend in to_do as a tuple with the user_id first
            to_do.append((user_id, id))

        # Iterate through the to_do list
        for tup in to_do:
            # Check if we've already put in this friend
            if tup[1] not in visited:
                # Put new friend in visited by adding onto list from old friend
                visited[tup[1]] = visited[tup[0]] + [tup[1]]
                # Add new tuples to the to_do list to go through
                for id in self.friendships[tup[1]]:
                    to_do.append((tup[1], id))


        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
