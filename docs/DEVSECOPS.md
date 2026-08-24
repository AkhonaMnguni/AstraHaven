# DevSecOps

CI should install from the pinned requirements, run pytest with coverage, lint and type-check the application, scan dependencies and the Docker image, then publish only reviewed artifacts. Runtime secrets belong in the platform secret store, not in the repository.
