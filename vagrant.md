# **Vagrant with Docker**
#### **YOU SHOULD NOT NEED TO EDIT THE VagrantFile**

This guide will walk you through setting up your local development environment using **Vagrant** with **Docker** as the provider.

We are using **Vagrant** to standardize our local development environment. Instead of installing dependencies directly on your machine, Vagrant will spin up a **Docker container** for your development work. This ensures that everyone has a consistent environment regardless of their operating system (Windows, macOS, or Linux).

---

## **Prerequisites**

Before you begin, please ensure you have the following installed:

### 1. **Docker**
   - Download and install **Docker Desktop** for your platform:
     - [Docker for Windows](https://www.docker.com/products/docker-desktop)
     - [Docker for macOS](https://www.docker.com/products/docker-desktop)
     - Linux: Install via your package manager (e.g., `apt`, `yum`, etc.).
   - Verify that Docker is installed:
     ```bash
     docker --version
     ```
     You should see the Docker version output.

   - Ensure that your project directory is **file-shared** (for Windows/macOS users):
     - Open **Docker Desktop > Settings > Resources > File Sharing**.
     - Add your project directory (e.g., `C:\Users\<username>\project` or `/Users/<username>/project`).

### 2. **Vagrant**
   - Download and install **Vagrant**:
     - [Vagrant for all platforms](https://developer.hashicorp.com/vagrant/downloads).
   - Verify that Vagrant is installed:
     ```bash
     vagrant --version
     ```
     You should see the Vagrant version output.

### 3. **Vagrant Docker Plugin**
   - Vagrant supports Docker natively, but you can ensure compatibility with:
     ```bash
     vagrant plugin install vagrant-docker-compose
     ```

---

## **Vagrant Commands Explained**

Below are the most commonly used Vagrant commands during development:

### 1. **Start the Development Environment:**
   ```bash
   vagrant up --provider=docker
   ```
   - Spins up the Docker container.
   - This command checks for any changes in the `Vagrantfile` and applies them if necessary.

### 2. **SSH into the Container:**
   ```bash
   vagrant ssh
   ```
   - Opens an interactive shell session inside the Docker container.
   - Useful for running commands directly inside the container (e.g., `poetry install`, `uvicorn`).

### 3. **Stop the Development Environment:**
   ```bash
   vagrant halt
   ```
   - Stops the running Docker container without destroying it.
   - Run this when you’re done working for the day.

### 4. **Restart the Container and Reprovision:**
   ```bash
   vagrant reload --provision
   ```
   - Restarts the container and applies any changes made to the `Vagrantfile` or provisioning scripts.
   - Use this when you update environment configurations or dependencies.

### 5. **Destroy the Container:**
   ```bash
   vagrant destroy -f
   ```
   - Destroys the Docker container entirely.
   - Use this to reset the environment or reclaim disk space.

### 6. **Check Container Status:**
   ```bash
   vagrant status
   ```
   - Displays the current status of the Vagrant-managed container.

---

## **Accessing the API**

After running:
```bash
poetry run uvicorn cc_simple_server.server:app --reload --host 0.0.0.0 --port 8000
```
The API will be available at:
```
http://localhost:8000
```

---

## **Common Issues and Solutions**

### **1. Docker File Sharing Issues (Windows/macOS)**
   - If you see errors related to file mounts or missing files, ensure the project directory is shared in Docker Desktop settings.

### **2. Permission Issues Inside the Container**
   - If you encounter `Permission denied` errors:
     ```bash
     sudo chmod -R u+rwx /home/vagrant/app
     ```

### **3. FastAPI Not Reloading**
   - If changes to your code don’t reflect:
     - Check if the Uvicorn process is running with the `--reload` flag.
     - Run:
       ```bash
       poetry run uvicorn cc_simple_server.server:app --reload --host 0.0.0.0 --port 8000
       ```

---

## **Why Are We Using Vagrant with Docker?**

- **Consistency:** All students have the same development environment, regardless of operating system.
- **No Local Dependency Conflicts:** Your local Python/Docker setup remains clean.
- **Ease of Use:** With just a few commands (`vagrant up`, `vagrant ssh`, etc.), you can quickly get started without worrying about complex configurations.

By using Vagrant with Docker, we abstract away environment setup complexities while giving you the flexibility to focus on development.

---
