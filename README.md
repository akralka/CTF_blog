# Vulnerable blog!

## Vulnerable web app named "Blog" with hidden flags!

As part of my engineering thesis, I created a web application in the form of a blog with many vulnerabilities that will be used in the labs of the Web and Mobile Application Security course at my faculty. 
The goal is to show students what attacks can be carried out on vulnerable web applications, i.e. how found security holes can be exploited to:

- extract unsecured user data
- gain access to other users' accounts
- prepare a malicious payload for other users that can be placed on this site

and so on.


## What is the purpose of all this?
As described above, the application is vulnerable to different types of attacks. The task is to find these vulnerabilities and expose them.

An additional feature on the blog are hidden flags based on the CTF (Capture-The-Flag) principle. In some places, finding a vulnerability will result in finding a flag (according to the pattern: flag={string}). There are 10 flags in total.

> [!NOTE] Each flag consists of text and ONLY one number - if it is in a different form, then something else needs to be done to get the correct flag. Each flag contains a number from 0 to 9.(e.g. flag={Hello the4e!})

# Instruction:
1. Make sure you have `Docker` installed on your computer.
2. If not - install it for your operating system: [How to install Docker](https://docs.docker.com/engine/install/)
3. Type the command in the terminal `git clone https://github.com/akralka/CTF_blog`
4. Navigate to the main folder (the one with app.py & Dockerfile files - CTF_blog)
5. The next step is to create a docker container. To do this, use the command: `docker build -t blog_container .`
6. To start the container with the built image, use the following command: `docker run -d -p 5000:5000 blog_container`
7. Application will be available at `http://localhost:5000` or `http://127.0.0.1:5000`
8. You may use `docker ps` command to check the status of containers.
9. Type `docker stop <container_id>` to stop the selected container (use `docker images` to check its ID).
10. If you run the container without the `-d` flag, just use CTRL+C in the terminal to terminate it.

> [!TIP] I build my image on wsl Ubuntu 22.04. Here's my pre-build image you may use: <br> 
<!-- - [Download blog_container.tar](link dysk google here) -->
- Sha256 for `.tar` file: 
- Sha256 for _docker image_:

After downloading the file, use the following commands to run the container:
- `docker load -i blog_container.tar` 
- `docker run -p 5000:5000 blog_container`

> [!TIP] I recommend using tools such as: <br>

- `exiftool`, `burpsuite`
- [JWT](https://jwt.io/), [cyberchef](https://cyberchef.org/), [payloads](https://github.com/swisskyrepo/PayloadsAllTheThings)

 ### Good luck!! 

###### P.S. All photos were generated with DALL∙E.
