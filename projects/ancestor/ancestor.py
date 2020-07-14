
def earliest_ancestor(ancestors, starting_node):
    # Create dictionary of ancestors connections
    # The tuples are in reverse order because the data is
    # (parent, child) and I want the dictionary to be {child: parent}
    family_tree = {}
    for tup in ancestors:
        if tup[1] in family_tree:
            family_tree[tup[1]].append(tup[0])
        else:
            family_tree[tup[1]] = [tup[0]]

    # Define list to store tuples for each individual and their 
    # generation level relative to the starting_node
    id_gen_list = [(starting_node, 0)]

    # Iterate through the list of individuals
    for person in id_gen_list:
        # Check if they have a key in the family tree dictionary
        if person[0] in family_tree:
            # They might branch in two directions so we need to 
            # account for that possibility
            for parent in family_tree[person[0]]:
                # Create a tuple for that parent with their
                # generation count being one higher than the child
                id_gen_list.append((parent, (person[1]+1)))
    
    # Get all of the generation values created
    gens = [tup[1] for tup in id_gen_list]

    # Get the max generation level from gens
    max_gen = max(gens)

    # Get the keys (the people) with the max_gen level
    max_gen_key = [tup[0] for tup in id_gen_list if tup[1] == max_gen]

    # Now we return the ancestor's id that is highest on the tree and 
    # with the lowest id value if necessary, or return a -1 if they 
    # have no ancestors on the tree
    if len(id_gen_list) == 1:
        return -1
    elif len(max_gen_key) > 1:
        return min(max_gen_key)
    else:
        return max_gen_key[0]
