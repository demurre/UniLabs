import matplotlib.pyplot as plt

results = [
    (2, "identity", 5),
    (2, "logistic", 5),
    (2, "tanh", 5),
    (2, "relu", 4),
    (5, "identity", 5),
    (5, "logistic", 0),
    (5, "tanh", 0),
    (5, "relu", 5),
    (10, "identity", 5),
    (10, "logistic", 0),
    (10, "tanh", 0),
    (10, "relu", 0),
]

activations = ["identity", "logistic", "tanh", "relu"]
data_by_activation = {act: [] for act in activations}
neuron_counts = sorted(set(r[0] for r in results))

for act in activations:
    for neurons in neuron_counts:
        for n, a, e in results:
            if n == neurons and a == act:
                data_by_activation[act].append(e)

plt.figure(figsize=(10, 6))
for act in activations:
    plt.plot(neuron_counts, data_by_activation[act], marker="o", label=f"{act}")

plt.title("Number of false classifications vs. number of neurons")
plt.xlabel("Number of neurons in the hidden layer")
plt.ylabel("Number of false classifications")
plt.xticks(neuron_counts)
plt.grid(True)
plt.legend(title="Activation function")
plt.tight_layout()
plt.show()
