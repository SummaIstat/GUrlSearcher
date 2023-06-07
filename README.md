# GUrlSearcher readme     

## What is GUrlSearcher and what is it intended to be used for

GUrlSearcher is the successor of UrlSearcher.

In a nutshell, GUrlSearcher is a Python application that:
- takes a list of strings as input
- uses each of these strings as a search string on the Google search engine
- after each search, writes (append mode) in a txt file on disk the URLs of the first 10 search results

I developed and used this program to acquire the list of the top 10 URLs associated with a company name, assuming that if a company whose name I only know has a website, it should appear in the top 10 Google search results.

Once the top 10 URLs for each company name in the list are obtained, the next step is to identify which one is most likely to be the official website for that company.

## How is the project folder made

The GUrlSearcher folder contains the following elements:

1) GUrlSearcher.py => the source code of the program
2) GUrlSearcherAuto.exe => the Windows executable version of the program
3) GUrlSearcherAuto.py => the source code of the executable version of the program (.exe file)
4) requirements.txt => list of the modules and packages required by the project
5) config.cfg => configuration file
6) input.txt => list of ids and corresponding strings to be searched (ids and strings are tab separated)
7) how_to_create_EXE.txt => instructions to generate the .exe version of the program
8) icon.ico => the icon of the program
9) README.md => this file
10) LICENSE => copy of the EUPL v1.2 license


## How to execute the program on your PC by using the terminal


If you have Python 3.X already installed on your PC you just have to apply the following instruction points:

1) create a folder on your filesystem (let's say "myDir")

2) copy the content of the project directory into "myDir"

3) customize the parameters inside the config.cfg file :
        
        If you are behind a proxy simply uncomment and customize the PROXY_HOST and PROXY_PORT parameters by removing the initial # character
        
        Change the value of the path related parameters (eg. FIRMS_FILE,OUTPUT_FILE_FOLDER,LOG_FILE_FOLDER) according with the position of the files and folders on your filesystem.

4) open a terminal and go into the myDir directory

5) if in your Python configuration (or you Python virtual environment) the dependencies required by the project are not installed, type and execute the following command:
		pip install -r requirements.txt

6) type and execute the following command:
        python GUrlSearcher.py config.cfg

7) at the end of execution you should find inside the "myDir" directory:
		- a txt file called seed_[dateTime].txt containing the top 10 urls retrieved for each string in the input.txt file
		- a log file called GUrlSearcher_[dateTime].log
                - a file called .google-cookie (you can delete this)


## How to execute the program on your PC by double click the EXE version


If you are using a Windows based operating system, alternatively to using the terminal commands described in the previous section, you can simply double-click on the GUrlSearcherAuto.exe executable file icon.

In this case, before running the program by double-clicking, you still need to make sure that:
    - the config.cfg file is present in the same folder as the GUrlSearcherAuto.exe file
    - the "proxy" and "path" related parameters configuration in the config.cfg file is correct.


## Licensing

This software is released under the European Union Public License v. 1.2
A copy of the license is included in the project folder.


## Considerations


This program is still a work in progress so be patient if it is not completely fault tolerant; in any case feel free to contact me (donato.summa@istat.it) if you have any questions or comments.
