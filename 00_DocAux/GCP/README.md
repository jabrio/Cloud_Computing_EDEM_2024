# Cloud computing fundamentals

## 1. Compute Engine

Compute Engine is a service that provides virtual machines that run on Google infrastructure. Compute Engine offers scale, performance, and value that allows you to easily launch large compute clusters on Google's infrastructure. There are no upfront investments and you can run thousands of virtual CPUs on a system that has been designed to be fast, and to offer strong consistency of performance.

To create and manage your virtual machines, you can use Google Cloud CLI or the web UI. In this exercise, you will use first the web UI and then the CLI.

### Create a Compute Engine instance

1. In the GCP Console, go to the VM Instances page.
   
   <img src=".images/vm_intro_1.png">

2. Activate the Compute Engine API if it is not already activated.
   
   <img src=".images/vm_intro_2.png">

3. Click Create instance.
   
    <img src=".images/vm_intro_3.png">

4. Select the region as europe-southwest1 (Madrid) and the zone as europe-southwest1-a.
   
    <img src=".images/vm_intro_4.png">

5. In the type of machine, select the machine type as e2-micro.
   
    <img src=".images/vm_intro_5.png">

5. In the Firwall section, select Allow HTTP traffic and Allow HTTPS traffic. And in the advanced section, add the tag `ejercicio-1` to the network tags.
   
    <img src=".images/vm_intro_6.png">


6. Leave the rest of the options as default and click Create.


Once the instance is created, we have to connect to it. We have several options:

- **SSH from the browser**: This option is only available for Linux instances. It is not available for Windows instances. It is the easiest way to connect to the instance, but it is not available for Windows instances.

- **SSH from the command line**: This option is available for both Linux and Windows instances. It is the most flexible option, but it requires to install the Cloud SDK in your local machine.


## 2. Create a Bucket in GCS

### Introduction to GCS

Cloud Storage is a service for storing your objects in Google Cloud. An object is an immutable piece of data consisting of a file of any format. You can think of an object as a file, but it is not limited to just files. An object consists of the following:

- The object itself
- Metadata
- A unique identifier
- A bucket that contains the object
- A name that you assign to the object
- A set of access control permissions
- A set of object lifecycle management rules

There are different types of storage depending on how fast you want to access the data and how much you want to pay for it. The most common types are:

- **Standard**: This is the default storage class. It is designed for frequently accessed data. It is the most expensive option.
- **Nearline**: This storage class is designed for data that is accessed less than once a month. It is cheaper than the standard storage class, but it has a retrieval fee.
- **Coldline**: This storage class is designed for data that is accessed less than once a year. It is cheaper than the nearline storage class, but it has a retrieval fee.
  


1. In the GCP Console, go to the Storage > Browser page.
   
   <img src=".images/gcs_1.png">

2. Click Create bucket.
    
    <img src=".images/gcs_2.png">

3. In the Create bucket dialog, specify the following attributes:
    - A unique bucket name.
    - A default storage class. For this tutorial, choose Standard.
    - A default location.
    - A default project. This tutorial uses My First Project.
    - Click Create.

    <img src=".images/gcs_3.png">

4. Allow for all public access to the bucket.
   
    <img src=".images/gcs_4.png">

5. Go inside the bucket and upload the file inside `01_Code/01_Fundamentals/GCP/02_GCS/data/employee_data.csv`.
   
    <img src=".images/gcs_5.png">


## 3. Create a PostgreSQL instance in Cloud SQL

1. In the GCP Console, go to the SQL page.
   
   <img src=".images/db_1.png">

2. Click on create instance with free credits.
    
    <img src=".images/db_2.png">

3. Select PostgreSQL as the database engine.
   
    <img src=".images/db_3.png">

4. Select the following options:
    - Instance ID: `ejercicio-3`
    - Root password: `EDEM2024-SQL`
    - Region: europe-west1 (Belgium)
    - Zone: europe-west1-b
    - DB version: PostgreSQL 15
    - Cloud SQL Edition: Enterprise
    - Default settings of DB: Test Zone
   
    <img src=".images/db_4.png">
    <img src=".images/db_5.png">

5. Click on Create.