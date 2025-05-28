import mglearn
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

xmin, xmax = -2, 2
n_samples = 100

X = np.random.uniform(low=xmin, high=xmax, size=(n_samples, 2))


def classify_point(x, y):
    return int(y > x**3)


y = np.array([classify_point(xi[0], xi[1]) for xi in X])

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

hidden_neurons = [2, 5, 10]
activations = ["identity", "logistic", "tanh", "relu"]
results = []

fig, axes = plt.subplots(len(hidden_neurons), len(activations), figsize=(20, 12))
x_line = np.linspace(xmin, xmax, 200)
y_line = x_line**3

for i, neurons in enumerate(hidden_neurons):
    for j, act in enumerate(activations):
        ax = axes[i, j]

        mlp = MLPClassifier(
            solver="lbfgs",
            max_iter=100000,
            activation=act,
            hidden_layer_sizes=[neurons],
            random_state=0,
        )
        mlp.fit(X_train, y_train)

        X_combined = np.vstack([X_train, X_test])
        y_combined = np.hstack([y_train, y_test])
        y_pred_combined = mlp.predict(X_combined)

        is_wrong = y_combined != y_pred_combined
        errors = np.sum(is_wrong)
        results.append((neurons, act, errors))

        mglearn.plots.plot_2d_separator(mlp, X_combined, fill=True, alpha=0.3, ax=ax)

        for class_value, marker in zip([0, 1], ["o", "^"]):
            idx = y_combined == class_value
            colors = np.array(
                [
                    "green" if wrong else ("C0" if class_value == 0 else "C1")
                    for wrong in is_wrong[idx]
                ]
            )
            ax.scatter(
                X_combined[idx, 0],
                X_combined[idx, 1],
                c=colors,
                marker=marker,
                edgecolor="k",
                s=40,
            )

        ax.plot(x_line, y_line, "k--", label="y = x^3")
        ax.set_title(f"Neurons: {neurons}, Activation: {act}\nErrors: {errors}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_xlim(xmin, xmax)

plt.tight_layout()
plt.show()
