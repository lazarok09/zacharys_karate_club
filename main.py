# %% Import libraries and load dataset
import networkx as nx
import matplotlib.pyplot as plt

# %% Initiate Karate Club Graph 
# G is our graph object containing nodes (members) and edges (friendships)
G = nx.karate_club_graph()


# %% Describe how many nodes are present. Also brings edges and the global degree
# https://networkx.org/documentation/stable/reference/classes/graph.html

number_of_nodes = G.number_of_nodes(); # or order() and other methods
graph_degree_global = list(G.degree);
# Degree is often called the direct friends, it measures how many edges are connected to each node
# Count of direct edges (friends). Local popularity.
number_of_edges = G.number_of_edges();

# %% Prints the leader degree - We thought it was the node 0
# But we were wrong, the leader of administration has more edges connected to him
# Let's rank to get the degree in a tuple, node/degree

# node_degree: tuple[int, int]
def degree_value(node_degree):
    node, degree = node_degree
    return degree

the_highest_degree_node= max(G.degree, key=degree_value)
leader = the_highest_degree_node[0];

# %% Prints the density. The expected output will reveal if the graph is sparse or densily connected
# For instance, a network where density is 0.13 means that 13% percent of all possible connections were made (are present).

density = nx.density;

# Output; Is not very dense, so most part of the network is sparse,
# meaning that it's very important to analyse and rank by betweness the nodes that if removed, can disconnect groups


# %% Describe and rank which 3 nodes has the highest degree centrality
# Answerr was the 33, 0 and 32. Which three nodes have the highest degree centrality
# In the context of a Karate Club, what does it mean if someone has a very high degree centrality?
# It means that they are very influential people, which nodes connect directly to them. IT does not mean that if they
# disappear, that network will be lost. That's a concept of betweness centrality.
# degree - connections, betweeness - bridges connecting more comunities. clustering - connected withim it's network tighly
# Answering the question
#

global_degree_centrality = nx.degree_centrality(G);

"""
* Q4: In the context of a Karate Club, what does it mean if someone has a very high degree centrality?
After analysing this data, we can see that the administrator, 33 node, it's higher ranked on degree centrality
Meaning that more nodes (or people) connect directly to him

"""

# %% Betweness centrality.
# Lets compare the shortest path the connections will take and compare with the most dense (high degree) nodes we have ranked
# It scores higher the nodes that are in the middle of other groups of nodes, acting like a bridge
# Our position scores the 0, 33 and 32. But, after 32, the numbers look almost the same, comes 2, 31, 8 etc.
# * Betweenness centrality measures how often a node acts as a bridge along the shortest path between two other nodes.
# Calculate the betweenness centrality for all nodes (Hint: nx.betweenness_centrality(G)). Which node is the biggest "broker"?

betnwess_centrality = nx.betweenness_centrality(G)
"""
Q6: Node 0 (the instructor) and Node 33 (the club president) usually score high here.
If Node 0 were to leave the club, what would happen to the flow of information? After the plot, let's follow up
"""

# %% The network plot
plt.figure(figsize=(10, 8))
# Spring layout spaces out nodes so they are easier to see
pos = nx.spring_layout(G, seed=42)

nx.draw(G, pos, with_labels=True, node_color='lightblue',
        edge_color='gray', node_size=500, font_weight='bold')
plt.title("Zachary's Karate Club Friendship Network")
plt.show()




# %% Removing the leader and observing if the density will improve or decrease, even leaving some nodes behind
# Which nodes are more likely to form a faction, how many members and how good or bad are they connected on their groups?

# To answer that question, what would happen afteer removing the node 0 (mister Hi)
# We need first, to recalculate the number of nodes and edges

# copy the object not interfeering the vars we've created already
administrator_clan = G.copy()

administrator_clan.remove_node(0);
adm_nodes = administrator_clan.number_of_nodes();
adm_edges = administrator_clan.number_of_edges();

"""
Conclusion: the edges went from 78 to 62, a decrease of 20.51%
And the nodes, only one removed.
"""

# %% Observing the new degree
adm_graph_degree = list(administrator_clan.degree);


# %% Collecting the new network density

adm_density = nx.density(administrator_clan);
adm_degree_centrality = nx.degree_centrality(administrator_clan);
adn_betnwess_centrality = nx.betweenness_centrality(administrator_clan);

## › without using the plot, if i rank the degree by the smallest i will find nodes that wil be left behind?
"""
Yes, i've found out before ploting that the degree of 0 to the node 11, mean that he lost connection as soon as his leader is
out of the table
And since we have very close numbers to 12,17 and 21, that doesnt mean that they are connected in the same groups. To find
the groups that were formed, we would need to have greedy_modularity_communities but that's for later
"""

# %% The Administrator network plot
plt.figure(figsize=(10, 8))
# Spring layout spaces out nodes so they are easier to see
pos = nx.spring_layout(G, seed=42)

def get_node_sizes(G, scale=3000):
      """
      Calculates a drawing size for each node based on degree centrality.

      Args:
          G: A NetworkX graph.
          scale: Multiplier that makes size differences visible.

      Returns:
          A list of node sizes in graph node order.
      """
      degree_centrality = nx.degree_centrality(G)

      return [
          degree_centrality[node] * scale
          for node in G.nodes()
      ]


nx.draw(administrator_clan, pos, with_labels=True, node_color='red',
        edge_color='gray', node_size=get_node_sizes(administrator_clan, 5000), font_weight='bold')
plt.title("Zachary's Karate Club NEW Network")
plt.show()
"""
Since we're in a very junior level here, we're observing the graphs. We can see in thee final plot
that 6 4 5 16 and 10 made a group. 11 was left without connection and the rest of the network it's ok now
We have some nodes almost alone and others highly connected
* Q6: Node 0 (the instructor) and Node 33 (the club president) usually score high here. If Node 0 were to leave the club, what would happen to the flow of information?

One would leave, a small group would be created not connected to the administrator.
"""


# %% How to evaluate the shortest paths taken
# There are a couple of functions that we can use and they all serve different purposes
# My question is, what's the average hops taken to get to the shortest path for each node
# That it's actually called a single graph-wide average hops

average_hops = nx.average_shortest_path_length(administrator_clan)
"""
Here i got this error because there are nodes that are not connected (as we previosly identified)
"Shortest path length is undefined if the graph is not connected."
What that means, is that we have multiple disconnected components. To find who are them
"""

# %% Getting the connected components
# IT returns a tuple with the nodes connected
un_connected_components = list(nx.connected_components(administrator_clan))

#  %% Getting to know if the network is connected  at all
adm_is_the_network_connected = nx.is_connected(administrator_clan) # false

# %% Counting how many components are disconnected
how_many_are_disconnected = len(un_connected_components)  # 3 are disconnected

"""
So answering the first  question, what's thee average shortest path taken  in this network  before removing the  lader
"""

# %% The shortest path the leader can  take to get to  the last  node
# Same node → 0 hops.  - A to B. So they  needto count  after the first  edge
leader_to_nodes_hops  =  nx.shortest_path_length(G, 0, 33)

# %% Printing the  shortest path
# node 0 → node 8 → node 33
# That is 2 hops and 3 nodes.

leader_to_nodes_shortest_path = nx.shortest_path(G, source=0, target=33)

# %%  Drawning shit
path = nx.shortest_path(G, source=0, target=33)
path_edges = list(zip(path, path[1:]))

  # Draw the original graph
nx.draw(
      G,
      pos,
      node_color="lightgray",
      edge_color="lightgray",
      node_size=30,
      with_labels=False
  )

  # Highlight shortest-path edges
nx.draw_networkx_edges(
      G,
      pos,
      edgelist=path_edges,
      edge_color="red",
      width=3
  )

  # Highlight shortest-path node
nx.draw_networkx_nodes(
      G,
      pos,
      nodelist=path,
      node_color="yellow",
      edgecolors="red",
      node_size=100
  )

  # Highlight source and target
nx.draw_networkx_nodes(
      G,
      pos,
      nodelist=[0],
      node_color="green",
      node_size=150
  )

nx.draw_networkx_nodes(
      G,
      pos,
      nodelist=[33],
      node_color="blue",
      node_size=150
  )
plt.title("shortest path from leader to the last node")
plt.show()



# %% Network  diamater calculates the longest shortest path
# that does not means the worst  case scenario, thats the longest best scenario  between hops

network_diameter =  nx.diameter(G)
adm_network_diameter = nx.diameter(G)


# %% Efficiency of the network is more tricky
# It first finds every  pair of nodes
# Then,  it find's the shortest distance of  each pair
#  Then  it calculates how  many hops to get to the node and transforrm that info in a formula
#  Then calculate the average  efficiency
# So, as  output, we get kind of  the inverse calculation  because one hop means 100% efficiency, more hops less eficiency
"""
  One precision: 1.0 means maximum efficiency relative to hop distance—a direct connection—not necessarily “100% real-world efficiency.” Also,
  unreachable pairs contribute 0.
"""
global_efficiency = nx.global_efficiency(G)
adm_global_efficiency = nx.global_efficiency(G)


print("End");


# %% Closeness
# Q1. Calculate the closeness centrality of every node. Rank the top 5. Explain what high closeness means in this network.
# Q2. Compare the node with the highest degree to the node with the highest closeness. Are they the same? Explain why or why not.\

"""
Since closeness calculates how near I am to the rest of the nodes, all of them n-1 
It helps to measure how the information flows, a high closness (since is a global score) could easily prevent
you from picking up someone who is not very good at reaching the rest of the network (lowest is the worse here)
And a high closeness, means that i can easily jump with hops between nodes. That means
high influence, information cost to travel is low, well positioned to access the whole group

"""

closeness_centrality = nx.closeness_centrality(G);

ranked = sorted(closeness_centrality.items(), key=lambda pair: pair[1], reverse=True)
# top 5
# The information has the shortest paths on average to all other nodes, they are named 0, 2, 33, 31 and 8
top5Centralities = ranked[:5]

"""
So the comparisson with the graph_degree_global comes up, 33 is the highest degree but it's not the 
closeest averarge guy in the network, and we can check this because 33 on the plot, has a bunch of nodes but 
there are many also far from it. Which could easily mean that the best to get to anybody is stil it's leader
""" 


# %% Clustering Coefficient
# It measures how I am important to my neibhors. 
# closest to one, means not that important, close to zero, mean that they can no longer connect without me
# Answers: how clustered are my neighbords with each other.
# Close to one, very tigh and forming a triangle.
# Close to zero, almost none, they are not connected without me.
# With a high betweness that could mean that I'm the glue of the group.
# Why this alone doesn't mean anything for bridge analyses?

"""
  Conceptual questions

  1. What does a clustering coefficient measure about a node’s neighbors?
  Measure how those neighbors are connected to each other without the node itself
  2. If node A is connected to B and C, what additional edge would make A part of a triangle?
   - A - B - A - C. The aditional edge that would make A part of a triangle, would be B to C.
  3. Why can a node with many neighbors still have a low clustering coefficient?
  Because, the clustering coefficient, measures the neightbors connecting with each other. All though
  I am connected to them (have many neighbors), they could not be connected to each other.
  4. What is the maximum possible clustering coefficient?
  - 1
  5. What does a coefficient of 0 mean?
  - They are not connected at all without me
  6. What does a coefficient of 1 mean for a node?
  - They are all connected and forming a triangle without the node
  
  The reason behind, only clustering coefficient is not enough to find the glue or bridge between groups
  it's because how it's calculated. While betweness measures the shortest paths taken, CC only pay attention
  to the average edges that would exist without me. Sounds like "Is my friends know each other?"
  Betweeness answers: Am I on the shortest path between others?
"""


adm_cluster_coefficient_of_index_4 = nx.clustering(administrator_clan, 5)

"""
So for instance, i've ran the command in a cleary neighborhood. The number 4, was cluster coefficient zero, people around him barely
connected only with in there.

While the number five, got 0.33 not bad but not great (great would be 1), so they also depend on me

the same run for the clan administrator throw out 0.1, less than the number 5, meaning that they 
depend so much on him to connect to themselfs, that he could be a super glue or bridge
but, this needs to be measured by betweness

- Near 1: neighbors form a tight, redundant group.
- Near 0: neighbors are mostly disconnected from one another
"""

adm_cluster_coefficient_of_administrator = nx.clustering(administrator_clan, 33)

# %% Components, Comunities and factions


