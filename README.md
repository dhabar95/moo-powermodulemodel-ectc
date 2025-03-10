# Optimizing Power Package Reliability: Mitigating Thermal Expansion Failures Using Active Learning

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
[![PyAnsys](https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC)](https://docs.pyansys.com/)
[![Python](https://img.shields.io/pypi/pyversions/ansys-dpf-core?logo=pypi)](https://pypi.org/project/ansys-dpf-core/)
[![pypi](https://img.shields.io/pypi/v/ansys-dpf-core.svg?logo=python&logoColor=white)](https://pypi.org/project/ansys-dpf-core)

## Authors

- [Dharshan Barkur](https://github.com/dhabar95) - PhD Student (Robert Bosch GmbH, Kusterdingen - Technische Universität Dresden)
- [Akshay Vivek Panchwagh](https://github.com/) - PhD Student (Robert Bosch GmbH - Technische Universität Chemnitz)

## Overview
### About the repository
This repository contains the codebase for the multi-objective optimization (MOO) of a Power Module, leveraging pyMAPDL, pyDPF, and Ax (by Facebook). The project is developed as part of the ECTC Student Competition 2025, focusing on simulation-driven optimization for enhanced performance and reliability.

### Motivation for this project
Power electronic packages—such as discrete packages, power modules, and ASICs—are composed of heterogeneous materials like copper, epoxy polymers, and SAC solder. Each of these materials exhibits unique thermo-mechanical behavior due to their intrinsic material properties. Among these, the Coefficient of Thermal Expansion (CTE) plays a critical role. When subjected to temperature fluctuations, the mismatch in CTEs among different materials leads to thermo-mechanical stresses, ultimately causing structural reliability issues and premature failure.
To tackle this challenge, this project proposes a novel simulation-driven design methodology that integrates high-fidelity finite element modeling (FEM) via pyMAPDL scripting with Bayesian Optimization using Gaussian Processes (BO-GP) through Facebook's Ax platform. By adaptively exploring the design space and accounting for uncertainties, this approach enables efficient identification of failure-prone configurations and optimization of both material selection and package geometry. The result is a robust, computationally efficient framework that enhances the reliability and performance of power packages under complex thermal loading conditions.
