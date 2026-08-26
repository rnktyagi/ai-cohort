import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

embeddings = np.load("embeddings.npy")

sections = []

with open("knowledge_base.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        sections.append(json.loads(line)["section"])

points = PCA(n_components=2).fit_transform(embeddings)

for section in set(sections):
    x = [points[i, 0] for i in range(len(points)) if sections[i] == section]
    y = [points[i, 1] for i in range(len(points)) if sections[i] == section]

    plt.scatter(x, y, label=section)

plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.legend()

plt.savefig("embeddings_2d.png")
plt.show()