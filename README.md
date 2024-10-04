[![lite-badge](https://jupyterlite.rtfd.io/en/latest/_static/badge.svg)](https://pythonhealthdatascience.github.io/intro-open-sim/lab/index.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![ORCID: Alison Harper](https://img.shields.io/badge/ORCID:_Alison_Harper-0000--0001--5274--5037-brightgreen)](https://orcid.org/0000-0001-5274-5037)
[![ORCID: Tom Monks](https://img.shields.io/badge/ORCID:_Tom_Monks-0000--0003--2631--4481-brightgreen)](https://orcid.org/0000-0003-2631-4481)
[![ORCID: Amy Heather](https://img.shields.io/badge/ORCID:_Amy_Heather-0000--0002--6596--3479-brightgreen)](https://orcid.org/0000-0002-6596-3479)

#  An introduction to Discrete-Event Simulation (DES) using Free and Open Source Software

> Work in progress.  This is a STARS project being prepared for the [Operational Research Society 12th Simulation Workshop in 2025 (SW25)](https://www.theorsociety.com/ORS/ORS/Events/2025/Simulation-Workshop/SW25.aspx). It has been adapted from our [template repository](https://github.com/pythonhealthdatascience/stars-simpy-jupterlite) for sharing `simpy` models with JupyterLite.

## 🧑‍💻 1. Tutorial

We being with two notebooks that introduce some basic concepts for creating DES in python:

* `01_sampling.ipynb`: Sampling from statistical distributions using `numpy`
* `02_basic_simpy.ipynb`: Creating simple `simpy` DES models that make use of `numpy` sampling

Your understanding of these is then tested in:

* `03a_exercise1.ipynb`: Exercise to testing understanding of the basics of `simpy` and `numpy`
* `03b_exercise1_solutions.ipynb`: Example solutions for the exercise

We then move on to some more advanced concepts, and create a full process model:

* `04_111_model.ipynb`: Full `simpy` process model, creating a model for a 111 call centre 
* `05_basic_results.ipynb`: Collecting results from a single run by storing process metrics during a run and performing calculations at the end

## 🔧 2. Set-up

To run the notebooks in this tutorial, you can either run via your browser or locally...

### 2.1 Running notebooks within your browser

This tutorial has been set up to run on your browser without the need to install any components. This is achieved using Web Assembly technology i.e. [JupterLite](https://github.com/jupyterlite/jupyterlite) and [xeus-python](https://github.com/jupyter-xeus/xeus-python). A model notebook is downloaded to your local machine and all dependencies are pre-installed via conda-forge. The model then lives in the browsers cache. You can make changes to the model or create new files and these are persisted (until the browser cache is cleared).

> ✨ **To access this tutorial in your browser:** <https://pythonhealthdatascience.github.io/intro-open-sim/>.

### 2.2 Running notebooks locally on your machine

You can also run the notebooks in `content/` locally on your machine. You'll need to install the provided conda environment `environment.yml`.

```
conda env create --name xeus-python-kernel --file environment.yml
conda activate xeus-python-kernel
```

## 📝 3. Citation

TBC.

## 🤝 4. Acknowledgements

<!--TODO: Is this just relevant to the template repository, or likewise to this one?-->

We would like to thank the [JupterLite](https://github.com/jupyterlite/jupyterlite) and [xeus-python](https://github.com/jupyter-xeus/xeus-python) developers for making this work possible. This discrete-event simulation focussed tutorial was based on the learning materials and template provided by [Jupyterlite xeus-python demo](https://github.com/jupyterlite/xeus-python-demo) and [tutorial given at PyData 2023](https://www.youtube.com/watch?v=WXRslU9D3bo) by Jeremy Tuloup.

## 💰 5. Funding

STARS is supported by the Medical Research Council [grant number [MR/Z503915/1](https://gtr.ukri.org/projects?ref=MR%2FZ503915%2F1)].