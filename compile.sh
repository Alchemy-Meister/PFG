#!/usr/bin/env bash

makeglossaries PFG-Jesus-Sesma
biber PFG-Jesus-Sesma
xelatex -shell-escape PFG-Jesus-Sesma
