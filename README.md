# Epidemic Modeling
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

See details of the code [here](https://github.com/OscarWan/Epidemic_Modeling/blob/master/code/awareness.py).

## False Test and Possible Quarantine Strategy

Here is the part where our research went into some wrong places. At first I was inspired by [this paper](https://www.medrxiv.org/content/10.1101/2020.07.06.20147702v1) and applied this model into our owns. There are few importent features for this model.
1. The false test. This article introduces the concept of test sensitivity - the accuracy to get a right result for a positive/negative participant. In our model, we finally decided to use 100% for positive patients and [70%, 80%, 90%] accuracy for negative participants.
2. The quarantine and delay-testing strategy. This was some place where we may have different understanding. According to this article, the quarantine and test procedure goes like this: lets define the delay time as 1 day in convenience. A participant takes the test at day N, then at day N+1 he will get the result whether he is infected or not. If the result is negative, nothing will happen. If the result is positive, then he will be moved into quarantined group Q (with status change) and will get the second test. Finally at N+2 day, the participant will go to recovered group R if the result is again positive, or he will go to his original status if the result is negative.
And my code is basically following this article.

Later in our discussion, we decided to simplify the process (using the same condition above): A participant takes the test at day N, then at day N+1 he will get the result whether he is infected or not. If the result is negative, nothing will happen. If the result is positive, then he will be moved into removed group R. I didn't implement this strategy in my final code.

Related Article [here](https://www.medrxiv.org/content/10.1101/2020.07.06.20147702v1)

## Interconnection Between Different Groups

Related Article [here](https://arxiv.org/pdf/1201.6339.pdf)
