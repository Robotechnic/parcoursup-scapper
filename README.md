# parcoursup-scapper
A little python programm to get, store and plot parcoursup rancking


# How to use locally on your computer
1. Create a .env file with two variables: `USER_ID` and `PASSWORD`
```
USER_ID=user id here
PASSWORD=password here
```
2. run scrapper.py every day
3. run plot.py to see the final result

# How it works?
This programm send a request to the parcoursup website with your id and password. Then it take the main page with all your wishes and parse it to extract all your wishes to store them in a json file.
