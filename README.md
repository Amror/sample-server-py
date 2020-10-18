# sample-server-py
A chocolate related recipes website with actual good recipes and nutritional information about them.  
A login system and a rating system are included and may be used to express your feelings about the amazing recipes!

As for the code, the client side is built with HTML, CSS and JavaScript + Jquery.  
The server side is built mainly with flask and pymongo in Python, flask is used for endpoint routing and serves as most of the logic layer while a set of functions built on top of pymongo manage the data access from the MongoDB database.


## Installation & Execution
1. Open cmd in the repository directory or cd into the repository directory through the cmd
2. Run `pip install -r requirements.txt`
3. Insert mongodb connection info in **db_config.json**
4. Run **main.py**
5. View the website at **localhost:5000**

## External Modules Used
- [flask](https://flask.palletsprojects.com/en/1.1.x/)
- [pymongo](https://pymongo.readthedocs.io/en/stable/)
- [hashlib](https://docs.python.org/3/library/hashlib.html)
- [uuid](https://docs.python.org/3/library/uuid.html)
- [os](https://docs.python.org/3/library/os.html)
- [re](https://docs.python.org/3/library/re.html)
- [datetime](https://docs.python.org/3/library/datetime.html)
- [json](https://docs.python.org/3/library/json.html)

## Notes
- The website is built without any css framework and without responsive css design, becasue of this, the website might look a
bit messy when resized or viewed from phone/tablet viewport
- The chocolate rolls recipe is the best one

## Credits
- Created by Ofek [[Amror]](https://github.com/Amror)