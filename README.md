# Collaborative Filtering ![Build Status](https://travis-ci.org/akellehe/collaborative_filtering.svg?branch=master)

# Getting Started

When you clone this project it should be in /opt/collaborative\_filtering.

After that, assuming you have vagrant/virtualbox installed you should just be able to do 

```
vagrant up
```

Vagrant will use the `ansible` scripts in `/deploy` to provision your virtual machine with the appropriate dependencies, then it will launch the web application under `daemontools` in the `/service` directory.

You can `ssh` to your virtual machine with 

```
vagrant ssh
```

from the `/opt/collaborative_filtering` directory on your physical machine.

After you log in, launch the test, it'll take a couple hours.

```
/collaborative_filtering/local/venv/collaborative_filtering/bin/activate;
cd /opt/collaborative_filtering;
python fill.py && time python collaborative_filtering.py
```

After that; to run the unit tests:

```
nosetests tests.py
```

Then go to `http://localhost:8080` in your browser. 
