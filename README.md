# URL-Shortner
URL shortening is a technique on the World Wide Web that enables the URL to be made considerably shorter and still direct to the desired page. This is done by using a redirect path to a web page that has a long URL.

The project is developed using Django for backend and HTML and CSS for frontend.

This project has been implemented in 2 ways as you can see in the screenshot below:
1. Creating a unique short url by generating a random string of length 5 and adding it to local host(127.0.0.1:8000/) which makes the length of string exactly 20(excluding https://) and then redirecting it to long url and updating the clicks.

2. Using the bit.ly API which handles the short url generation and redirection and updating the clicks.

After generation the short url comes with a copy to clipboard button by which you can copy the link and paste it in the browser to redirect to the long url.All the available long url,short url and their clicks are displayed in a tabular format 

Here is a preview
 
 ![](static1/Screenshot%20(81).png)
 
 

 
 
