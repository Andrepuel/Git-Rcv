Git-Rcv
=======
Python script to create a simple Git wrapper over SSH.

Each repo has an owner user and a list of users that may read and a list of user that may write. The owner may edit the permission list.

Git-Rcv uses the `authorized_keys` list to control access and authenticate the users. By now, the `authorized_keys` file management must be done manually.

Installing
==========
Put the code somewhere, and edit your `authorized_keys` file. Use the following format for each key:

    command="PATH-TO/git-rcv USERNAME",no-X11-forwarding,no-port-forwarding ssh-rsa BASE64-KEY KEY-IDENTIFIER

Replacing: 

* `PATH-TO` with the path where git-rcv resides.
* `USERNAME` the username (in git-rcv context) for the given key.
* `BASE64-KEY` the rsa public key, encoded in base64.
* `KEY-IDENTIFIER` some tip for what key is it. Normally the user and the name of computer that hold this key.

It is also suggested that you create a new user dedicated only for GIT access and remove passworded access to it.

Usage
=====

* `ssh git_rcv_user@git_rcv_host git-receive-pack repo_dir` Used internally by git to write data to repo.
* `ssh git_rcv_user@git_rcv_host git-upload-pack repo_dir` Used internally by git to read data from repo.
* `ssh git_rcv_user@git_rcv_host git-upload-archive repo_dir` Used internally by git to read data from repo.
* `ssh git_rcv_user@git_rcv_host fork repo_dir forked_repo_dir` Copies the repository at `repo_dir` to `forked_repo_dir`. This is faster (and saves disk space) than creating a `forked_repo_dir` manually and pushing `repo_dir`'s data do the new repo.
* `ssh git_rcv_user@git_rcv_host create-repo repo_dir` Creates a repository with path `repo_dir`.
* `ssh git_rcv_user@git_rcv_host receive-permissions repo_dir` Outputs the list of permissions of repo in `repo_dir`. 
* `ssh git_rcv_user@git_rcv_host upload-permissions repo_dir` Read a new list of persmissions from standard input and write it over `repo_dir`'s permission list.
* `ssh git_rcv_user@git_rcv_host list-repos` List every repo that the actual user has read or write access.

Todo
====

* Improve this document
* Added mechanism to manage the keys
