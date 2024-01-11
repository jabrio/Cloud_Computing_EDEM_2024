# AWS Cloud Computing Fundamentals exercise


## 1. EC2 instance

1. Create an EC2 instance following the instructions in the [README.md](/00_DocAux/AWS/README.md) file.

2. Install Docker following either the commands below (Fedora distribution) or the instructions in the [README.md](/00_DocAux/AWS/README.md) file.

    ```bash
    sudo apt update
    sudo apt install --yes apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt update
    sudo apt install --yes docker-ce
    sudo usermod -aG docker $USER
    logout 
    ```
    
3. Log in again to the EC2 instance and run the following command to check that Docker is installed correctly:

    ```bash
    docker run hello-world
    ```
4. Run the following command to copy all the files from the folder `01_Code/01_Fundamentals/AWS/01_EC2` to the EC2 instance:

    ```bash
    scp -i "ejercicio1.pem" -r . <VM-user>@<VM-IP>:~/
    ``

5. Run `docker compose up -d` from the `01_Code/01_Fundamentals/GCP/01_VM` folder. This will create a postgres database, run the init.sql script creating a table and inserting some data from a csv file.
   
6. Once the database is created, you can try to access the container by running `docker exec -it <container_id> psql -U initexample` and then `select * from employees_data limit 10;` This will show you 10 files of the table created.

7. Now we will configure the inbound rules of the EC2 instance to allow the connection to the database. To do so, follow these steps:
    7.1 Go to the EC2 section in the AWS console and click on `Security Groups`.
    7.2 Select the security group of the EC2 instance and click on `Edit inbound rules`.
   
    7.3 Add a new rule with the following parameters:
    - Type: PostgreSQL
    - Protocol: TCP
    - Port range: 5432
    - Source: Anywhere
   
    7.4 Click on `Save rules`.

8. From there, you can connect to the database using the following credentials:
   - Host: \<VM external IP\>
   - Port: 5432
   - User: initexample
   - Password: initexample
   - Database: initexample

9. Once everything is set up, you can try to run the following query to check that everything is working properly:
   ```sql
   select * from employees_data limit 10;
   ```

<br>

## 2. S3 bucket

### 2.1. Read from a bucket

1. Create a bucket following the instructions in the [README.md](/00_DocAux/AWS/README.md) file.

2. Upload the content of the folder `01_Code/01_Fundamentals/AWS/02_S3` to `AWS Cloud Shell`.

3. Run the command to install the requirements: `pip install -r requirements.txt`

4. Run the command to read the file from the bucket: `python read_from_bucket.py`

### 2.2. Write to a bucket

1. Run the command to write the file to the bucket: `python write_files.py`

2. Go to the S3 section in the AWS console and check that the file has been uploaded correctly.

<br>


## 3. RDS Database PostgreSQL instance

1. Create a PostgreSQL instance following the instructions in the [README.md](/00_DocAux/AWS/README.md) file.

2. Run the script `insert-data.py` to insert the data from the file `employee_data.csv` into the database.

3. We will then use DBeaver to connect to the database. To do so, follow these steps:
    3.1 Go to the RDS section in the AWS console and click on `Databases`.
    3.2 Once installed, open DBeaver and click on `New connection`.
    3.3 Select `PostgreSQL` as the database and click on `Next`.
    3.4 Fill in the following parameters:
    - Host: \<DB endpoint\>
    - Port: 5432
    - Database: postgres
    - User name: postgres
    - Password: EDEM2024
    3.5 Click on `Test connection` to check that everything is working properly.
    3.6 Click on `Finish` to save the connection.
    3.7 Click on `Connect` to connect to the database.
    3.8 Once connected, you can run the following query to check that everything is working properly:
    ```sql
    select * from <schema>.employees_data limit 10;
    ```