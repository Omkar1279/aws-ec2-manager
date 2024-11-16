# EC2 Manager

A FastAPI-based application to manage AWS EC2 instances. The application allows users to create, list, retrieve, start, stop, and terminate EC2 instances.

---

## Features

- Create EC2 instances with custom configurations.
- Retrieve information about a specific EC2 instance.
- List all EC2 instances with optional filtering.
- Start, stop, and terminate EC2 instances.
- Retrieve instance status summary.

---

## Prerequisites

Before setting up the application, ensure you have the following:

- **Python 3.8+** installed on your machine.
- AWS credentials configured (e.g., in `~/.aws/credentials` or environment variables).
- An AWS account with permissions to manage EC2 instances.
- **pip** for installing Python dependencies.

---

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Omkar1279/aws-ec2-manager.git
   cd ec2_manager
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the root directory and add your AWS credentials:
   ```
   AWS_ACCESS_KEY_ID=<your-access-key>
   AWS_SECRET_ACCESS_KEY=<your-secret-key>
   AWS_REGION=<your-region>
   ```

5. **Run the Application**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the API**
   Open your browser or use a tool like Postman to access the API at:
   ```
   http://127.0.0.1:8000/docs
   ```

---

## API Documentation

The application provides the following API endpoints:

### **Base URL**
All endpoints are prefixed with `/api/v1/instances`.

### **Endpoints**

1. **Create a New EC2 Instance**
   - **URL:** `POST /`
   - **Description:** Creates a new EC2 instance with the specified parameters.
   - **Request Body:**
     ```json
     {
       "name": "my-instance",
       "instance_type": "t2.micro",
       "ami_id": "ami-12345678",
       "key_pair_name": "my-key-pair",
       "security_group_id": "sg-12345678",
       "environment": "production"
     }
     ```
   - **Response:** The details of the created EC2 instance.

2. **List All EC2 Instances**
   - **URL:** `GET /`
   - **Description:** Retrieves all EC2 instances with optional filters.
   - **Query Parameters:**
     - `environment` (optional): Filter by environment.
     - `instance_type` (optional): Filter by instance type.
   - **Response:** A list of EC2 instances.

3. **Get Details of a Specific EC2 Instance**
   - **URL:** `GET /{instance_id}`
   - **Description:** Retrieves details of a specific EC2 instance.
   - **Response:** Details of the requested EC2 instance.

4. **Start an EC2 Instance**
   - **URL:** `POST /{instance_id}/start`
   - **Description:** Starts a stopped EC2 instance.
   - **Response:** The started EC2 instance.

5. **Stop an EC2 Instance**
   - **URL:** `POST /{instance_id}/stop`
   - **Description:** Stops a running EC2 instance.
   - **Response:** The stopped EC2 instance.

6. **Terminate an EC2 Instance**
   - **URL:** `DELETE /{instance_id}`
   - **Description:** Terminates an EC2 instance.
   - **Response:** The terminated EC2 instance.

7. **Get Instance Status Summary**
   - **URL:** `GET /status/summary`
   - **Description:** Retrieves a summary of statuses across all instances.
   - **Response:**
     ```json
     {
       "total_instances": 5,
       "status_breakdown": {
         "running": 3,
         "stopped": 2
       },
       "timestamp": "2024-11-17T12:00:00Z"
     }
     ```

8. **Update Instance Tags** (Not Implemented)
   - **URL:** `POST /{instance_id}/tags`
   - **Description:** Updates tags for a specific instance.
   - **Response:** `501 Not Implemented`
