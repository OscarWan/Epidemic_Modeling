# Epidemic_Modeling
This project aims to simulate COVID-19 with a relative small range by designing a kitchensink model. Our group constructs a stochastic SIR model with scale-free network. Several customized parameters are designed to realize different function.

## Exploration of Newman's Theory
Newman's Spread of epidemic disease on networks
$$\\T_{c} = \frac{<k>}{<k^{2}>-<k>}$$\
$$\\<k> = \sum k p_{k} \text{, where } p_{k} = \frac{2m(m+1)}{k(k+1)(k+2)}$$
$$T = 1- \int_{0}^{\inf} dr \sum_{\tau} P(r)P(\tau)(1-r)^{\tau}$$
$$T = 1-(1-\beta)^{\gamma} \text{ where }  \beta = 0.5, \gamma = 5 \text{ in our simulation}$$
