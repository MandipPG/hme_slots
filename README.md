# Slot Finder

### Requirements
Python 3.5+, pip3

### Usage

1.  Move to ```<project-dir>```, create virtual environment and then activate it as


```sh
$ cd <project-dir>
$ virtualenv -p python3 .env
$ source .env/bin/activate
```

2. Add project to ```PYTHONPATH``` as 

```sh 
$ export PYTHONPATH="$PYTHONPATH:." # . corresponds to current directory(project-dir)
```

3. Then run test cases as  

```sh
$ python -m unittest discover -s 'tests' -p '*.py'
```

4. Then run the application ```run.py``` as  
 
```sh
$ python run.py 
```
Note: Input parameters can be changed under `run.py` file.