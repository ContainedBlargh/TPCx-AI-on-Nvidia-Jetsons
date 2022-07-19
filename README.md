# TPCx-AI-on-Nvidia-Jetsons
This repository contains only instructions for adjustments required to replicate our paper "TPCx-AI on NVIDIA Jetsons"

The copyright of the original TPCx-AI benchmark belongs to the [Transaction Processing Performance Council (TPC)](https://www.tpc.org/)

## Overview


[In workload/python/workload/UseCase05.py:](./workload/python/workload/UseCase05.py) we've made a simple bugfix in Use Case 5 where we pass an argument that was omitted in the original code.

[In workload/python/workload/UseCase08.py:](./workload/python/workload/UseCase08.py) we've parallelized Use Case 8 to take advantage of concurrent processing.
