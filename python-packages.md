---
layout: page
title: Python Packages
sidebar_link: true
sidebar_sort_order: 4
---

The various python packages that I have developed are listed below.

## BDRL (Birth Death Record Linkage)
Provides a python implementation of estimators for recovering unobserved duration distributions using data that is subject to record linkage error. 
Refer to my paper, ["Birth, Death, and Record Linkage: Survival Analysis in the Presence of Record Linkage Error,"](research.html) for an in depth description of the model and estimators.

## Monte Carlo Simulator
Provides generic methods to implement Monte Carlo simulations in python.
The user simply provides a function that generates a data set and a function that computes a set of statistics of interest and the methods will perform the simulations.
Auxiliary methods, such as for stability analysis or computing multiple MC simulations across a range of parameter values, are also provided.

## ArDa (Article Database)
This python application organizes research articles and the meta data associated with them to help streamline the use of literature in your current research projects.
It allows the user to download meta data, group articles into projects (or reading lists), produce bib files, and create notes that are article/project specific.
