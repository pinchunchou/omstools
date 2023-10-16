# Trigger rates and counts from OMS

## Install
```
git clone git@github.com:pinchunchou/omstools.git
cd omstools/
```
* Add requirements
    - On private computer
    ```
    pip3 install -r requirements.txt # private pc
    ```
    - On lxplus8
    ```
    git clone ssh://git@gitlab.cern.ch:7999/cmsoms/oms-api-client.git
    cd oms-api-client
    python3 setup.py install --user
    python3.8 setup.py bdist_rpm --python /usr/bin/python3.8 --build-requires python38,python38-setuptools --release 0.el8
    ```

* Add secret info (ask me) in `env.py`
```
CLIENT_ID = 'example_id'
CLIENT_SECRET = 'example_secret'
```

## Usage

### `autoratecheck.py`
* Automatically check the L1 and HLT trigger rates and save to a csv file.

### `numevtcheck.py`
* Automatically check the number of events passing the HLT trigger and save to a csv file.
