TimeSide_benchmark
==================

Benchmark suite for TimeSide


Based on *Airspeed Velocity*: A simple Python benchmarking tool with web-based reporting (see http://spacetelescope.github.io/asv )

Benchmark results for TimeSide can be viewed here: http://parisson.github.io/TimeSide_benchmark/

Install and run
----------------

```
sudo apt-get install python-psutil python-numpy python-pip
sudo pip install conda
sudo conda init
sudo conda update -q conda
git clone https://github.com/spacetelescope/asv.git
cd asv
sudo python setup.py install
cd ..
git clone https://github.com/Parisson/TimeSide_benchmark.git
cd TimeSide_benchmark
asv machine
asv run
asv publish
asv preview  #  to preview the results in a local static webserver
asv gh-pages  # to push the results in this repository gh-pages
```
