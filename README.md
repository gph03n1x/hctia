HCTIA
=====

hctia is a small application for mass addition or deletion of a ssh key.
Adding or deleting manually an ssh key on multiple internal virtual machines, can be quite the pain. 
This script makes easier to add/remove entries such as these:
```shell
ssh-rsa rsa/yaba/daba/dou= email@example.com
```

at the `.ssh/authorized_keys` file of each VM. The application is listing the available hosts from the users personal ssh config located at `~/.ssh/config`.

Using the application
---------------------

First of all you need to create python 3.9.6 virtual environment. I am using pyenv and venv for this job.

```shell
pyenv install 3.9.6  # if you don't have said version
pyenv local 3.9.6
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

You can start the application using the provided bash script:

```shell
./run.sh
```

The script will open the web-ui in your browser