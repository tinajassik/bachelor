# Stage 1: Build the Angular application
# Use a Node.js version that's compatible with your Angular project
FROM node:18-alpine as builder
# 'alpine' variants are smaller

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
# This leverages Docker's cache. If these files don't change,
# Docker won't re-run npm install unnecessarily.
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application source code
COPY . .

# Build the application for production
# The output path 'dist/your-project-name' might need adjustment
# based on your angular.json 'outputPath' setting.
# Common default is 'dist/your-angular-project-name' or just 'dist/app'
RUN npm run build --prod
# If your build output goes to a specific subfolder like 'dist/my-app',
# you might need: RUN npm run build -- --output-path=./dist/my-app

# Stage 2: Serve the built application with Nginx
FROM nginx:1.25-alpine
# Using a specific version of nginx-alpine

# Remove default Nginx welcome page
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom Nginx configuration (we'll create this file next)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the built application from the 'builder' stage to Nginx's web root
# IMPORTANT: Adjust 'dist/your-project-name' below to match the
# actual output directory of your 'npm run build --prod' command.
# Check your angular.json or the output of the build command.
# For example, if your build output is in 'dist/frontend', use that.
COPY --from=builder /app/dist/frontend /usr/share/nginx/html
# If your build output is just in 'dist' (e.g., 'dist/index.html'), it might be:
# COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80 (Nginx default port)
EXPOSE 80

# Nginx will be started by the base image's default CMD
