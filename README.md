# Epidemic_Modeling
This project aims to simulate COVID-19 with a relative small range by designing a kitchensink model. Our group constructs a stochastic SIR model with scale-free network. Several customized parameters are designed to realize different function.

## Exploration of Newman's Theory
Newman's Spread of epidemic disease on networks

![](https://latex.codecogs.com/png.latex?T_{c}&space;=&space;\frac{<k>}{<k^{2}>-<k>})

![](https://latex.codecogs.com/png.latex?<k>&space;=&space;\sum&space;k&space;p_{k}&space;\text{,&space;where&space;}&space;p_{k}&space;=&space;\frac{2m(m&plus;1)}{k(k&plus;1)(k&plus;2)})

![](https://latex.codecogs.com/png.latex?T&space;=&space;1-&space;\int_{0}^{\inf}&space;dr&space;\sum_{\tau}&space;P(r)P(\tau)(1-r)^{\tau})

![](https://latex.codecogs.com/png.latex?T&space;=&space;1-(1-\beta)^{\gamma}&space;\text{&space;where&space;}&space;\beta&space;=&space;0.5,&space;\gamma&space;=&space;5&space;\text{&space;in&space;our&space;simulation})

See details in the notebook [here](https://github.com/OscarWan/Epidemic_Modeling/blob/master/code/BA%20Percolation.ipynb).

Related paper is posted [here](https://journals.aps.org/pre/pdf/10.1103/PhysRevE.66.016128).

## Exploration of Awareness

We use scale-free networks of N nodes with degree k distributed according to P(k), where P(k) is the fraction of nodes with connectivity k.

Awareness is a factor ![](https://latex.codecogs.com/png.latex?\rho\in(0,1)). The result of the multiplication between it and the infectious rate ![](https://latex.codecogs.com/png.latex?b) are considered to be final infectious rate for the particular node.

We can get awareness by ![](https://latex.codecogs.com/png.latex?\rho(t)=\sum_k&space;P(k)\rho_k(t)) with discrete time step, where ![](https://latex.codecogs.com/png.latex?\rho_k(t))is the relative density; i.e. the probability that a node with k links is infected.

Related papers are posted [here](https://aip.scitation.org/doi/10.1063/1.3673573) and [here](https://journals.aps.org/prl/pdf/10.1103/PhysRevLett.86.3200).

See details of the code here.
