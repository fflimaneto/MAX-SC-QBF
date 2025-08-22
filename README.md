# MAX-QBF Solver via Integer Linear Programming

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3119/)
[![Gurobi 12.0](https://img.shields.io/badge/Gurobi-12.0-orange.svg)](https://www.gurobi.com/)


This project implements an Integer Linear Programming (ILP) solution for the MAX-QBF problem with Set Cover constraints (MAX-SC-QBF).

## Authors

- Mateus Marques Rico
- Francisco Ferreira Lima Neto
- Felipe Araújo de Lima

## How to run the solver
- python3 solve.py
- python3 solve.py instance_path

When an instance path is not passed, all instances within the folder 'data' are solved.

## Problem Description

The MAX-SC-QBF problem involves maximizing an objective function f(x) while optimizing binary variables x, which are determined by selecting subsets that contain these variables.