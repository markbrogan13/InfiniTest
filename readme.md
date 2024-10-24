# InfiniTest Application

## Purpose

Creating a testing tool that will allow SEs and Testing team to run tests trough the InfiniBand suite, collect logs, and analyze the results. Hopefully looking to get throughput and error detection.

### Objectives

1. Python-based tool that automates testing
2. IB Network Detection and Validation
3. Performance Testing
4. Error Detection
    - packet errors
    - link recovery events
    - alerts if error hits thresholds
5. Logging and Report Generation
6. (Optional) Dashboard integration for nice UI

### Tech Stack

- Python
- Libraries:
  - `subprocess` for running commands
  - `psutil` resource monitoring
  - `matplotlib` or `Plotly` for generating performance graphs
  - `Flask` or `Django` for a web-based dashboard

### Main Milestones

1. Setup IB network detection and link validation
2. Basic throughput and latency benchmarking
3. Implement error counting and monitoring + logging
4. Build reports
