# Cloud computing fundamentals

## 1. Compute Engine

Compute Engine is a service that provides virtual machines that run on Google infrastructure. Compute Engine offers scale, performance, and value that allows you to easily launch large compute clusters on Google's infrastructure. There are no upfront investments and you can run thousands of virtual CPUs on a system that has been designed to be fast, and to offer strong consistency of performance.

To create and manage your virtual machines, you can use Google Cloud CLI or the web UI. In this exercise, you will use first the web UI and then the CLI.

### 1.1. Create a Compute Engine instance

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