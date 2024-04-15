from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD

# Define the structure of the Bayesian network
model = BayesianNetwork([('A', 'C'), ('B', 'C')])

# Define Conditional Probability Distributions (CPDs)
cpd_a = TabularCPD(variable='A', variable_card=2, values=[[0.6], [0.4]])
cpd_b = TabularCPD(variable='B', variable_card=2, values=[[0.7], [0.3]])
cpd_c = TabularCPD(variable='C', variable_card=2, values=[[0.9, 0.8, 0.7, 0.1], [0.1, 0.2, 0.3, 0.9]],
                   evidence=['A', 'B'], evidence_card=[2, 2])

# Add CPDs to the model
model.add_cpds(cpd_a, cpd_b, cpd_c)

# Check if the model is correctly defined
print("Model is valid:", model.check_model())

# Print CPDs
print("CPD A:")
print(cpd_a)
print("CPD B:")
print(cpd_b)
print("CPD C:")
print(cpd_c)
