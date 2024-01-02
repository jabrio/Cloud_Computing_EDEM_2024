# Cloud computing fundamentals excercises

## 1. Virtual machines

1. Create a VM following the instructions in the [README.md](01_VirtualMachines/README.md) file.

2. Install Docker by following the steps of this link: https://tomroth.com.au/gcp-docker/
   
3. Once docker is installed, upload the folder `01_Code/01_Fundamentals/GCP/01_VM` to the VM.
   <img src=".images/vm_1.png" width="500">

4. Run `docker compose up -d` from the `01_Code/01_Fundamentals/GCP/01_VM` folder. This will create a postgres database, run the init.sql script creating a table and inserting some data from a csv file.
   
5. Once the database is created, you can try to access the container by running `docker exec -it <container_id> psql -U initexample` and then `select * from employees_data limit 10;` This will show you 10 files of the table created.
   
6. However, if want to access it from your local machine, you need to create a firewall rule to allow the connection. To do so, go to the VPC network section in the GCP console and create a new firewall rule. To do so, follow these steps:
    6.1 Go to the VPC network section in the GCP console and create a new firewall rule.
    <img src=".images/vm_3.png" width="500">
    <img src=".images/vm_4.png" width="500">
    6.2 Create a new firewall rule with the following parameters:
    <img src=".images/vm_5.png" width="500">
    <img src=".images/vm_6.png" width="500">

7. Try to query the database from the VM. You can install the following vscode extension to do so https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql

8. From there, you can connect to the database using the following credentials:
   - Host: \<VM external IP\>
   - Port: 5432
   - User: initexample
   - Password: initexample
   - Database: initexample
    <img src=".images/vm_2.png" width="500">

9. Once everything is set up, you can try to run the following query to check that everything is working properly:
   ```sql
   select * from employees_data limit 10;
   ```

