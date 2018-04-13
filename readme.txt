-------------Library To Render the system status data using the timestamp input --------------------

Prerequisties
i)   python 2.7
ii)  jinja2(   For rendering the svg template  )



usage 

test.py file should be invoked with argument.
It will create the output.html file under the same directory.


python test.py starttimestamp endtimestamp inputfile.txt outputfile.html

Find all the timestamp between mentioned timestamp from inputfile.txt.
It retrieve the timestamp with associated machine status value.
Then using the value It will render svg template.




Example:


python test.py 1429004005 1429602187 testdata.txt outfile.html



Used Orderdict to store the retrieved data from file.

Using Jinja2 to render the template and redirect it to outfile.html.


Addition :   Moving the coursor over the graph will display the timestamp value.
