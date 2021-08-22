# ConLAR
A resource allocation engine for Docker containers.

## Introduction
ConLAR applies a learning-to-allocate approach that predicts and allocates resources to Docker containers under time-varying workloads. It efficiently reduces over-provisioning cost with the SLO guarantees by taking an Observing-Predicting-Allocating-Executing paradigm: given a container, it observes the running of the online application and its environment, leverages the LSTM (long short term memory) model to predict its future workload, adaptively learns to construct resource allocation strategies with two objectives through RL (reinforcement learning), and executes them to scale container resources dynamically.

The following figure presents an overview of ConLAR, which contains four main components:

(1)**Observation Component** monitors the resource utilization and limits of Docker containers in real time, by interrogating directly with Linux cgroup subsystems.

(2)**Workload Prediction Component** employs ML models to predict the future workload of the application dynamically. It analyzes the workload for the previous few cycles provided by the observation component, and outputs the predicted workload for the next cycle. 

(3)**Resource Allocation Component** adaptively generates resource scaling strategies using reinforcement learning technique, where the reward function is measured by SLO violation rate and resource provisioning cost. 

(4)**Execution Component** executes the resource scaling strategies by modifying the container cgroup file system to update the resource quota during runtime.


![image](https://user-images.githubusercontent.com/45347405/130312984-113908f3-f946-434f-91c9-0faa04d6f669.png)

## Dataset
