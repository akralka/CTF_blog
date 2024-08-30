# Vulnerable blog!

## Vulnerable web app named "Blog" with hidden flags!

As part of my engineering thesis, I created a vulnerable web application in the form of a blog. This app will be used in the labs of the Web and Mobile Application Security course at my faculty. 
The goal is to show students what attacks can be carried out on vulnerable web applications, i.e. how found security holes can be exploited to:

- extract unsecured user data
- gain access to other users' accounts
- prepare a malicious payload for other users that can be placed on the site

and so on.


## What is the purpose of all this?
As described above, the application is vulnerable to different types of attacks. The task is to find these vulnerabilities and expose them.

An additional feature on the blog are hidden flags based on the CTF (Capture-The-Flag) principle. In some places, finding a vulnerability will result in finding a flag (according to the pattern: flag={string}). There are 10 flags in total.

> [!NOTE] Each flag consists of text and ONLY one number (between 0-9) - if it is in a different form, then something else needs to be done to get the correct flag. (e.g. flag={Hello the4e!})

# Instruction 1:
1. Make sure you have `Docker` installed on your computer.
2. If not - install it for your operating system: [How to install Docker](https://docs.docker.com/engine/install/)
3. Type the command in the terminal `git clone https://github.com/akralka/CTF_blog`
4. Navigate to the main folder (the one with app.py & Dockerfile files)
5. The next step is to create a docker image. To do this, use the command: `docker build -t blog .`
6. To start the container with the built image, use the following command: `docker run -d -p 5000:5000 blog`
7. Application will be available at `http://localhost:5000` or `http://127.0.0.1:5000`
8. You may use `docker ps` command to check the status of containers and its ID.
9. Type `docker stop <container_id>` to stop the selected container.
10. If you run the container without the `-d` flag, just use CTRL+C in the terminal to terminate it.


# Instruction 2:
1. Make sure you have `Docker` installed on your computer.
2. If not - install it for your operating system: [How to install Docker](https://docs.docker.com/engine/install/)
3. Use ` docker pull <username>/<docker_image>:<tag>` command.
   e.g. `docker pull adriella/ctf_blog:amd64`
4. To start the container with the built image, use the following command: `docker run -d -p 5000:5000 adriella/ctf_blog:amd64`
5. Application will be available at `http://localhost:5000` or `http://127.0.0.1:5000`
6. You may use `docker ps` command to check the status of containers and its ID.
7. Type `docker stop <container_id>` to stop the selected container.
8. If you run the container without the `-d` flag, just use CTRL+C in the terminal to terminate it.


> [!TIP] I recommend using tools such as: <br>

- `exiftool`, `burpsuite`
- [JWT](https://jwt.io/), [cyberchef](https://cyberchef.org/), [payloads](https://github.com/swisskyrepo/PayloadsAllTheThings)

 ### Good luck!! 

###### P.S. All photos were generated with DALL∙E.
