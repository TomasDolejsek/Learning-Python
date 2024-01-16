![Coders-Lab-1920px-no-background](https://user-images.githubusercontent.com/30623667/104709394-2cabee80-571f-11eb-9518-ea6a794e558e.png)


## Exercise 1 - done with the lecturer

Write and run your first Flask application that, upon entering `/`, greets the user with the caption: "Hello user!". 
Upon entering `/hello/<name>`, it will output the user's name entered in the parameter `<name>`.


## Exercise 2 - done with the lecturer

Write and run an application that displays the current time on the screen.


## Exercise 3

Write and run an application that displays the current date on the screen.


## Exercise 4

Using Flask, write a program that will return the result of adding two numbers sent in a GET request
`/count/number1/number2`


## Exercise 5

Using Flask, write an application, which on the GET request `/draw` will draw and display 3 digits (digits can be repeated).


## Exercise 6

Using Flask, write th application which on the GET request `/lotto` will draw and display 6 numbers in the range from 1 to 49 (the numbers cannot be repeated - this is a simulation of a lotto lottery draw).
The easiest way to draw with no repeated values is:

* create a list of elements from 1 to 49,
* mix it up,
* take the elements from 0 to 5 inclusive.

If you still need help, take a look at snippets.


## Exercise 7

Write and run an application that:

* displays on the screen a form asking the user to enter their name
* when it has been submitted, it greets the user with the message: "Hello <Name>!"


## Exercise 8

Write and run a simple calculator that:

* displays a form with two fields for entering numbers and a list of selectable operations (+, -, *, /)
* after pressing the "send" button calculates the result and displays it on the screen.


## Exercise 9

Write and run a simple guessing game that:

* draws the correct answer,
* asks the user - "Try to guess the number", displaying a form.
* after submitting the form with the answer, prints on the screen:
  * "too little!" if the user's answer is less than the number; and the form for entering value again,
  * "too many!" if the user's answer is greater than the number; and the form for entering value again,
  * "Congratulations, you made it!" if the user guessed the number.

### Preliminary information for the next tasks
[https://www.garron.me/en/bits/curl-delete-request.html](https://www.garron.me/en/bits/curl-delete-request.html)

[http://superuser.com/questions/149329/what-is-the-curl-command-line-syntax-to-do-a-post-request](http://superuser.com/questions/149329/what-is-the-curl-command-line-syntax-to-do-a-post-request)



## Exercise 10

Using Flask, write a program that will respond to a request sent to `/` (that is, `http://localhost:5000/`) depending on the method it was sent through:
- if the method was POST - the response will be the string "You have sent a POST",
- if the method was GET - the response will be the string "You have sent a GET".

<!--- if the method was PUT - the response will be the string "You have sent a PUT".
- if the method was DELETE - the response will be the string "You have sent a DELETE"-->


## Exercise 11

Using Flask, write and run a program that:

* upon entering using the GET method will display an empty form with the following fields:
    * name,
    * surname,
    * "Send" button.
* the above form should send data using the POST method.
* when accessed using the POST method, it will display the message "Hello _name surname_".
