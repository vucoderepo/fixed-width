# fixed-width
Creates and converts fixed width file into csv file. 

### Instructions to build and run Docker image:
1) Clone fixed-width project<br>
    git clone git@github.com:venu-uppala/fixed-width.git<br>
2) Change to the project root directory<br>
    cd fixed-width<br>
3) Build fixed-width docker image<br> 
    docker build -t fixed-width .<br>
4) Run fixed-width docker image in docker container<br> 
     docker run -d --name fixed-width fixed-width<br>
5) docker exec fixed-width python ./generate.py
   Output of the docker run command contains input records, generated fixed width records and generated csv records<br>
6) You can copy generated fixed width files from docker container to your host using below commands
    docker cp fixed-width:/fixed-width/generator/fw_file.txt .  
    docker cp fixed-width:/fixed-width/generator/fw_csv_file.csv . 
### Assumptions:
- Input records will be provided according to spec.json file
- Input record will be provided as a list of values for all the fields of a record
- Develop code according to spec.json file, so didn't provide a parameter to accept different specification configuration file
- Performance of code can be improved at later stage if improvement needed

### Test cases covered:
- Test Valid input record which is according to spec.json file
- Test invalid input record which is not according to spec.json file
- Test empty record
- Test with field values that are greater than field length specified in spec.json file
