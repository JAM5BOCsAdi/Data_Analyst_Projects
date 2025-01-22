You can not use Direct Query with an API call, only Import (Storage Mode).
https://blog.crossjoin.co.uk/2021/04/25/can-i-build-a-power-bi-directquery-dataset-on-top-of-a-rest-api/

So if you want to build a Power Bi Dasboard that gets the data from an API, for example this Weather Report 
project uses WeatherStack API, BUT this WeatherStack does not allow Multiple Locations (Only with subscription).

If you have subscription you can do that, by only including the countries you want to see.
For example here: https://weatherstack.com/documentation
Search for: "Multiple Locations (Professional Plan and higher)" [CTRL+F]

And a lot of API only allows Single location, and for subscription you can do multiple locations.
So if you are broke as me, you can not use multiple locations, to connect with Power Bi. Only Single location, 
but you can not use all the Countries, because you need Direct Query Connection to data (API), because until that you
can not Bind Parameter(s) to a table.

