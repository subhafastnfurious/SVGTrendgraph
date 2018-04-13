#!/usr/bin/env python

import sys
import jinja2
import os.path
import jinja2
from collections import OrderedDict
from jinja2 import Environment, PackageLoader, select_autoescape


env = Environment(trim_blocks=True,
                  loader=jinja2.FileSystemLoader('templates'),
                  autoescape=select_autoescape(['html', 'xml']))
# trim_blocks argument will remove unnecessary new line from template.


class Trendgraph(object):
    """
    This Trendgraph class provides the functionality to read
    system generated file containing status info and render it
    to SVG template to make it browser friendly.
    """
    def __init__(self, template_name):
        """
        This is Connection class constructor or intializatio method which
        is called when we create a new instance for this class.
        The constructor is always written as a function called __init__()
            Connection  class  constructor.
                - **parameters**, **types**, **return** and **return types**::
                    :param template_name: template_name, name of the template for rendering the values.
                    :type template_name: string

        """
        if len(sys.argv) != 5:
            print "Usage: python generate_trend_graph.py starttime endtime inputfile outfile"
            sys.exit(1)
        if not os.path.exists(sys.argv[3]):
            print "File not exist: %s" % (sys.argv[3])
            sys.exit(1)

        # removing existing html file from current directory.
        pwd = os.getcwd()
        files = os.listdir(pwd)
        for item in files:
            if item.endswith(".html"):
                os.remove(os.path.join(pwd, item))

        # initializing instance variable.
        self.template = env.get_template(template_name)
        self.startstamp = int(sys.argv[1])
        self.endstamp = int(sys.argv[2])
        self.input = sys.argv[3]
        self.output = sys.argv[4]

    def render_template(self, *args, **kwargs):
        """
        This render_template method will take list of input data as argument
        and render it using the template to generate the html.
                - **parameters**, **types**, **return** and **return types**::
                    :param *args: *args will take list of data as input for rendering onto template.
                    :type *args: tuple
                    :returns html: string

        """
        # render method will  use the initialized html as template to
        # render the list of data.
        html = self.template.render(items=args[0] if args else None)
        return html

    def create_trendgraph_svg(self, *args, **kwargs):
        """
        This create_trendgraph_svg method will use initialized data
        to generate svg graph html file under current directory.
                - **parameters**, **types**, **return** and **return types**::
        """
        # html string required to add at the top and bottom of the file.
        open_svg_html = """<?xml version="1.0" encoding="utf-8"?> 
                           <svg viewBox="0 0 500 50" version="1.1" xmlns="http://www.w3.org/2000/svg">"""
        close_svg_html = """</svg>"""

        # count variable to set the rectangle index under svg html.
        chunks, count = [], 1
        # opening both input and output file.
        with open(self.input, "r") as infp, open(self.output, "a") as outfp:
            try:
                outfp.write(open_svg_html)
                for line in infp.xreadlines():
                        attrs = line.rstrip().split(" ")
                        if self.startstamp <= int(attrs[0]) <= self.endstamp:
                            chunks.append((int(attrs[0]), attrs[1], count))
                            if len(chunks) == 50:
                                htmlstr = self.render_template(chunks)
                                outfp.write(htmlstr)
                                chunks = []
                            count += 1
                htmlstr = self.render_template(chunks)
                outfp.write(htmlstr)
                outfp.write(close_svg_html)
            except Exception as e:
                    print e

if __name__ == '__main__':
    trend = Trendgraph(template_name='index.html')
    trend.create_trendgraph_svg()
