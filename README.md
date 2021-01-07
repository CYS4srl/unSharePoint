# unSharePoint
A tool created to ease SharePoint security assessments.
Currently supported for Python v. >= 3.x.

To run the project, first clone the repo:

```
git clone https://github.com/CYS4srl/unSharePoint.git
```

Then, install dependencies:

```
pip install -r requirements.txt
```

Now you are all set, run unsharepoint.py to start the tool.

## Usage


```
unsharepoint.py -h
```
shows a basic list of options and flag to use the tool.

```
unsharepoint.py -t i --url TARGETURL
unsharepoint.py --url TARGETURL
```
runs an informative scan.


```
unsharepoint.py -t a --url TARGETURL
```
runs an api scan.


```
unsharepoint.py -t ad --url TARGETURL
```
runs a detailed api scan.


```
unsharepoint.py -t ad -u USERNAME -p PASSWORD --url TARGETURL
```
runs a detailed api scan providing username and password to access the target.


```
unsharepoint.py --bruteforce --username-file USERSFILE --password-file PASSFILE --url TARGETURL
```
runs a bruteforce on usernames and password reading each line from USERFILE and PASSFILE files respectively.


