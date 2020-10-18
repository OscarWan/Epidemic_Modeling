# Epidemic_Modeling
This project aims to simulate COVID-19 with a relative small range by designing a kitchensink model. Our group constructs a stochastic SIR model with scale-free network. Several customized parameters are designed to realize different function.

## Exploration of Newman's Theory
Newman's Spread of epidemic disease on networks

![](https://latex.codecogs.com/png.latex?T_{c}&space;=&space;\frac{<k>}{<k^{2}>-<k>})

![](https://latex.codecogs.com/png.latex?<k>&space;=&space;\sum&space;k&space;p_{k}&space;\text{,&space;where&space;}&space;p_{k}&space;=&space;\frac{2m(m&plus;1)}{k(k&plus;1)(k&plus;2)})

![](https://latex.codecogs.com/png.latex?T&space;=&space;1-&space;\int_{0}^{\inf}&space;dr&space;\sum_{\tau}&space;P(r)P(\tau)(1-r)^{\tau})

![](https://latex.codecogs.com/png.latex?T&space;=&space;1-(1-\beta)^{\gamma}&space;\text{&space;where&space;}&space;\beta&space;=&space;0.5,&space;\gamma&space;=&space;5&space;\text{&space;in&space;our&space;simulation})

See details in the notebook [here](https://github.com/OscarWan/Epidemic_Modeling/blob/master/code/BA%20Percolation.ipynb).
