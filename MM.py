import random as rd
import gurobipy as gp
import numpy as np
from scipy.stats import binom
N = 8 #products
M = 5 #parts
S = 2
N_b = 10
p = 0.5
ps = 0.5

m = gp.Model("Multiproduct Assembly")
#m.setParam('OutputFlag', 0)  #pls don't add this

z = m.addVars(S, N, lb=0, ub=gp.GRB.INFINITY, vtype=gp.GRB.INTEGER, name = "ProductsProduced") #number of unit produced
y = m.addVars(S, M, lb=0, ub=gp.GRB.INFINITY, vtype=gp.GRB.INTEGER, name = "PartsScrapped") #number of unit left in inventory
x = m.addVars(M, lb=0, ub=gp.GRB.INFINITY, vtype=gp.GRB.INTEGER, name = "PartsPreOrdered") #number of unit ordered

l = [rd.randint(1, 100) for _ in range(N)]
q = [rd.randint(1000, 100000) for i in range(N)]
s = [rd.randint(1, 100) for _ in range(M)]
b = [rd.randint(s[i], 100) for i in range(M)]
A = [[rd.randint(1, 10) for _ in range(M)]for _ in range(N)]

d = np.array([np.random.binomial(N_b, p, size=N) for _ in range(S)])
d = d.tolist()

d_p = []
binomial_dist = binom(N_b, p)
for values in d:
    binomial_dist = binom(N_b, p)
    pmf_values = [binomial_dist.pmf(value) for value in values]
    d_p.append(pmf_values)


ConstrY = m.addConstrs((
    y[k, j] == x[j] - gp.quicksum(A[i][j] * z[k, i] for i in range(N)) for j in range(M) for k in range(S)
), name = "Constraint.y")

ConstrZ = m.addConstrs((
    z[k, i] <= d[k][i] for i in range(N) for k in range(S)
), name = "Constraint.z")


m.setObjective(
    gp.quicksum(b[j] * x[j] for j in range(M))
    + ps * (gp.quicksum((gp.quicksum(d_p[k][i] * (l[i] - q[i]) * z[k, i] for i in range(N)) - gp.quicksum(s[j] * y[k, j] for j in range(M))) for k in range(S)))
, sense = gp.GRB.MINIMIZE)

m.update()
m.optimize()
print(f"objective val = {m.ObjVal}")
for v in m.getVars():
    print(f"{v.VarName} = {v.X}")

###############################################################################################################################################################################################
#This One is for testing and learning
# m = Model()
# x1 = m.addVar(lb = 0, ub = GRB.INFINITY, obj = 20, vtype = GRB.CONTINUOUS, name = "food.1")
# x2 = m.addVar(obj = 10, name = "food.2")
# x3 = m.addVar(obj = 31, name = "food.3")
# x4 = m.addVar(obj = 11, name = "food.4")
# x5 = m.addVar(obj = 12, name = "food.5")
# con1 = m.addConstr(2*x1+0*x2+3*x3+1*x4+2*x5>=21, "nutrient.1")
# con2 = m.addConstr(0*x1+1*x2+2*x3+2*x4+2*x5>=12, "nutrient.2")
# m.update()
# m.optimize()

# m = Model()
# x1 = m.addVar(lb = 0, ub = GRB.INFINITY, obj = 30, vtype = GRB.INTEGER)
# x2 = m.addVar(obj = 12)
# x3 = m.addVar(obj = 25)
# con1 = m.addConstr(9*x1+3*x2+5*x3<=500)
# con2 = m.addConstr(5*x1+4*x2<=350)
# con3 = m.addConstr(3*x1+2*x3<=150)
# con4 = m.addConstr(x3<=20)
# m.setObjective(30*x1+12*x2+25*x3, GRB.MAXIMIZE)
# m.update()
# m.optimize()
# #TestcodeEnd

# l = producing cost for each product
# q = selling cost for each product
# s = scrapping cost for each part
# b = preorder cost for each part

# a = amount of parts for each product
# d = demand for l q s a

# x y z = PartsPreOrdered PartsScrapped ProductsProduced
# #               MAIN                           (Second stage)

# import random as rd
# N=8
# M=5

# m = Model()

# z = m.addVars(N, lb=0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name = "ProductsProduced1")
# y = m.addVars(M, lb=0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name = "PartsScrapped")
# x = m.addVars(M, lb=0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name = "PartsPreOrdered")


# l = [rd.randint(1, 100) for _ in range(N)] #gia sx product
# q = [rd.randint(1, 100) for _ in range(N)] #gia ban product
# s = [rd.randint(1, 100) for _ in range(M)] #gia ban part
# b = [rd.randint(1, 100) for _ in range(M)] #gia preorder part
# a = [[rd.randint(1, 100) for _ in range(M)]for _ in range(N)] #ma tran
# d = [rd.randint(1, 100) for _ in range(N)] #phat sinh (Can phai sx them mot luong product nua moi du chi tieu)

# x = [rd.randint(1, 100) for _ in range(M)]

# Con21 = m.addConstrs((y[j] == x[j] - quicksum(a[i][j] * z[i] for i in range(N)) for j in range(M)), name = "Constraint.2.1")


# Con22 = m.addConstrs((0<=z[i] for i in range(N)), name = "Constraint.2.2")

# Con23 = m.addConstrs((d[i]>=z[i] for i in range(N)), name = "Constraint.2.3")

# Con24 = m.addConstrs((y[j]>=0 for j in range(M)), name = "Constraint.2.4")

# m.setObjective((quicksum((l[i] - q[i]) * z[i] for i in range(N)) - quicksum(s[j] * y[j] for j in range(M))), sense=GRB.MINIMIZE)
# m.update()
# m.optimize()

# import gurobipy as gp
# import random as rd
# import numpy as np
# N=8
# M=5
# S=2
# N_b=10
# p=0.5
# m = gp.Model()

# z = m.addVars(S, N, lb=0, ub=gp.GRB.INFINITY, vtype=gp.GRB.CONTINUOUS, name = "ProductsProduced1")
# y = m.addVars(S, M, lb=0, ub=gp.GRB.INFINITY, vtype=gp.GRB.CONTINUOUS, name = "PartsScrapped")
# #x = m.addVars(M, lb=0, ub=gp.GRB.INFINITY, vtype=gp.GRB.CONTINUOUS, name = "PartsPreOrdered")


# l = [rd.randint(1, 100) for _ in range(N)] #gia sx product
# q = [rd.randint(1, 100) for _ in range(N)] #gia ban product
# s = [rd.randint(1, 100) for _ in range(M)] #gia ban part
# #b = [rd.randint(1, 100) for _ in range(M)] #gia preorder part
# a = [[rd.randint(1, 100) for _ in range(M)]for _ in range(N)] #ma tran
# # d = [rd.randint(1, 100) for _ in range(N)] #phat sinh (Can phai sx them mot luong product nua moi du chi tieu)
# d = np.array([np.random.binomial(N_b, p, size=N) for _ in range(S)])
# x = [rd.randint(1, 100) for _ in range(M)]

# Con21 = m.addConstrs((y[k, j] == x[j] - gp.quicksum(a[i][j] * z[k, i] for i in range(N)) for j in range(M) for k in range(S)), name = "Constraint.2.1")


# # Con22 = m.addConstrs((0<=z[k, i] for i in range(N) for k in range(2)), name = "Constraint.2.2")

# Con23 = m.addConstrs((z[k,i]<=d[k][i] for i in range(N) for k in range(S)), name = "Constraint.2.3")

# # Con24 = m.addConstrs((y[k, j]>=0 for j in range(M) for k in range(2)), name = "Constraint.2.4")

# m.setObjective(gp.quicksum((gp.quicksum((l[i] - q[i]) * z[k, i] for i in range(N))) - (gp.quicksum(s[j] * y[k, j] for j in range(M))) for k in range(2)), sense=gp.GRB.MINIMIZE)

# m.update()
# m.optimize()
# for v in m.getVars():
#     print(f"{v.VarName} = {v.X}")

# #############################                  Result                      #############################
# Gurobi Optimizer version 10.0.3 build v10.0.3rc0 (win64)

# CPU model: 11th Gen Intel(R) Core(TM) i7-1165G7 @ 2.80GHz, instruction set [SSE2|AVX|AVX2|AVX512]
# Thread count: 4 physical cores, 8 logical processors, using up to 8 threads

# Optimize a model with 26 rows, 13 columns and 66 nonzeros
# Model fingerprint: 0x7cffd4e9
# Coefficient statistics:
#   Matrix range     [1e+00, 1e+02]
#   Objective range  [8e+00, 1e+02]
#   Bounds range     [0e+00, 0e+00]
#   RHS range        [2e+01, 9e+01]
# Presolve removed 26 rows and 13 columns
# Presolve time: 0.01s
# Presolve: All rows and columns removed
# Iteration    Objective       Primal Inf.    Dual Inf.      Time
#        0   -1.8004000e+04   0.000000e+00   0.000000e+00      0s

# Solved in 0 iterations and 0.01 seconds (0.00 work units)
# Optimal objective -1.800400000e+04


# #############################Result#############################




# #May cai nay la thong so cua bai tren. Thay l q s a d x trong phan code phia tren de co the ra duoc cai ket qua nay. l q s a d x dung randint nen ket qua se khac moi khi khoi tao cai moi
# l = [12, 87, 57, 81, 60, 86, 82, 51]
# q = [45, 5, 69, 42, 82, 78, 6, 2]
# s = [49, 65, 49, 19, 99]
# a = [[11, 55, 94, 70, 52], [57, 24, 41, 68, 62], [97, 86, 5, 14, 26], [32, 92, 10, 18, 12], [93, 1, 1, 7, 44], [43, 87, 52, 33, 69], [58, 1, 83, 32, 33], [14, 100, 36, 68, 24]]
# d = 75
# x = [23, 40, 81, 84, 88] #<----- Subjected to change



# Day 1: 6 units
# Day 2: 4 units
# Day 3: 5 units
# Day 4: 8 units
# Day 5: 3 units
# Day 6: 5 units
# Day 7: 7 units
# Day 8: 6 units
# Day 9: 5 units
# Day 10: 4 units









# #binomial generate function
# #For Stage one
# #Will need to be applied


# hon


# python