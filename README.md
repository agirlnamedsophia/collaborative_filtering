# Collaborative Filtering ![Build Status](https://travis-ci.org/akellehe/collaborative_filtering.svg?branch=master)

Get started by installing requirements

```
pip install -r requirements.txt
```

Then install `redis-server`. On ubuntu that's just

```
sudo apt-get install redis-server
```

Fire it up

```
>> redis-server
```

Then launch the test, it'll take a couple hours.

```
python fill.py && time python collaborative_filtering.py
```
