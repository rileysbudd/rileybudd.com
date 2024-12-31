FROM nginx:latest

# Copy custom configuration file to the container (optional)
# COPY nginx.conf ./etc/nginx/nginx.conf

# Copy website content to the default NGINX root directory
COPY ./html ./usr/share/nginx/html

# Expose port 80 for HTTP
EXPOSE 8080

# Command to start NGINX (default in the base image)
CMD ["nginx", "-g", "daemon off;"]
