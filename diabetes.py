import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

csv_file = "/home/eduardo/Área de trabalho/Trabalho_Final/diabetes_data.csv"
data = pd.read_csv(csv_file)
correlation_matrix = data.corr()
graph = nx.Graph()

columns = data.columns
for col in columns:
    graph.add_node(col)

for i, col1 in enumerate(columns):
    for j, col2 in enumerate(columns):
        if i < j:
            weight = correlation_matrix.loc[col1, col2]
            if not np.isnan(weight):
                graph.add_edge(col1, col2, weight=abs(weight))

pos = nx.spring_layout(graph, seed=42, k=1.0)

plt.figure(figsize=(14, 12))
edges = graph.edges(data=True)
nx.draw_networkx_edges(
    graph, pos, edgelist=edges,
    width=[d['weight'] * 5 for (_, _, d) in edges],
    alpha=0.5
)
nx.draw_networkx_nodes(graph, pos, node_size=800, node_color="lightblue")
labels = {node: node[:10] + "..." if len(node) > 10 else node for node in graph.nodes()}
nx.draw_networkx_labels(
    graph, pos, labels=labels, font_size=9, font_color="black", verticalalignment="center"
)
plt.axis("off")
plt.title("Grafo de Correlações", fontsize=16)
plt.show()

pos = nx.spring_layout(graph, seed=42, k=1.0)
plt.figure(figsize=(14, 12))
edges = graph.edges(data=True)
regular_edges = [(u, v) for u, v, d in edges]
nx.draw_networkx_edges(
    graph, pos, edgelist=regular_edges,
    width=[d['weight'] * 5 for (_, _, d) in edges],
    alpha=0.5, edge_color="gray"
)
minor_edges = [(u, v) for u, v, d in edges if "Diabetes" in [u, v] and (u == "Age" or v == "Age" or u == "HeartDiseaseorAttack" or v == "HeartDiseaseorAttack")]
nx.draw_networkx_edges(
    graph, pos, edgelist=minor_edges,
    width=[d['weight'] * 8 for (u, v, d) in edges if (u, v) in minor_edges],
    alpha=0.9, edge_color="black"
)
nx.draw_networkx_nodes(graph, pos, node_size=800, node_color="lightblue")
labels = {node: node for node in graph.nodes()}
nx.draw_networkx_labels(
    graph, pos, labels=labels, font_size=10, font_color="black"
)
plt.axis("off")
plt.title("Correlação Menor", fontsize=16)
plt.show()

plt.figure(figsize=(14, 12))
major_edges = [(u, v) for u, v, d in edges if "Diabetes" in [u, v] and (u == "HighBP" or v == "HighBP" or u == "HighChol" or v == "HighChol" or u == "Age" or v == "Age")]
nx.draw_networkx_edges(
    graph, pos, edgelist=major_edges,
    width=[d['weight'] * 8 for (u, v, d) in edges if (u, v) in major_edges],
)
nx.draw_networkx_edges(
    graph, pos, edgelist=regular_edges,
    width=[d['weight'] * 5 for (_, _, d) in edges],
    alpha=0.5, edge_color="gray"
)
nx.draw_networkx_nodes(graph, pos, node_size=800, node_color="lightblue")
labels = {node: node for node in graph.nodes()}
nx.draw_networkx_labels(
    graph, pos, labels=labels, font_size=10, font_color="black"
)
plt.axis("off")
plt.title("Correlação Maior", fontsize=16)
plt.show()

diabetic_data = data[data['Diabetes'] == 1]
age_labels = ["18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80+"]
diabetic_data = diabetic_data.copy()
diabetic_data['AgeGroup'] = diabetic_data['Age'].map(lambda x: age_labels[int(x) - 1] if pd.notnull(x) else 'Unknown')
male_data = diabetic_data[diabetic_data['Sex'] == 1]
female_data = diabetic_data[diabetic_data['Sex'] == 0]
male_counts = male_data['AgeGroup'].value_counts().sort_index()
female_counts = female_data['AgeGroup'].value_counts().sort_index()
all_age_groups = sorted(set(male_counts.index).union(female_counts.index))
male_counts = male_counts.reindex(all_age_groups, fill_value=0)
female_counts = female_counts.reindex(all_age_groups, fill_value=0)
x = range(len(all_age_groups))
width = 0.4
plt.figure(figsize=(12, 6))
plt.bar([pos - width/2 for pos in x], male_counts, width=width, label='Male', alpha=0.7)
plt.bar([pos + width/2 for pos in x], female_counts, width=width, label='Female', alpha=0.7)
plt.xticks(ticks=x, labels=all_age_groups, rotation=45)
plt.xlabel('Age Group')
plt.ylabel('Number of Diabetic Patients')
plt.title('Distribution of Diabetes by Gender and Age Group')
plt.legend()
plt.tight_layout()
plt.show()
