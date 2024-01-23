import numpy as np
import matplotlib.pyplot as plt


class RLS:
    """Implementation from https://github.com/craig-m-k/Recursive-least-squares"""

    def __init__(self, num_vars, lam, delta=1):
        """
        num_vars: number of variables including constant
        lam: forgetting factor, usually very close to 1.
        """
        self.num_vars = num_vars

        # delta controls the initial state.
        self.A = delta * np.matrix(np.identity(self.num_vars))
        self.w = np.matrix(np.zeros(self.num_vars))
        self.w = self.w.reshape(self.w.shape[1], 1)

        # Variables needed for add_obs
        self.lam_inv = lam ** (-1)
        self.sqrt_lam_inv = np.sqrt(self.lam_inv)

        # A priori error
        self.a_priori_error = 0

        # Count of number of observations added
        self.num_obs = 0

    def add_obs(self, x, t):
        """
        Add the observation x with label t.
        x is a column vector as a numpy matrix
        t is a real scalar
        """
        z = self.lam_inv * self.A * x
        alpha = (1 + (x.T @ z).item()) ** (-1)
        self.a_priori_error = t - (self.w.T @ x).item()
        self.w = self.w + (t - alpha * (x.T @ (self.w + t * z)).item()) * z
        self.A -= alpha * z * z.T
        self.num_obs += 1

    def fit(self, X, y):
        """
        Fit a model to X, y.
        X and y are numpy arrays.
        Individual observations in X should have a prepended 1 for the constant coefficient.
        """
        for i, point in enumerate(X):
            x = np.matrix(np.ones((1, 4)))
            x[0, 1:4] = point  # Copy the coordinates of the 3D point to x
            x = np.transpose(x)
            self.add_obs(x, y[i])

    def get_error(self):
        """
        Finds the a priori (instantaneous) error.
        Does not calculate the cumulative effect
        of round-off errors.
        """
        return self.a_priori_error

    def predict(self, x):
        """
        Predict the value of observation x. x should be a numpy matrix (col vector)
        """
        x = x[:, np.newaxis]
        print(f"Shape of self.w: {self.w.shape}, Shape of x: {x.shape}")
        print(self.w.T)
        print(x)

        return float(self.w.T @ x)  # changed * to @ because


def regression_test():
    # Predicting a quadratic function
    test_size = 1000
    # Test function
    f = lambda x: 0.2 * x**2 - 3.8 * x - 5.1
    # Gaussian noise to be added to the quadratic signal
    noise = np.random.randn(test_size)
    # You can play around with other noise (like sinusoidal)
    # noise = [np.sin(2*np.pi*i/13) for i in range(test_size)]
    y = np.array([f(i) for i in range(test_size)])
    noisy_y = y + noise
    lam = 0.98
    LS = RLS(4, lam, 1)  # adjusted to 4 bc 3D plus constanst
    # Not using the RLS.fit function because I want to remember all the predicted values
    pred_x = []
    pred_y = []
    for i in range(test_size):
        x = np.matrix(np.zeros((1, 3)))
        x[0, 0] = 1
        x[0, 1] = i
        x[0, 2] = i**2
        pred_x.append(i)
        pred_y.append((x @ LS.w).item())
        LS.add_obs(x.T, noisy_y[i])

    print("Predicted equation in the form Ax^2 + Bx + C")
    print(f"A = {LS.w[2, 0]} | Real value = 0.2")
    print(f"B = {LS.w[1, 0]} | Real value = -3.8")
    print(f"C = {LS.w[0, 0]} | Real value = -5.1")
    # plot the predicted values against the non-noisy output
    plt.plot(pred_x, y - pred_y)
    plt.title("Error as more points are added")
    plt.show()


if __name__ == "__main__":
    regression_test()
    # To deal with the output being dimensions in R^3, it seems sufficient to
    # deal with each dimension separately
    # (See https://math.stackexchange.com/q/2688132)
