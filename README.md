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

To run the unit tests:

```
nosetests tests.py
```

# Running the web application

It's a basic tornado app at the moment, running on your physical machine with no virtualization. You can run the web app like

```
>> python app.py
```
Then go to `http://localhost:8080` in your browser. 