import pandas as pd
import matplotlib.pyplot as plt
import scipy as scy
import numpy as np


# test function for X_real
def funcX_real(data, a, b, c, d, e):

    #data input will be [A_pix,Y_pix, R_pix]
    X_pix = data[0]
    Y_pix = data[1]
    R_pix = data[2]

    return a*np.arctan(d*np.divide(np.subtract(X_pix,951),R_pix)) + b*np.arctan(e*np.divide(np.subtract(X_pix,951),Y_pix)) + c

# test function for Y_real
def funcY_real(data, a, b, c, d):

    #data input will be [A_pix,Y_pix, R_pix]
    X_pix = data[0]
    Y_pix = data[1]
    R_pix = data[2]

    return a*np.arctan(b*np.divide(Y_pix+d,R_pix)) + c


def funcZ_real(data, a, b, c):
    #data input will be [A_pix,Y_pix, R_pix]
    X_pix = data[0]
    Y_pix = data[1]
    R_pix = data[2]

    return a*np.divide(b,R_pix) + c

def avg_error(real_data, fit_data):

    # Parameters:
    # real_data: [X_real,Y_real,Z_real]
    # fit_data: [X_fit,Y_fit,Z_fit]

    error = np.sum(np.abs(np.subtract(real_data,fit_data))) / len(real_data[0])
    return error


df = pd.read_csv("./depth_data.csv")
X_pix = df['X_pix'].tolist()
Y_pix = df['Y_pix'].tolist()
R_pix = df['R_pix'].tolist()
X_real = df['X_real'].tolist()
Y_real = df['Y_real'].tolist()
Z_real = df['Z_real'].tolist()



Xparameter_guess = [0.4,3.87,-0.02]
Yparameter_guess = [250,0]

parameters_X, covariance_X = scy.optimize.curve_fit(funcX_real, [X_pix, Y_pix, R_pix], X_real)
parameters_Y, covariance_Y = scy.optimize.curve_fit(funcY_real,[X_pix, Y_pix, R_pix], Y_real)
parameters_Z, covariance_Z = scy.optimize.curve_fit(funcZ_real,[X_pix, Y_pix, R_pix], Z_real)

X_fit = funcX_real([X_pix, Y_pix, R_pix], parameters_X[0], parameters_X[1], parameters_X[2],parameters_X[3], parameters_X[4])
Y_fit = funcY_real([X_pix, Y_pix, R_pix], parameters_Y[0], parameters_Y[1], parameters_Y[2], parameters_Y[3])
Z_fit = funcZ_real([X_pix, Y_pix, R_pix], parameters_Z[0], parameters_Z[1], parameters_Z[2])


# Include fits into dataframe
df['X_fit'] = X_fit
df.assign(X_fit=X_fit)

df['Y_fit'] = Y_fit
df.assign(Y_fit=Y_fit)

df['Z_fit'] = Z_fit
df.assign(Z_fit=Z_fit)


# Create new dataframes to plot y levels in pixel space
new_df_y5 = df[(df.Y_real == 5)]
new_df_y4 = df[(df.Y_real == 4)]
new_df_y3 = df[(df.Y_real == 3)]
new_df_y2 = df[(df.Y_real == 2)]
new_df_y1 = df[(df.Y_real == 1)]
new_df_y0 = df[(df.Y_real == 0)]

# Create new dataframes to plot Z levels in the pixel space
new_df_z5 = df[(df.Z_real == 5)]
new_df_z6 = df[(df.Z_real == 6)]
new_df_z7 = df[(df.Z_real == 7)]
new_df_z8 = df[(df.Z_real == 8)]
new_df_z9 = df[(df.Z_real == 9)]
new_df_z10 = df[(df.Z_real == 10)]
new_df_z11 = df[(df.Z_real == 11)]
new_df_z12 = df[(df.Z_real == 12)]

# Create new dataframes for X levels
new_df_x0 = df[(df.X_real == -2)]
new_df_x1 = df[(df.X_real == -1)]
new_df_x2 = df[(df.X_real == 0)]
new_df_x3 = df[(df.X_real == 1)]
new_df_x4 = df[(df.X_real == 2)]

# Calculate error in predictions
X_error = avg_error([X_real], [X_fit])
Y_error = avg_error([Y_real], [Y_fit])
Z_error = avg_error([Z_real], [Z_fit])

XYZ_error = np.sqrt(X_error**2 + Y_error**2 + Z_error**2)

# print dat shit
print("X parameters:")
print(parameters_X)
print("Average Error in X:")
print(X_error)
print("\n")

print("Y parameters:")
print(parameters_Y)
print("Average Error in Y:")
print(Y_error)
print("\n")

print("Z parameters:")
print(parameters_Z)
print("Average Error in Z:")
print(Z_error)
print("\n")

print("Average Error in XYZ:")
print(XYZ_error)
print("\n")

# Figure to display pixel space
fig1 = plt.figure(1)
ax = plt.axes(projection='3d')
ax.scatter(X_pix, Y_pix, R_pix, c='green')
plt.xlabel("X_pix")
plt.ylabel("Y_pix")
plt.title("Pixel Space")

plt.close()

# Figure to display X_fit to X_real
fig2 = plt.figure(2)
ax = plt.axes(projection='3d')
ax.scatter(X_real, Y_pix, R_pix, c='green')
ax.scatter(X_fit, Y_pix, R_pix, c='red' )
plt.xlabel("X_real (feet)")
plt.ylabel("Y_pix")
plt.title("X_fit compared to X_real")

plt.close()

# Figure to display Y_fit to Y_real
fig3 = plt.figure(3)
ax = plt.axes(projection='3d')
ax.scatter(X_pix, Y_real, R_pix, c='green')
ax.scatter(X_pix, Y_fit, R_pix, c='red' )
plt.xlabel("X_pix")
plt.ylabel("Y_real (feet)")
plt.title("Y_fit compared to Y_real")

plt.close()

# Figure to display Z_fit to Z_real
fig4 = plt.figure(4)
ax = plt.axes(projection='3d')
ax.scatter(X_pix, Y_pix, Z_real, c='green')
ax.scatter(X_pix, Y_pix, Z_fit, c='red' )
plt.xlabel("X_pix")
plt.ylabel("Y_pix")
plt.title("Z_fit compared to Z_real")

plt.close()

# Figure to display X_real layers in the pixel space
fig5 = plt.figure(5)
ax = plt.axes(projection='3d')
ax.scatter(new_df_x0['X_pix'].tolist(), new_df_x0['Y_pix'].tolist(), new_df_x0['R_pix'].tolist(), c='blue')
ax.scatter(new_df_x1['X_pix'].tolist(), new_df_x1['Y_pix'].tolist(), new_df_x1['R_pix'].tolist(), c='green')
ax.scatter(new_df_x2['X_pix'].tolist(), new_df_x2['Y_pix'].tolist(), new_df_x2['R_pix'].tolist(), c='orange')
ax.scatter(new_df_x3['X_pix'].tolist(), new_df_x3['Y_pix'].tolist(), new_df_x3['R_pix'].tolist(), c='black')
ax.scatter(new_df_x4['X_pix'].tolist(), new_df_x4['Y_pix'].tolist(), new_df_x4['R_pix'].tolist(), c='yellow')
plt.xlabel("X_pix")
plt.ylabel("Y_pix")
plt.title("Pixel Space w X layers")

plt.close()

# Figure to display Y_real layers in the pixel space
fig6 = plt.figure(6)
ax = plt.axes(projection='3d')
ax.scatter(new_df_y5['X_pix'].tolist(), new_df_y5['Y_pix'].tolist(), new_df_y5['R_pix'].tolist(), c='green')
ax.scatter(new_df_y4['X_pix'].tolist(), new_df_y4['Y_pix'].tolist(), new_df_y4['R_pix'].tolist(), c='red')
ax.scatter(new_df_y3['X_pix'].tolist(), new_df_y3['Y_pix'].tolist(), new_df_y3['R_pix'].tolist(), c='blue')
ax.scatter(new_df_y2['X_pix'].tolist(), new_df_y2['Y_pix'].tolist(), new_df_y2['R_pix'].tolist(), c='yellow')
ax.scatter(new_df_y1['X_pix'].tolist(), new_df_y1['Y_pix'].tolist(), new_df_y1['R_pix'].tolist(), c='orange')
ax.scatter(new_df_y0['X_pix'].tolist(), new_df_y0['Y_pix'].tolist(), new_df_y0['R_pix'].tolist(), c='purple')
plt.xlabel("X_pix")
plt.ylabel("Y_pix")
plt.title("Pixel Space w Y layers")

plt.close()

# Figure to display Z_real layers in the pixel space
fig7 = plt.figure(7)
ax = plt.axes(projection='3d')
ax.scatter(new_df_z5['X_pix'].tolist(), new_df_z5['Y_pix'].tolist(), new_df_z5['R_pix'].tolist(), c='green')
ax.scatter(new_df_z6['X_pix'].tolist(), new_df_z6['Y_pix'].tolist(), new_df_z6['R_pix'].tolist(), c='red')
ax.scatter(new_df_z7['X_pix'].tolist(), new_df_z7['Y_pix'].tolist(), new_df_z7['R_pix'].tolist(), c='blue')
ax.scatter(new_df_z8['X_pix'].tolist(), new_df_z8['Y_pix'].tolist(), new_df_z8['R_pix'].tolist(), c='yellow')
ax.scatter(new_df_z9['X_pix'].tolist(), new_df_z9['Y_pix'].tolist(), new_df_z9['R_pix'].tolist(), c='orange')
ax.scatter(new_df_z10['X_pix'].tolist(), new_df_z10['Y_pix'].tolist(), new_df_z10['R_pix'].tolist(), c='purple')
ax.scatter(new_df_z11['X_pix'].tolist(), new_df_z11['Y_pix'].tolist(), new_df_z11['R_pix'].tolist(), c='black')
ax.scatter(new_df_z12['X_pix'].tolist(), new_df_z12['Y_pix'].tolist(), new_df_z12['R_pix'].tolist(), c='cyan')

plt.xlabel("X_pix")
plt.ylabel("Y_pix")
plt.title("Pixel Space w Z layers")

plt.close()

# Figure to display fit vs real
fig8 = plt.figure(8)
ax = plt.axes(projection='3d')
ax.scatter(X_real, Y_real, Z_real, c='green')
ax.scatter(X_fit, Y_fit, Z_fit, c='red')

plt.xlabel("X_real (feet)")
plt.ylabel("Y_real (feet)")
plt.title("Real space vs Fit space")

# Figure to dive into Y values
fig9 = plt.figure(9)

plt.scatter(new_df_x0['Y_real'], new_df_x0['Y_fit'], c='blue')
plt.scatter(new_df_x1['Y_real'], new_df_x1['Y_fit'], c='green')
plt.scatter(new_df_x2['Y_real'], new_df_x2['Y_fit'], c='orange')
plt.scatter(new_df_x3['Y_real'], new_df_x3['Y_fit'], c='black')
plt.scatter(new_df_x4['Y_real'], new_df_x4['Y_fit'], c='yellow')

plt.xlabel("Y_real (feet)")
plt.ylabel("Y_fit (feet)")
plt.title("Y_real vs Y_fit")

plt.close()

fig10 = plt.figure(10)
plt.scatter(new_df_y0['Z_real'], new_df_y0['Z_fit'], c='blue')
plt.scatter(new_df_y1['Z_real'], new_df_y1['Z_fit'], c='green')
plt.scatter(new_df_y2['Z_real'], new_df_y2['Z_fit'], c='orange')
plt.scatter(new_df_y3['Z_real'], new_df_y3['Z_fit'], c='black')
plt.scatter(new_df_y4['Z_real'], new_df_y4['Z_fit'], c='yellow')
plt.scatter(new_df_y5['Z_real'], new_df_y5['Z_fit'], c='cyan')

plt.xlabel("Z_real (feet)")
plt.ylabel("Z_fit (feet)")
plt.title("Z_real vs Z_fit")

plt.close()

plt.show()

