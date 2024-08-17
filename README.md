# Vulnerable blog!

## Vulnerable web app named "Blog" with hidden flags!

As part of the Web and mobile application security course, I created a web application in the form of a blog with many different vulnerabilities. The aim is to understand how attacks on web applications work and how you can exploit vulnerabilities you find to

- extract unsecured user data
- gain access to other users' accounts
- prepare a payload harmful to other users that can be placed on this site

and so on. The topic of the blog is vulnerabilities that can be exploited in web applications. It is worthwhile to familiarize with them, as some of them can be found in this application.


## What is the purpose of all this?
As described above, the application is vulnerable to many different types of attacks. The task is to find these vulnerabilities and expose them.

An additional feature on the blog are hidden flags based on the CTF (Capture-The-Flag) principle. In some places, finding a vulnerability will result in finding a flag (according to the pattern: flag={string}). There are 10 flags.

> [!NOTE] Each flag consists of text and ONLY one number - if it is in a different form, then something else needs to be done to get the correct flag. Each flag contains a number from 0 to 9.(e.g. flag={Hello the4e!})

# Instruction:
1. Make sure you have `Docker` installed on your computer.
2. If not - install it for your operating system: [How to install Docker](https://docs.docker.com/engine/install/)
3. Type the command in the terminal `git clone https://github.com/akralka/CTF_blog`
4. Navigate to the main folder (the one with app.py & Dockerfile files - CTF_blog)
5. The next step is to create a docker container. To do this, use the command: `docker build -t blog_container .`
6. To start the container with the built image, use the following command: `docker run -d -p 5000:5000 blog_container`
7. Application will be available at `http://localhost:5000` or `http://127.0.0.1:5000`
8. Use `docker ps` command to check running containers, then type `docker stop <container_id>` to stop the selected container.
 ### Good luck!! 


###### P.S. All photos were generated with DALL∙E.

