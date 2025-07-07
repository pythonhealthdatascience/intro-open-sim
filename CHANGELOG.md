# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Dates formatted as YYYY-MM-DD as per [ISO standard](https://www.iso.org/iso-8601-date-and-time-format.html).

## Unreleased

## Added

* `07a_exercise.ipynb`and `07a_solutions.ipynb`: simple exercises to complement learning in `07_experiments.ipynb`
* `10_multiple_arrival_processes.ipynb`: simulating multiple arrivals classes each with their own distribution
* `11_blocking.ipynb`: simulating the blocking of one resource while queuing for another.
* `12_arrival_classes.ipynb`: simulate unique processes for different classes of arrival to the model.
* `distributions.py`: module containing some distributions to reduce code in notebooks.
* `basic_model.py`: contains a single activity version of the call centre model to use with `07_exercise.ipynb`

## [v0.2.0 - 11/02/2024](https://github.com/pythonhealthdatascience/intro-open-sim/releases/tag/v0.2.0) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14849934.svg)](https://doi.org/10.5281/zenodo.14849934)

Simulation workshop 2025 release. Additional notebooks to respond to reviewers requests.

## Added

* `06a_basic_results_exercise.ipynb`: An exercise to practice collecting results from a `simpy` model.
* `06b_basic_results_solutions.ipynb`: Solutions to exercise.
* `07_experiments.ipynb`: our approach to setting up a model for multiple replications, experimentation, and common random numbers
* `08_full_model.ipynb`: an extended version of the 111 call centre process. We also introduce a warm-up period
* `09_time_weighted_calcs.ipynb`: An alternative approach to collects results for queue length and resource utilisation.

## Changed

* Upgraded to JupyterLite v0.5.x and xeus-python kernel v3.x
* Modified SW25 paper.

## [v0.1.0 - 22/10/2024](https://github.com/pythonhealthdatascience/intro-open-sim/releases/tag/v0.1.0) - [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13971859.svg)](https://doi.org/10.5281/zenodo.13971859)

🌱 Initial release of tutorial materials.

### Added

* Six notebooks introducing sampling, basic simpy concepts and basic results collection procedures.