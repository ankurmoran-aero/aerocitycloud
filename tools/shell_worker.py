import docker
import os
import shutil
import configuration as config

client = docker.from_env()

def create_dockerfile(directory):
    # Detect if it's a Node.js or Python project
    has_package_json = os.path.exists(os.path.join(directory, 'package.json'))
    
    dockerfile_content = f"""
FROM python:3.10-slim

# Install common system dependencies + Node.js
RUN apt-get update && apt-get install -y --no-install-recommends \\
    git \\
    curl \\
    ffmpeg \\
    gcc \\
    python3-dev \\
    build-essential \\
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \\
    && apt-get install -y nodejs \\
    && npm install -g tsx typescript \\
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN groupadd -r aerocity && useradd -r -g aerocity aerocity
WORKDIR /app
COPY . .
RUN chown -R aerocity:aerocity /app

# Install dependencies based on project type
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi
RUN if [ -f package.json ]; then npm install; fi

RUN chmod +x start.sh
USER aerocity
CMD ["./start.sh"]
"""
    with open(os.path.join(directory, 'Dockerfile'), 'w') as f:
        f.write(dockerfile_content)

STORAGE_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'storage'))

def deploy_project(user_id, directory, codebase_id, port=None, internal_port=8000):
    # 1. Prepare persistent storage
    user_storage = os.path.join(STORAGE_BASE, str(user_id), codebase_id)
    os.makedirs(user_storage, exist_ok=True)
    
    # 2. Copy files to persistent storage
    for item in os.listdir(directory):
        s = os.path.join(directory, item)
        d = os.path.join(user_storage, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

    create_dockerfile(user_storage)
    
    image_tag = f"aerocity_{user_id}_{codebase_id}".lower()
    container_name = f"aerocity_cont_{user_id}_{codebase_id}".lower()
    
    try:
        # Build Image using the storage directory
        print(f"Building image {image_tag}...")
        image, build_logs = client.images.build(path=user_storage, tag=image_tag, rm=True)
        
        # Prune old dangling images to save disk space
        try:
            client.images.prune(filters={'dangling': True})
        except Exception:
            pass
        
        # Remove existing container if any
        try:
            old_container = client.containers.get(container_name)
            old_container.stop()
            old_container.remove()
        except docker.errors.NotFound:
            pass
            
        # Run Container
        print(f"Starting container {container_name} with port mapping...")
        
        # Setup port mapping if provided
        try:
            int_port_val = int(internal_port) if internal_port else 8000
        except ValueError:
            int_port_val = 8000
            
        ports_config = { f'{int_port_val}/tcp': port } if port else None
        
        container = client.containers.run(
            image_tag,
            detach=True,
            name=container_name,
            mem_limit=f"{config.FREE_TIER_RAM}m",
            ports=ports_config,
            environment={"PORT": str(int_port_val)},
            restart_policy={"Name": "always"}
        )
        
        return True, container.id
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False, str(e)

def stop_container(container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        return True
    except docker.errors.NotFound:
        return True 
    except Exception:
        return False

def start_container(container_id):
    try:
        container = client.containers.get(container_id)
        container.start()
        return True
    except Exception:
        return False

def remove_container_physical(container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        container.remove()
        return True
    except docker.errors.NotFound:
        return True
    except Exception:
        return False

def rebuild_container(user_id, codebase_id, port=None, internal_port=8000):
    user_storage = os.path.join(STORAGE_BASE, str(user_id), codebase_id)
    if not os.path.exists(user_storage):
        return False, "Project storage not found"
        
    create_dockerfile(user_storage)
    
    image_tag = f"aerocity_{user_id}_{codebase_id}".lower()
    container_name = f"aerocity_cont_{user_id}_{codebase_id}".lower()
    
    try:
        print(f"Rebuilding image {image_tag}...")
        try:
            client.images.build(path=user_storage, tag=image_tag, rm=True)
        except docker.errors.BuildError as be:
            log_error = ""
            for line in be.build_log:
                if 'stream' in line:
                    log_error += line['stream']
            return False, f"Build Error:\n{log_error}"
        
        try:
            old_container = client.containers.get(container_name)
            old_container.stop()
            old_container.remove()
        except docker.errors.NotFound:
            pass
            
        print(f"Starting container {container_name} with port {port}...")
        
        # Setup port mapping if provided
        try:
            int_port_val = int(internal_port) if internal_port else 8000
        except ValueError:
            int_port_val = 8000
            
        ports_config = { f'{int_port_val}/tcp': port } if port else None
        
        try:
            container = client.containers.run(
                image_tag,
                detach=True,
                name=container_name,
                mem_limit=f"{config.FREE_TIER_RAM}m",
                ports=ports_config,
                environment={"PORT": str(int_port_val)},
                restart_policy={"Name": "always"}
            )
        except Exception as ce:
            return False, f"Runtime Error: {str(ce)}"
 
        return True, container.id
    except Exception as e:
        return False, str(e)

